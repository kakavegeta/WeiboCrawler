import requests
import redis
import time
import os
from bs4 import BeautifulSoup
from wblogin import Client
import pandas as pd
import csv

def main():
    client = Client()
    client.login()
    for i in range(1,1000):
        client.logger.info('now in page {}'.format(i))
        params = 'page={}'.format(i)
        data = None
        while not data:
            client.logger.info('get data from page {}......'.format(i))
            data = client.GetUserTweets(uid=2208751963,params=params)
        client.logger.info('get data done!')
        try:
            SaveData(data, 'output/res.csv')
        except:
            client.logger.error('write file error')
            pass
        
    
def SaveData(data, path, mode = 'a'):
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
    with open(path, mode, newline='') as f:
        fcsv = csv.writer(f)
        try:
            fcsv.writerows(data)
        except:
            print('write file error')

if __name__=='__main__':
   main() 