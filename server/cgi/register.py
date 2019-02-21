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
        username=form["username"].value
        salt=form["salt"].value
        password_hash=form["hash"].value
        email=form["email"].value
        surname=form.getvalue("surname")
        givenname=form.getvalue("givenname")
    except KeyError:
        print("Status: 400")
        print()
        print("Missing parameter")
        exit()

    if not username.isalnum() or len(username)>64:
        print("Status: 400")
        print()
        print("Illegal username")
        exit()

    if not salt.isalnum() and len(salt)==32:
            print("Status: 400")
            print()
            print("Use 32-digit alnum salt")
            exit()

    if not password_hash.isalnum() and len(password_hash)==128:
        print("Status: 400")
        print()
        print("Use sha512")
        exit()

    if "@" not in email or len(email)>54:
        print("Status: 400")
        print()
        print("Illegal email address")
        exit()

    if len(surname)>32 or len(familyname)>32:
        print("Status: 400")
        print()
        print("True name too long")
        exit()

    conn=sql.connect(DBHOST,DBUSER,DBPASSWORD,DBNAME)
    cur=conn.cursor()

    try:
        cur.execute("insert into users(email) values(%s);",(email,))
    except sql.IntegrityError:
        conn.close()
        print("Status: 400")
        print()
        print("Email address already been registered")
        exit()

    try:
        cur.execute("update users set username=%s where email=%s;",(username,email))
    except sql.IntegrityError:
        conn.close()
        print("Status: 400")
        print()
        print("Username already been registered")
        exit()

    challenge=rand32()
    cur.execute("update users set password_hash=%s,salt=%s,challenge=%s,surname=%s,familyname=%s where email=%s;",(password_hash,salt,challenge,email,surname,familyname))

    #email user the salt and challenge using smtplib

    conn.commit()
    conn.close()

    print()
    print("Success")
    #to be deleted:
    print(salt)
    print(challenge)
except Exception as e:
    print("Status: 500")
    print()
    print("Unexpected error")
    print(repr(e))