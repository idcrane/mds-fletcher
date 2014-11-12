import os

WTF_CSRF_ENABLED = True

home = os.environ['HOME']
with open(home + '/metis/secure/csrf_key_1.password') as infile:
    SECRET_KEY = infile.read()

