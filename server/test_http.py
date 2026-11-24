"""Optional production-WSGI integration test using only loopback and .test mail."""
import http.client
import json
import os
from pathlib import Path
import socket
import subprocess
import time
import unittest
from urllib.parse import urlencode

from test_inquiry import smtp_capture


@unittest.skipUnless(os.environ.get('KERRCO_GUNICORN'), 'Set KERRCO_GUNICORN to run the production HTTP/SMTP integration test')
class HTTPTest(unittest.TestCase):
    def test_actual_gunicorn_json_native_form_and_rejection(self):
        executable = os.environ['KERRCO_GUNICORN']
        self.assertTrue(Path(executable).is_file())
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            port = listener.getsockname()[1]
        origin = f'http://127.0.0.1:{port}'
        with smtp_capture() as (smtp_port, captured):
            env = {**os.environ, 'KERRCO_SITE_ORIGIN': origin, 'KERRCO_INQUIRY_FROM': 'website@example.test', 'KERRCO_INQUIRY_TO': 'owner@example.test', 'KERRCO_SMTP_HOST': '127.0.0.1', 'KERRCO_SMTP_PORT': str(smtp_port), 'KERRCO_SMTP_SECURITY': 'local', 'KERRCO_SMTP_USERNAME': '', 'KERRCO_SMTP_PASSWORD': ''}
            process = subprocess.Popen([executable, '--config', 'gunicorn.conf.py', '--bind', f'127.0.0.1:{port}', '--log-level', 'error', 'inquiry:create_app()'], cwd=Path(__file__).parent, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            def request(method, body=None, **headers):
                connection = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
                try:
                    connection.request(method, '/inquiries', body, headers)
                    response = connection.getresponse()
                    return response.status, response.read(), dict(response.getheaders())
                finally:
                    connection.close()
            try:
                ready = False
                for attempt in range(60):
                    if process.poll() is not None:
                        self.fail('Gunicorn failed to start: ' + process.stderr.read().decode())
                    try:
                        ready = request('GET')[0] == 405
                    except OSError:
                        pass
                    if ready:
                        break
                    time.sleep(.05)
                self.assertTrue(ready, 'Production WSGI server never became ready')
                data = urlencode({'name': 'Example Visitor', 'email': 'visitor@example.test', 'message': 'Please review our example software.'})
                headers = {'Origin': origin, 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
                status, body, returned = request('POST', data, **headers)
                self.assertEqual(status, 201)
                self.assertTrue(json.loads(body)['ok'])
                self.assertEqual(returned['Cache-Control'], 'no-store')
                self.assertEqual(len(captured), 1)
                status, body, returned = request('POST', data, **{**headers, 'Accept': 'text/html'})
                self.assertEqual(status, 201)
                self.assertIn(b'Inquiry submitted', body)
                self.assertEqual(len(captured), 2)
                status, body, returned = request('POST', data, **{**headers, 'Origin': 'https://other.example'})
                self.assertEqual(status, 403)
                self.assertEqual(len(captured), 2)
                status, body, returned = request('POST', data + '&to=other%40example.test', **headers)
                self.assertEqual(status, 422)
                self.assertEqual(len(captured), 2)
            finally:
                process.terminate()
                process.communicate(timeout=10)
