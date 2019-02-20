#!/usr/bin/python3
import cgi
import MySQLdb as sql
from hashlib import sha512
from os import environ
from time import time

from whl import *

try:
    print("Content-Type: text/plain")

    if environ.get("REQUEST_METHOD")!="GET":
        print("Status: 405")
        print("Allow: GET")
        print()
        print("Use GET method")
        exit()

    form=cgi.FieldStorage()
    try:
        login=form["login"].value
        response=form["hash"].value
    except KeyError:
        print("Status: 400")
        print()
        print("Missing parameter")
        exit()

    if not login.isalnum() and "@" not in login:
        print("Status: 400")
        print()
        print("Illegal login")
        exit()

    if not response.isalnum() and len(response)==128:
        print("Status: 400")
        print()
        print("Use sha512")
        exit()

    conn=sql.connect(DBHOST,DBUSER,DBPASSWORD,DBNAME)
    cur=conn.cursor()

    if "@" in login:
        cur.execute("select password_hash,last_login_time,challenge from users where email=%s;",(login,))
    else:
        cur.execute("select password_hash,last_login_time,challenge from users where username=%s;",(login,))
    try:
        password_hash,last_login_time,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        print("User not found")
        exit()

    if last_login_time!=0:
        conn.close()
        print("Status: 403")
        print()
        print("User already been verified")
        exit()

    s=bytes(challenge+password_hash,"ascii")
    h=sha512(s)

    if response!=h.hexdigest():
        conn.close()
        print("Status: 403")
        print()
        print("Failed")
        exit()

    if "@" in login:
        cur.execute("update users set last_login_time=%s,challenge=%s where email=%s;",(int(time()),rand32(),login))
    else:
        cur.execute("update users set last_login_time=%s,challenge=%s where username=%s;",(int(time()),rand32(),login))

    conn.commit()
    conn.close()

    print()
    print("Success")
except Exception as e:
    print("Status: 500")
    print()
    print("Unexpected error")
    print(repr(e))