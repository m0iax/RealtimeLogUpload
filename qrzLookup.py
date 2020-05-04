import threading

#from __future__ import print_function

from socket import socket, AF_INET, SOCK_DGRAM
import requests
import json
import time
import configparser
import os
#import configAndSettings

def createConfigFile(configFileName):
    #cretes the config file if it does not exist
    if not os.path.isfile(configFileName):
            
        config = configparser.ConfigParser()
        config['NETWORK'] = {'serverip': '127.0.0.1',
                             'serverport': 2333
                            }
        config['QRZ.COM'] = {'apikey': 'F1A5-5FF9-6A7F-56AE'
                            }  
        config['EQSL.CC'] = {'username': 'username',
                             'password': 'password'
                            }  
        config['SERVICES'] = {'eqsl': 0,
                             'qrz': 0
                            }  
        
        with open(configFileName, 'w') as configfile:
            config.write(configfile)
            configfile.close()
    

configfilename="./loguploader.cfg"
createConfigFile(configfilename)

if os.path.isfile(configfilename):
    config = configparser.ConfigParser()
    config.read(configfilename)

    serverip = config.get('NETWORK','serverip')
    serverport = int(config.get('NETWORK', 'serverport'))

    qrzAPIKey= config.get('QRZ.COM', 'apikey')
    
    qrz=int(config.get('SERVICES','qrz'))
    qrzEnabled=False
    if qrz==1:
        qrzEnabled=True
    
    eqsl=int(config.get('SERVICES','eqsl'))
    eqslEnabled=False
    if eqsl==1:
        eqslEnabled=True
    
listen = (serverip, serverport)

class UploadServer(threading.Thread):
    messageType='';
    messageText=''
    pttCount=0
    
    def setQRZEnabled(self, enabled):
        self.qrzEnabled=enabled
    def setEQSLEnabled(self, enabled):
        self.eqslEnabled=enabled
    def setQRZAPIKey(self, apikey):
        self.qrzAPIKey=apikey
        
    def __init__(self):
        t = threading.Thread.__init__(self)
        
        self.qrzEnabled=qrzEnabled
        self.eqslEnabled=eqslEnabled
        
        self.qrzAPIKey = qrzAPIKey
        self.first = False
        self.messageText=None
        self.messageType=None
        self.pttCount = 0
        
        #self.apikey='meh'

    def get_qrz_session(self, urlString):
      
        self._session = requests.Session()
        self._session.verify = False
        r = self._session.get(urlString)
        if r.status_code == 200:
            print(r)
            print(r.text)
            #raw_session = xmltodict.parse(r.content)
            #self._session_key = raw_session['QRZDatabase']['Session']['Key']
            #if self._session_key:
            return True
        
        print('Response: '+r)
        raise Exception("Could not get QRZ session")    

    def get_eqsl_session(self, urlString):
          
        self._session = requests.Session()
        self._session.verify = False
        r = self._session.get(urlString)
        if r.status_code == 200:
            print(r)
            print(r.text)
            #raw_session = xmltodict.parse(r.content)
            #self._session_key = raw_session['QRZDatabase']['Session']['Key']
            #if self._session_key:
            return True
        
        print('Response: '+r)
        raise Exception("Could not get QRZ session")    
        
    def uploadToEQSL(self, adifEntry):
        url='https://www.eQSL.cc/qslcard/importADIF.cfm?ADIFData={0}'
        url=url+'&EQSL_USER={1}&EQSL_PSWD={2}'
        url=url.format(adifEntry,self.eqslUser,self.eqslPassword)
        
        print('eqsl '+url)
        self.get_eqsl_session(url)
        
    def uploadToQRZ(self, logEntry):
        print('Uploading to QRZ.com')
       # url = '''https://xmldata.qrz.com/xml/current/?username={0}&password={1}'''.format(username, password)
        url = ' http://logbook.qrz.com/api'
        url = url+'?KEY={0}&'
        url = url+'ACTION=INSERT&ADIF={1}'
        url = url.format(self.qrzAPIKey, logEntry.decode())
        
        print(url)
        self.get_qrz_session(url)
        
    
    def run(self):
        print('listening on', ':'.join(map(str, listen)))
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(listen)
        self.listening = True
        try:
            while self.listening:
                content, addr = self.sock.recvfrom(65500)
               
                print('incoming ADIF:', ':'.join(map(str, addr)))
                
                #print(content.decode())
                
                if self.qrzEnabled:
                    self.uploadToQRZ(content)
                if self.eqslEnabled:
                    self.uploadToEQSL(content)

        finally:
            self.sock.close()

    def close(self):
        self.listening = False


if __name__ == "__main__":
    
    server = UploadServer()
    server.start()
    

