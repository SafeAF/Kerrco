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
  $subject = trim((string) ($_POST['subject'] ?? 'Website contact request'));
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
  $safeName = preg_replace('/[\r\n]+/', ' ', $name);
  $safeSubject = preg_replace('/[\r\n]+/', ' ', $subject);
  $body = implode("\n", [
    'Website contact request',
    '',
    'Name: ' . $name,
    'Email: ' . $email,
    '',
    $message,
  ]);
  $headers = [
    'From: KERRCO Website <kerrcoenterprises@gmail.com>',
    'Reply-To: ' . $safeName . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
  ];

  if (mail($to, $safeSubject, $body, implode("\r\n", $headers))) {
    echo 'OK';
    exit;
  }

  http_response_code(500);
  echo 'Unable to send message.';
?>
