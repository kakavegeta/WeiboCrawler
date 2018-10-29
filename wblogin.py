import base64
import requests
import binascii
import json
import re
import rsa
import random
from ZLogger import Logger
from config import headers, agents, accounts

json_pattern = re.compile(r'\(({.*})\)')


def EncodeUsername(username):
    return base64.b64encode(bytes(username, encoding='utf-8'))

def EncodePassword(password, pubkey, servertime, nonce):
    rsaPubkey = int(pubkey, base=16)
    rsakey = rsa.PublicKey(rsaPubkey, int('10001', base=16))
    string = str(servertime) + "\t" + str(nonce) + "\n" + str(password)
    pwd = rsa.encrypt(bytes(string, encoding='utf-8'), rsakey)
    return binascii.b2a_hex(pwd)

def PreLoginData(username):
    su = EncodeUsername(username)
    url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)'.format(su)
    r = requests.get(url)
    data = json.loads(json_pattern.findall(r.text)[0])
    servertime = data['servertime']
    nonce = data['nonce']
    pubkey = data['pubkey']
    rsakv = data['rsakv']
    return su, servertime, nonce, pubkey, rsakv

def PostData(username, passwd, pubkey, servertime, nonce, rsakv):
    su = EncodeUsername(username)
    sp = EncodePassword(passwd,pubkey,servertime,nonce)    
    data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate':'7',
        'qrcode_flag':'false',
        'useticket':'1',
        'pagerefer':'',
        'vsnf': '1',
        'su': su,
        'service': 'miniblog', 
        'servertime': '1540701654',
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': sp,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '243',
        'cdult':'2',
        'returntype': 'TEXT' 
            }
    return data

class Client:

    def __init__(self, username='zhangjie@elements.org.cn', passwd = 'zhangjie123456'):
        self.username = username
        self.passwd = passwd
        self.su = None
        self.nonce = None
        self.pubkey = None
        self.servertime = None
        self.rsakv = None
        self.session = None
        self.headers = headers
        self.state = False # status of current client, False: not login; True: login
        self.logger = Logger('weibospider.log')
    
    def _prelogin(self):
        self.su, self.servertime, self.nonce, self.pubkey, self.rsakv = PreLoginData(self.username)
        

    @property
    def sp(self):
        return EncodePassword(self.passwd,self.pubkey,self.servertime,self.nonce)
    
    @property
    def postdata(self):
        return PostData(self.username,self.passwd,self.pubkey,self.servertime,self.nonce,self.rsakv)

    #there you can change account 
    def login(self, username=None, passwd=None):
        self.state = False
        if username:
            self.username = username
        if passwd:
            self.passwd = passwd
        self._prelogin()
        url_login = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        postdata = self.postdata
        session = requests.Session()

        #agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
        #headers = {'User-Agent': agent, 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '529', 'Content-Type': 'application/x-www-form-urlencoded'}
        r = session.post(url_login, data=postdata, headers=self.headers)
        #print(r.request.headers)
        c = r.content.decode('gbk')
        #print(c)
        info = json.loads(c)
        try:
            if info['retcode'] == '0':
                self.logger.info('Login succeed')
                self.state = True
                # get the cookie and 
                cookies = session.cookies.get_dict()
                #print(cookies)
                cookies = [key+'='+value for key, value in cookies.items()]
                cookies = ";".join(cookies)
                session.headers['Cookie'] = cookies
            else:
                self.logger.info('Login failed')
        except Exception as e:
            self.logger.error(e)
        self.session = session
        return session

    def SwitchAgent(self):
        agent = random.choice(agents)
        self.headers['User-Agent'] = agent
        

    def SwitchAccount(self):
        login = 0
        while not login:
            self.SwitchAgent()
            self.logger.info('switch to agent: {}'.format(self.headers['User-Agent']))
            account = random.choice(accounts)
            username = account.split('/')[0]
            password = account.split('/')[1]
            self.logger.info('switch to account: {}'.format(username))
            session = self.login(username=username, passwd=password)
            if not self.state:
                self.logger.info('login failed, continue')
                continue
            login = 1
        self.session = session
        return session
    
            


def main():
    client = Client()
    client.login()
if __name__ == '__main__':
    main()