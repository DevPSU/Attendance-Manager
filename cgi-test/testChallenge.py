import requests as rq

login=""

r=rq.post("https://devpsu.whmhammer.com/cgi/challenge.py",{"login":login})

print(r.text)