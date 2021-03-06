# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:35:37 2021

@author: gabri
"""

import json

def generate():

    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] = 'WeAlUXYEFGd5ATynALI0FNXDF'
    credentials['CONSUMER_SECRET'] = 'n1J0RxRqKXSfhZZ4vNRsoj8Nm5ZYJY4x6gNJlKPUXUvJP4nPWY'
    credentials['ACCESS_TOKEN'] = '112542768-IqLxg5pPmT9hIcGVbfErYLh7vsSgtOmMTP3qXQlN'
    credentials['ACCESS_SECRET'] = '8LvnhZr4FaFq8DLbmM0kWt5dmaFiu5rDMnpXqCrPD9Dxv'
    credentials['BEARER_TOKEN'] = "AAAAAAAAAAAAAAAAAAAAAPs8NQEAAAAAFUyGELvdGCHBg9ApKM6pZwPy6Ss%3DjfGpRdGSxX94qLHzsjZnosmNSiHuZsi8pmIUywMAvNbVFg9CMZ"
     
    # Save the credentials object to file
    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)
    print("Credenciais Geradas")
    
     