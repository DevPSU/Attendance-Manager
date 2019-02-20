#!/usr/bin/python3
import cgi
import MySQLdb as sql
from os import environ

from whl import *

try:
    print("Content-Type: text/plain")

    if environ.get("REQUEST_METHOD")!="POST":
        print("Status: 405")
        print("Allow: POST")
        print()
        print("Use POST method")
        exit()

    form=cgi.FieldStorage()
    try:
        login=form["login"].value
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

    conn=sql.connect(DBHOST,DBUSER,DBPASSWORD,DBNAME)
    cur=conn.cursor()

    if "@" in login:
        cur.execute("select salt,last_login_time,challenge from users where email=%s;",(login,))
    else:
        cur.execute("select salt,last_login_time,challenge from users where username=%s;",(login,))
    try:
        salt,last_login_time,challenge=cur.fetchone()
    except TypeError:
        conn.close()
        print("Status: 404")
        print()
        print("User not found")
        exit()

    if last_login_time==0:
        conn.close()
        print("Status: 403")
        print()
        print("User hasn't been verified")
        exit()

    challenge=rand32()

    if "@" in login:
        cur.execute("update users set challenge=%s where email=%s;",(challenge,login))
    else:
        cur.execute("update users set challenge=%s where username=%s;",(challenge,login))

    conn.commit()
    conn.close()

    print()
    print("Success")
    print(salt)
    print(challenge)
except Exception as e:
    print("Status: 500")
    print()
    print("Unexpected error")
    print(repr(e))