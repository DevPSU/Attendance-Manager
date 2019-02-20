import requests as rq
from hashlib import sha512

login=""
password=""
challenge=""
salt=""

s0=bytes(salt+password,"ascii")
h0=sha512(s)
s1=bytes(challenge+h0.hexdigest(),"ascii")
h1=sha512(s1)

data={
    "login":login,
    "hash":h1.hexdigest()
}

r=rq.get("https://devpsu.whmhammer.com/cgi/verify.py",data)

print(r.text)