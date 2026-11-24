from contextlib import contextmanager, redirect_stderr
from dataclasses import replace
from email import policy
from email.parser import BytesParser
from io import BytesIO, StringIO
import json
import socketserver
from threading import Thread
import unittest
from urllib.parse import urlencode
from wsgiref.util import setup_testing_defaults

from inquiry import Application, MAX_BODY, RateLimit, Settings, client_ip


@contextmanager
def smtp_capture(reject=False):
    captured = []

    class SMTP(socketserver.StreamRequestHandler):
        def handle(self):
            self.wfile.write(b'220 local test fixture\r\n')
            recipients = []
            while True:
                line = self.rfile.readline()
                if not line:
                    return
                command = line.upper()
                if command.startswith((b'EHLO', b'HELO')):
                    self.wfile.write(b'250 local test fixture\r\n')
                elif command.startswith(b'MAIL FROM:'):
                    self.wfile.write(b'250 sender accepted\r\n')
                elif command.startswith(b'RCPT TO:'):
                    recipients.append(line.decode().strip())
                    self.wfile.write(b'550 rejected by test fixture\r\n' if reject else b'250 recipient accepted\r\n')
                elif command.startswith(b'DATA'):
                    self.wfile.write(b'354 message follows\r\n')
                    lines = []
                    while True:
                        data = self.rfile.readline()
                        if data in {b'.\r\n', b''}:
                            break
                        lines.append(data[1:] if data.startswith(b'..') else data)
                    captured.append((recipients[:], b''.join(lines)))
                    self.wfile.write(b'250 message accepted\r\n')
                elif command.startswith(b'QUIT'):
                    self.wfile.write(b'221 bye\r\n')
                    return
                elif command.startswith(b'RSET'):
                    self.wfile.write(b'250 reset\r\n')
                else:
                    self.wfile.write(b'500 unsupported\r\n')

    with socketserver.ThreadingTCPServer(('127.0.0.1', 0), SMTP) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield server.server_address[1], captured
        finally:
            server.shutdown()
            thread.join()


class InquiryTest(unittest.TestCase):
    def setUp(self):
        self.fields = {'name': 'Test Visitor', 'email': 'visitor@example.test', 'business': 'Example business', 'message': 'Please help with our example software workflow.', 'website': ''}
        self.sent = []
        self.settings = Settings(sender='website@example.test', recipient='owner@example.test')
        self.app = Application(self.settings, sender=lambda settings, fields: self.sent.append(fields))

    def request(self, fields=None, app=None, **headers):
        fields = self.fields if fields is None else fields
        raw = fields if isinstance(fields, bytes) else urlencode(fields).encode()
        environ = {}
        setup_testing_defaults(environ)
        environ.update(PATH_INFO='/inquiries', REQUEST_METHOD='POST', HTTP_ORIGIN='https://kerrco.us', HTTP_ACCEPT='application/json', CONTENT_TYPE='application/x-www-form-urlencoded', CONTENT_LENGTH=str(len(raw)), REMOTE_ADDR='192.0.2.10')
        environ.update(headers)
        environ['wsgi.input'] = BytesIO(raw)
        response = {}
        def start(status, values):
            response.update(status=int(status.split()[0]), headers=dict(values))
        body = b''.join((app or self.app)(environ, start))
        response['body'] = body
        if response['headers']['Content-Type'].startswith('application/json'):
            response['json'] = json.loads(body)
        return response

    def test_smtp_acceptance_required_and_envelope_is_fixed(self):
        with smtp_capture() as (port, captured):
            response = self.request(app=Application(replace(self.settings, smtp_port=port)))
        self.assertEqual(response['status'], 201)
        self.assertTrue(response['json']['ok'])
        self.assertEqual(len(captured), 1)
        recipients, raw = captured[0]
        self.assertEqual(recipients, ['rcpt TO:<owner@example.test>'])
        message = BytesParser(policy=policy.default).parsebytes(raw)
        self.assertEqual(message['Reply-To'].addresses[0].addr_spec, 'visitor@example.test')
        self.assertEqual(message['To'], 'owner@example.test')
        self.assertEqual(message['From'].addresses[0].addr_spec, 'website@example.test')
        self.assertEqual(message['Subject'], 'KERRCO software consultation inquiry')
        self.assertIn(self.fields['message'], message.get_content())

    def test_smtp_rejection_never_returns_success_or_logs_payload(self):
        output = StringIO()
        with smtp_capture(reject=True) as (port, captured), redirect_stderr(output):
            response = self.request(app=Application(replace(self.settings, smtp_port=port)))
        self.assertEqual(response['status'], 503)
        self.assertFalse(response['json']['ok'])
        self.assertEqual(captured, [])
        for value in [self.fields['name'], self.fields['email'], self.fields['message']]:
            self.assertNotIn(value, output.getvalue())

    def test_unconfigured_delivery_fails_closed(self):
        with redirect_stderr(StringIO()):
            response = self.request(app=Application(Settings()))
        self.assertEqual(response['status'], 503)
        self.assertFalse(response['json']['ok'])

    def test_origin_and_referer_checks(self):
        for origin in ['', 'null', 'https://other.example', 'https://kerrco.us.other.example']:
            with self.subTest(origin=origin):
                self.assertEqual(self.request(HTTP_ORIGIN=origin)['status'], 403)
        self.assertEqual(self.request(HTTP_ORIGIN='', HTTP_REFERER='https://kerrco.us/contact.html')['status'], 201)
        self.assertEqual(self.request(HTTP_ORIGIN='', HTTP_REFERER='http://[')['status'], 403)
        self.assertEqual(self.request(HTTP_SEC_FETCH_SITE='cross-site')['status'], 403)

    def test_invalid_fields_and_header_injection_are_rejected(self):
        for field, value in [('name', ''), ('name', 'Name\r\nBcc: other@example.test'), ('email', 'bad address'), ('email', 'a@@example.test'), ('email', 'x@example.test\r\nBcc: z@example.test'), ('business', 'x' * 161), ('message', 'short'), ('message', 'x' * 5001), ('message', 'bad\x00message' * 3), ('website', 'bot')]:
            with self.subTest(field=field, value=value):
                app = Application(self.settings, sender=lambda *args: self.fail('Invalid inquiry sent'))
                self.assertEqual(self.request({**self.fields, field: value}, app=app)['status'], 422)
        self.assertEqual(self.sent, [])

    def test_extra_recipients_and_duplicate_fields_rejected(self):
        for fields in [{**self.fields, 'to': 'other@example.test'}, urlencode(self.fields).encode() + b'&email=other%40example.test']:
            self.assertEqual(self.request(fields)['status'], 422)
        self.assertEqual(self.sent, [])

    def test_bad_bytes_body_limit_and_content_type(self):
        self.assertEqual(self.request(b'name=\xff')['status'], 422)
        self.assertEqual(self.request(CONTENT_LENGTH=str(MAX_BODY + 1))['status'], 413)
        self.assertEqual(self.request(CONTENT_LENGTH='')['status'], 411)
        self.assertEqual(self.request(CONTENT_LENGTH='-1')['status'], 413)
        self.assertEqual(self.request(CONTENT_TYPE='application/json')['status'], 415)
        self.assertEqual(self.sent, [])

    def test_optional_business_unicode_and_message_preserved(self):
        fields = {**self.fields, 'business': '', 'name': 'Zoë Example', 'message': 'First line.\nSecond line with “quoted” text.'}
        self.assertEqual(self.request(fields)['status'], 201)
        self.assertEqual(self.sent[0]['message'], fields['message'])
        self.assertEqual(self.sent[0]['name'], fields['name'])

    def test_native_form_and_security_headers(self):
        response = self.request(HTTP_ACCEPT='text/html')
        self.assertEqual(response['status'], 201)
        self.assertIn(b'Inquiry submitted', response['body'])
        self.assertNotIn(self.fields['name'].encode(), response['body'])
        self.assertEqual(response['headers']['Cache-Control'], 'no-store')
        self.assertIn("frame-ancestors 'none'", response['headers']['Content-Security-Policy'])

    def test_wrong_method_and_path(self):
        response = self.request(REQUEST_METHOD='GET')
        self.assertEqual(response['status'], 405)
        self.assertEqual(response['headers']['Allow'], 'POST')
        self.assertEqual(self.request(PATH_INFO='/other')['status'], 404)

    def test_rate_limit_blocks_and_expires(self):
        clock = [0]
        app = Application(self.settings, sender=lambda *args: None, limiter=RateLimit(limit=2, seconds=60, clock=lambda: clock[0]))
        self.assertEqual(self.request(app=app)['status'], 201)
        self.assertEqual(self.request(app=app)['status'], 201)
        self.assertEqual(self.request(app=app)['status'], 429)
        clock[0] = 60
        self.assertEqual(self.request(app=app)['status'], 201)

    def test_proxy_ip_cannot_be_spoofed_by_nonlocal_peer(self):
        self.assertEqual(client_ip({'REMOTE_ADDR': '192.0.2.10', 'HTTP_X_REAL_IP': '192.0.2.20'}), '192.0.2.10')
        self.assertEqual(client_ip({'REMOTE_ADDR': '127.0.0.1', 'HTTP_X_REAL_IP': '192.0.2.20'}), '192.0.2.20')

    def test_rate_limit_capacity_fails_closed(self):
        limiter = RateLimit(capacity=1)
        self.assertTrue(limiter.allow('first'))
        self.assertFalse(limiter.allow('second'))

    def test_preview_is_not_a_delivery_confirmation(self):
        response = self.request(app=Application(self.settings, sender=lambda *args: self.fail('Preview sent mail'), preview=True))
        self.assertEqual(response['status'], 200)
        self.assertFalse(response['json']['ok'])
        self.assertTrue(response['json']['preview'])

    def test_remote_plaintext_smtp_disallowed(self):
        with self.assertRaises(ValueError):
            replace(self.settings, smtp_host='mail.example.test').validate_delivery()

    def test_configuration_representation_omits_credentials(self):
        settings = replace(self.settings, smtp_username='test-user', smtp_password='test-password')
        self.assertNotIn('test-user', repr(settings))
        self.assertNotIn('test-password', repr(settings))


if __name__ == '__main__':
    unittest.main()
