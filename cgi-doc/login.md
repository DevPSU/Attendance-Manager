# Documenmtation for login API

---

## Introduction

This documentation explains how to log into an account. The API is based on HTTP. "Chellenge-response authentication" is used so 2 requests need to be sent.

---

## Challenge

The 1st request is to get the "salt" and "challenge" of the account.

---

### Request

The request should be sent to [https://devpsu.whmhammer.com/cgi/challenge.py](https://devpsu.whmhammer.com/cgi/challenge.py) using **POST** method with the following parameter:

### `login` (REQUIRED)

The username **or** the email address of the account.

---

### Response

The response is always in `text/plain`.

The 1st line indicates the status of the registration. Here is a list of possible outcomes (case sensitive):

- `Success`

- `Use POST method`

- `Missing parameter`

- `Illegal login`

- `User not found`

- `User hasn't been verified`

- `Unexpected error`

A randomly generated "challenge" is written to the database only when the responded status is `success`. The challenge is also a 32-digit string containing only alphabetical and digital characters. The "challenge" is in the same format as the "salt" but they function differently. In this case (the 1st line is `success`), the "salt" will be given in the 2nd line, and the "challenge" will be given in the 3rd line.

---

## Response

The 2nd request sends the hashed password to the server.

---

### Request

The request should be sent to [https://devpsu.whmhammer.com/cgi/login.py](https://devpsu.whmhammer.com/cgi/login.py) using **POST** method with the following parameter:

#### `login` (REQUIRED)

The username **or** the email address of the account.

#### `response` (REQUIRED)

The 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "challenge" (got from the previous request) and the 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "salt" (got from the previous request) and the raw password.

---

### Response

The response is always in `text/plain`.

The first line indicates the status of the registration. Here is a list of possible outcomes (case sensitive):

- `Success`

- `Use POST method`

- `Missing parameter`

- `Illegal login` (the `login` given is neither a legal username nor a legal email address)

- `Use sha512`

- `User not found`

- `User hasn't been verified`

- `Failed` (the `response` given does not match the hashed password in database)

- `Unexpected error`

The user is successfully logged into the account only when the responded status is `success`.