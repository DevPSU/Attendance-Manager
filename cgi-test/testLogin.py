import requests as rq
from hashlib import sha512

login=""
password=""
salt=""
challenge=""

s0=bytes(salt+password,"ascii")
h0=sha512(s0)
s1=bytes(challenge+h0.hexdigest(),"ascii")
h1=sha512(s1)

data={
    "login":login,
    "hash":h1.hexdigest()
}

r=rq.post("https://devpsu.whmhammer.com/cgi/login.py",data)

print(r.text)