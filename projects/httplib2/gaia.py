import httplib2 
import random
import threading
from urllib import urlencode

def test():
    h = httplib2.Http()
    for i in range(10):
        h.clear_credentials()
        passwd = "".join([chr(random.randint(0, 20)+ord('a')) for j in range(20)]) 
        auth = dict(Email="joe.gregorio@gmail.com", Passwd=passwd, service="blogger", source="Testing-ForCaptcha-01")
        print h.request("https://www.google.com/accounts/ClientLogin", method="POST", body=urlencode(auth), headers={'Content-Type': 'application/x-www-form-urlencoded'})
    auth = dict(Email="joe.gregorio@gmail.com", Passwd="jcg@q4q4", service="blogger", source="Testing-ForCaptcha-01")
    print h.request("https://www.google.com/accounts/ClientLogin", method="POST", body=urlencode(auth), headers={'Content-Type': 'application/x-www-form-urlencoded'})


for i in range(20):
    t = threading.Thread(target=test)
    t.start()

