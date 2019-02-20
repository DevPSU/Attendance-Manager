from random import choice
from string import ascii_letters,digits

rand32=lambda :"".join([choice(ascii_letters+digits) for i in range(32)])

DBHOST=""
DBUSER=""
DBPASSWORD=""
DBNAME=""