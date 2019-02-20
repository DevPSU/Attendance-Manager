# Documenmtation for verification API

---

## Introduction

This documentation explains how to verify a registration. The API is based on HTTP. The front end should ask the user for username or email address, password, and the "challenge" sent to user by email.

---

## Request

The request should be sent to [https://devpsu.whmhammer.com/cgi/verify.py](https://devpsu.whmhammer.com/cgi/verify.py) using **GET** method with the following parameters:

### `login` (REQUIRED)

The username **or** the email address of the account.

### `response` (REQUIRED)

The 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "challenge" (sent to user by email) and the 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "salt" (sent to user by email) and the raw password.

---

## Response

The response is always in `text/plain`.

The first line indicates the status of the registration. Here is a list of possible outcomes (case sensitive):

- `Success`

- `Use GET method`

- `Missing parameter`

- `Illegal login` (the `login` given is neither a legal username nor a legal email address)

- `Use sha512`

- `Failed` (the `response` given does not match the hashed password in database)

- `Unexpected error`

The account status is changed in the database only when the responded status is `success`. In this case, the user should be able to log into the account. Read `login.md` for more information about logging in.