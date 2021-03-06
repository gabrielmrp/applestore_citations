# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:24:11 2021

@author: gabri
"""

from datetime import date, timedelta
import time
import json
import operator
import base64 
import requests
import twitter
import re
 
#Carrega as Credenciais

with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
    
    
#Autorização oAuth1.0

twitter = twitter.Twitter(auth = twitter.OAuth(
                  creds['ACCESS_TOKEN'],
                  creds['ACCESS_SECRET'],
                  creds['CONSUMER_KEY'],
                  creds['CONSUMER_SECRET'])
                  )

#Autorização oAuth2.0


key_secret = '{}:{}'.format( creds['CONSUMER_KEY'], creds['CONSUMER_SECRET']).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')
 

base_url = 'https://api.twitter.com/'
 
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
  
search_headers = {
    'Authorization': 'Bearer {}'.format(creds['BEARER_TOKEN'])    
}


#Captura das Citações pela API do Twitter

def get_citations(all_track_names):
     
    track_usernames = {}
    for track_name in all_track_names: 
        
        results = twitter.users.search(q = re.split('-|–',
                                       track_name)[0]. #excluí informações desnecessárias                                        
                                       replace('Music','') #caso específico do Spotify 
                                       )
        
        #coleta o nome do usuário e  o número de seguidores
        users = dict()
        for user in results:
           users[user["screen_name"]]=user["followers_count"]    
           
        #escolhe o nome do usuário com maior número de seguidores.
        track_usernames[track_name]=max(users.items(), key=operator.itemgetter(1))[0]
     
    
    citations = {}    
    yesterday = date.today()- timedelta(1)
    one_day_before_yesterday = date.today()-  timedelta(2)
    search_url = '{}1.1/search/tweets.json'.format(base_url)
    period_request_sleep = 1.01
        
    
    for name,username in track_usernames.items():
        
        #parâmetros para busca
        search_params = {
            'q': "@"+username,
            'result_type': 'recent',
            'count': 100,
            'since': one_day_before_yesterday,
            'until':yesterday
        }          
        
        i=0
        count_citation = 0
        count=0 
        
        while count==0 or count==100:  
            #faz o request para a api
            search_resp = requests.get(search_url, headers=search_headers, params=search_params)
            tweet_data = search_resp.json()
            
            #incrementa a contagem
            count = tweet_data['search_metadata']['count']
            count_citation += len(tweet_data['statuses'])
            
            #evitar atingir o limite da api
            time.sleep(period_request_sleep)
            i+=1
            
            #define a próxima página de busca de resultados
            if('next_results' in tweet_data['search_metadata']):
                search_params['max_id']= tweet_data['search_metadata']['next_results'].split('&')[0].replace('?max_id=','')
                print([name,i, tweet_data['statuses'][0]['created_at'] ])
            else:
                print([name,i, 'last' ])   
                break;
            
        citations[name]=count_citation        
    return citations

 