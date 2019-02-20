import requests as rq
from hashlib import sha512
from random import choice
from string import ascii_letters,digits

rand32=lambda :"".join([choice(ascii_letters+digits) for i in range(32)])

username=""
password=""
email=""
surname=""
familyname=""

salt=rand32()
s=bytes(salt+password,"ascii")
h=sha512(s)

data={
    "username":username,
    "salt":salt,
    "hash":h.hexdigest(),
    "email":email,
    "surname":surname,
    "familyname":familyname
}

r=rq.post("https://devpsu.whmhammer.com/cgi/register.py",data)

print(r.text)