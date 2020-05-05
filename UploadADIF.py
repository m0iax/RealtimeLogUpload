#! /usr/bin/python3

#Realtime ADIF uploaded for JS8Call
#By Mark - M0IAX
#http://m0iax.com/findme

import threading
from socket import socket, AF_INET, SOCK_DGRAM
import requests
import json
import time
import configparser
import os
import sys
import errno
from time import sleep
import urllib3


def createConfigFile(configFileName):
    #cretes the config file if it does not exist
    if not os.path.isfile(configFileName):
            
        config = configparser.ConfigParser()
                            
        config['QRZ.COM'] = {'apikey': 'APIKEY'
                            }  
        config['EQSL.CC'] = {'username': 'USERNAME',
                             'password': 'PASSWORD'
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

   
    qrzAPIKey= config.get('QRZ.COM', 'apikey')
    
    eqsluser= config.get('EQSL.CC', 'username')
    eqslpassword= config.get('EQSL.CC', 'password')
    
    qrz=int(config.get('SERVICES','qrz'))
    qrzEnabled=False
    if qrz==1:
        qrzEnabled=True
    
    eqsl=int(config.get('SERVICES','eqsl'))
    eqslEnabled=False
    if eqsl==1:
        eqslEnabled=True
    

class UploadServer(threading.Thread):
    messageType='';
    messageText=''
    pttCount=0
    
    def toggleEQSL(self):
        self.eqslEnabled = not self.eqslEnabled
        return self.eqslEnabled
    def toggleQRZ(self):
        self.qrzEnabled = not self.qrzEnabled
        return self.qrzEnabled
    def getQRZEnabled(self):
        return self.qrzEnabled
    def getEQSLEnabled(self):
        return self.eqslEnabled
    
    def setQRZEnabled(self, enabled):
        self.qrzEnabled=enabled
    def setEQSLEnabled(self, enabled):
        self.eqslEnabled=enabled
    def setQRZAPIKey(self, apikey):
        self.qrzAPIKey=apikey
        
    def __init__(self):
        t = threading.Thread.__init__(self)
        
        #we can ignore the ssl warnings as the two domains we are uploading to are secure
        urllib3.disable_warnings()
        self.showdebug=False
        self.listening = True
       
        self.qrzEnabled=qrzEnabled
        self.eqslEnabled=eqslEnabled
        
        self.qrzAPIKey = qrzAPIKey
        self.eqslUser = eqsluser
        self.eqslPassword = eqslpassword
        
        self.first = False
        self.messageText=None
        self.messageType=None
        self.pttCount = 0
        
    def processMessage(self,value):
        if self.qrzEnabled:
            self.uploadToQRZ(value)
        if self.eqslEnabled:
            self.uploadToEQSL(value)
        if not self.qrzEnabled and not self.eqslEnabled:
            print ('No ADIF upload enabled. ADIF not uploaded.')
    
    def sendToQRZ(self, urlString):
      
        self._session = requests.Session()
        self._session.verify = False
        r = self._session.get(urlString)
        if r.status_code == 200:
            if self.showdebug:
                print(r)
                print('rtext '+r.text)
            if "STATUS=FAIL" in r.text:
                print("Failed to upload to QRZ.com returned status is: ")
                print(r.text)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to QRZ")    

    def sendToEQSL(self, urlString):
          
        self._session = requests.Session()
        r = self._session.get(urlString, verify=False)
        if r.status_code == 200:
            if self.showdebug:
                print(r)
                print(r.text)
            
            if "Result: 1 out of 1" not in r.text:
                print("Failed to upload to eQSL.cc returned status is: ")
                print(r.text)
                
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to eQSL")    
        
    def uploadToEQSL(self, adifEntry):
        print('Uploading to eQSL.cc')
        url='https://eQSL.cc/qslcard/importADIF.cfm?ADIFData={0}&EQSL_USER={1}&EQSL_PSWD={2}'
        url=url.format(adifEntry,self.eqslUser,self.eqslPassword)
        
        if self.showdebug:
            print('eqsl '+url)
        self.sendToEQSL(url)
        
    def uploadToQRZ(self, logEntry):
        print('Uploading to QRZ.com')
        url = ' https://logbook.qrz.com/api'
        url = url+'?KEY={0}&'
        url = url+'ACTION=INSERT&ADIF={1}'
        url = url.format(self.qrzAPIKey, logEntry)
        
        if self.showdebug:
            print(url)
        self.sendToQRZ(url)
        
    def setListen(self, listen):
        self.listening=listen
            
    def close(self):
        self.listening = False

if __name__ == "__main__":
    
    server = UploadServer()
    

