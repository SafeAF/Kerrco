"""Small WSGI inquiry endpoint. Nginx serves the site; Gunicorn runs this app.

Only the configured recipient receives mail. No visitor autoresponder, uploads,
message database, or payload logging. SMTP acceptance is required for success.
"""
from collections import OrderedDict
from dataclasses import dataclass, field
from email.headerregistry import Address
from email.errors import HeaderParseError
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from html import escape
import ipaddress
import json
import mimetypes
import os
from pathlib import Path
import re
import smtplib
import ssl
import sys
from threading import Lock
import time
from urllib.parse import parse_qs, urlsplit

MAX_BODY = 65_536
FIELDS = {'name', 'email', 'business', 'message', 'website'}


def mailbox(value):
    if not value or len(value) > 254 or not value.isascii() or re.search(r'[\s<>\x00-\x1f\x7f]', value):
        raise ValueError('Invalid email address')
    try:
        parsed = Address(addr_spec=value)
    except (ValueError, IndexError, HeaderParseError) as error:
        raise ValueError('Invalid email address') from error
    if not parsed.username or '.' not in parsed.domain or parsed.addr_spec != value:
        raise ValueError('Invalid email address')
    return value


@dataclass(frozen=True)
class Settings:
    origin: str = 'https://kerrco.us'
    recipient: str = 'kerrcoenterprises@gmail.com'
    sender: str = ''
    smtp_host: str = '127.0.0.1'
    smtp_port: int = 25
    smtp_security: str = 'local'
    smtp_username: str = field(default='', repr=False)
    smtp_password: str = field(default='', repr=False)

    @classmethod
    def from_env(cls):
        return cls(
            origin=os.environ.get('KERRCO_SITE_ORIGIN', cls.origin),
            recipient=os.environ.get('KERRCO_INQUIRY_TO', cls.recipient),
            sender=os.environ.get('KERRCO_INQUIRY_FROM', ''),
            smtp_host=os.environ.get('KERRCO_SMTP_HOST', cls.smtp_host),
            smtp_port=int(os.environ.get('KERRCO_SMTP_PORT', '25')),
            smtp_security=os.environ.get('KERRCO_SMTP_SECURITY', 'local'),
            smtp_username=os.environ.get('KERRCO_SMTP_USERNAME', ''),
            smtp_password=os.environ.get('KERRCO_SMTP_PASSWORD', ''),
        )

    def validate_delivery(self):
        mailbox(self.recipient)
        mailbox(self.sender)
        if self.smtp_security not in {'local', 'starttls', 'ssl'}:
            raise ValueError('Invalid SMTP security mode')
        if not self.smtp_host or not 1 <= self.smtp_port <= 65535:
            raise ValueError('SMTP host and port must be configured')
        if self.smtp_security == 'local' and self.smtp_host not in {'127.0.0.1', '::1', 'localhost'}:
            raise ValueError('Unencrypted SMTP is restricted to loopback')
        if bool(self.smtp_username) != bool(self.smtp_password):
            raise ValueError('Both SMTP credentials must be configured')


class RateLimit:
    """A single Gunicorn worker shares this bounded, thread-safe memory state."""
    def __init__(self, limit=5, seconds=600, capacity=4096, clock=time.monotonic):
        self.limit, self.seconds, self.capacity, self.clock = limit, seconds, capacity, clock
        self.buckets, self.lock = OrderedDict(), Lock()

    def allow(self, key):
        now = self.clock()
        with self.lock:
            expired = [key for key, (started, _) in self.buckets.items() if now - started >= self.seconds]
            for old in expired:
                del self.buckets[old]
            if key not in self.buckets:
                # Fail closed at capacity; do not evict active limits to admit a flood.
                if len(self.buckets) >= self.capacity:
                    return False
                self.buckets[key] = (now, 0)
            started, count = self.buckets[key]
            if count >= self.limit:
                return False
            self.buckets[key] = (started, count + 1)
            return True


def client_ip(environ):
    peer = environ.get('REMOTE_ADDR', '')
    if peer in {'127.0.0.1', '::1'} and environ.get('HTTP_X_REAL_IP'):
        peer = environ['HTTP_X_REAL_IP']
    try:
        return str(ipaddress.ip_address(peer))
    except ValueError:
        return 'unknown'


def deliver(settings, fields):
    settings.validate_delivery()
    message = EmailMessage()
    message['From'] = Address('KERRCO website', addr_spec=settings.sender)
    message['To'] = settings.recipient
    message['Reply-To'] = Address(fields['name'], addr_spec=fields['email'])
    message['Subject'] = 'KERRCO software consultation inquiry'
    message['Date'] = formatdate(localtime=False, usegmt=True)
    message['Message-ID'] = make_msgid(domain=settings.sender.split('@')[1])
    message.set_content('\n'.join([
        'Website inquiry', '', 'Name: ' + fields['name'],
        'Reply email: ' + fields['email'],
        'Business: ' + (fields['business'] or '(not supplied)'), '', fields['message'],
    ]))
    connection = None
    try:
        if settings.smtp_security == 'ssl':
            connection = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=8, context=ssl.create_default_context())
        else:
            connection = smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=8)
            if settings.smtp_security == 'starttls':
                connection.starttls(context=ssl.create_default_context())
                connection.ehlo()
        if settings.smtp_username:
            connection.login(settings.smtp_username, settings.smtp_password)
        refused = connection.send_message(message, from_addr=settings.sender, to_addrs=[settings.recipient])
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)
    finally:
        if connection:
            try:
                connection.quit()
            except (OSError, smtplib.SMTPException):
                connection.close()


class Application:
    def __init__(self, settings=None, sender=deliver, limiter=None, preview=False):
        self.settings = settings or Settings.from_env()
        self.sender = sender
        self.limiter = limiter or RateLimit()
        self.preview = preview

    def respond(self, environ, start_response, status, message, ok=False, preview=False):
        wants_json = 'application/json' in environ.get('HTTP_ACCEPT', '')
        if wants_json:
            payload = {'ok': ok}
            payload['message' if ok or preview else 'error'] = message
            if preview:
                payload['preview'] = True
            body = json.dumps(payload).encode('utf-8')
            content_type = 'application/json; charset=utf-8'
        else:
            title = 'Inquiry submitted' if ok else 'Inquiry preview' if preview else 'Inquiry not sent'
            body = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>{title} | KERRCO</title><link rel="stylesheet" href="/assets/css/home.css"></head><body><main class="wrap page-intro"><p class="eyebrow">KERRCO / Software consulting</p><h1>{title}</h1><p class="intro">{escape(message)}</p><p><a href="/contact.html#inquiry">Return to the inquiry page</a></p><p>Prefer email? <a href="mailto:{escape(self.settings.recipient, quote=True)}">{escape(self.settings.recipient)}</a></p></main></body></html>'''.encode('utf-8')
            content_type = 'text/html; charset=utf-8'
        headers = [('Content-Type', content_type), ('Content-Length', str(len(body))), ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff'), ('Referrer-Policy', 'same-origin'), ('Content-Security-Policy', "default-src 'none'; style-src 'self'; base-uri 'none'; frame-ancestors 'none'")]
        if status.startswith('405'):
            headers.append(('Allow', 'POST'))
        if status.startswith('429'):
            headers.append(('Retry-After', str(self.limiter.seconds)))
        start_response(status, headers)
        return [body]

    def __call__(self, environ, start_response):
        def reply(status, text, **kwargs):
            return self.respond(environ, start_response, status, text, **kwargs)
        if environ.get('PATH_INFO') != '/inquiries':
            return reply('404 Not Found', 'This page could not be found.')
        if environ.get('REQUEST_METHOD') != 'POST':
            return reply('405 Method Not Allowed', 'Please use the inquiry form to send a message.')
        origin = environ.get('HTTP_ORIGIN')
        if not origin and environ.get('HTTP_REFERER'):
            try:
                parsed = urlsplit(environ['HTTP_REFERER'])
                origin = parsed.scheme + '://' + parsed.netloc
            except ValueError:
                origin = None
        if origin != self.settings.origin or environ.get('HTTP_SEC_FETCH_SITE') == 'cross-site':
            return reply('403 Forbidden', 'Please open the inquiry form on the KERRCO website and try again.')
        if environ.get('CONTENT_TYPE', '').split(';')[0].strip().lower() != 'application/x-www-form-urlencoded':
            return reply('415 Unsupported Media Type', 'Please submit the inquiry using the website form.')
        try:
            length = int(environ.get('CONTENT_LENGTH', ''))
        except ValueError:
            return reply('411 Length Required', 'The inquiry could not be read. Please try again.')
        if not 0 < length <= MAX_BODY:
            return reply('413 Content Too Large', 'Please shorten the inquiry and try again.')
        if not self.limiter.allow(client_ip(environ)):
            return reply('429 Too Many Requests', 'Too many attempts. Please wait a few minutes or use the email address alongside the form.')
        try:
            raw = environ['wsgi.input'].read(length)
            if len(raw) != length:
                raise ValueError('Incomplete body')
            values = parse_qs(raw.decode('utf-8', errors='strict'), keep_blank_values=True, max_num_fields=8, errors='strict')
            if not set(values) <= FIELDS or any(len(value) != 1 for value in values.values()):
                raise ValueError('Unexpected or duplicate fields')
            fields = {key: values.get(key, [''])[0].strip() for key in FIELDS}
            if fields['website']:
                raise ValueError('Honeypot')
            for key, limit in [('name', 120), ('business', 160), ('email', 254)]:
                if len(fields[key]) > limit or re.search(r'[\x00-\x1f\x7f]', fields[key]):
                    raise ValueError('Invalid field')
            if not fields['name'] or not 10 <= len(fields['message']) <= 5000 or re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', fields['message']):
                raise ValueError('Invalid message')
            mailbox(fields['email'])
        except (ValueError, UnicodeError, IndexError):
            return reply('422 Unprocessable Content', 'Please check your name, email address, and message (10–5,000 characters).')
        if self.preview:
            return reply('200 OK', 'Preview only. Your inquiry has not been sent. Use Back to keep editing or return to the inquiry page.', preview=True)
        try:
            self.sender(self.settings, fields)
        except Exception as error:
            # Never log submitted fields, SMTP payloads, credentials, or reply addresses.
            print('Inquiry delivery unavailable (' + type(error).__name__ + ')', file=sys.stderr)
            return reply('503 Service Unavailable', 'Your inquiry could not be sent. Please try again or use the email address alongside the form.')
        return reply('201 Created', 'Thank you. Your inquiry has been submitted. I’ll respond by email.', ok=True)


def create_app():
    """Production factory: configuration errors prevent service startup."""
    settings = Settings.from_env()
    settings.validate_delivery()
    return Application(settings)


if __name__ == '__main__':
    import argparse
    from wsgiref.simple_server import make_server, WSGIRequestHandler
    parser = argparse.ArgumentParser(description='Local site preview; no email is sent.')
    parser.add_argument('--port', type=int, default=8091)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / 'web'
    preview = Application(Settings(origin=f'http://127.0.0.1:{args.port}'), preview=True)

    def development(environ, start_response):
        route = environ.get('PATH_INFO', '/')
        if route == '/inquiries':
            return preview(environ, start_response)
        path = (root / route.lstrip('/')).resolve()
        if route == '/':
            path = root / 'index.html'
        allowed = path.is_relative_to(root) and path.is_file() and path.suffix in {'.html', '.css', '.js', '.jpg', '.jpeg', '.png', '.svg', '.webp', '.ico', '.txt', '.xml'}
        if environ['REQUEST_METHOD'] not in {'GET', 'HEAD'} or not allowed:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'Not found']
        data = path.read_bytes()
        start_response('200 OK', [('Content-Type', mimetypes.guess_type(path)[0] or 'application/octet-stream'), ('Content-Length', str(len(data))), ('Cache-Control', 'no-store')])
        return [] if environ['REQUEST_METHOD'] == 'HEAD' else [data]

    class QuietHandler(WSGIRequestHandler):
        def log_message(self, *args):
            pass

    print(f'Local preview: http://127.0.0.1:{args.port}/ — form preview only; no email is sent.', flush=True)
    with make_server('127.0.0.1', args.port, development, handler_class=QuietHandler) as server:
        server.serve_forever()
