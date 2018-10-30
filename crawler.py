import requests
import redis

from bs4 import BeautifulSoup
from wblogin import Client

def main():
    client = Client()
    client.login()
    data = client.GetUserTweets(uid=2208751963,params='page=1')
    print(data)


if __name__=='__main__':
    main()