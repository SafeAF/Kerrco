<?php
  declare(strict_types=1);

  header('Content-Type: text/plain; charset=utf-8');

  if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Method not allowed.';
    exit;
  }

  $name = trim((string) ($_POST['name'] ?? ''));
  $email = trim((string) ($_POST['email'] ?? ''));
  $phone = trim((string) ($_POST['phone'] ?? ''));
  $message = trim((string) ($_POST['message'] ?? ''));

  if ($name === '' || $email === '' || $message === '') {
    http_response_code(422);
    echo 'Please complete the required fields.';
    exit;
  }

  if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo 'Please enter a valid email address.';
    exit;
  }

  $to = 'kerrcoenterprises@gmail.com';
  $subject = 'Request for a quote';
  $safeName = preg_replace('/[\r\n]+/', ' ', $name);
  $body = implode("\n", [
    'Website quote request',
    '',
    'Name: ' . $name,
    'Email: ' . $email,
    'Phone: ' . ($phone !== '' ? $phone : 'Not provided'),
    '',
    $message,
  ]);
  $headers = [
    'From: KERRCO Website <kerrcoenterprises@gmail.com>',
    'Reply-To: ' . $safeName . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
  ];

  if (mail($to, $subject, $body, implode("\r\n", $headers))) {
    echo 'OK';
    exit;
  }

  http_response_code(500);
  echo 'Unable to send message.';
?>
