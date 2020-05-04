#! /usr/bin/python3

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
        #print('QSL ',self.eqslEnabled)
        self.eqslEnabled = not self.eqslEnabled
        #print('QSL Now',self.eqslEnabled)
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
        
        self.listen = (serverip, serverport)

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
        
        print('listening on', ':'.join(map(str, self.listen)))

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(self.listen)
        self.sock.setblocking(False)

    def sendToQRZ(self, urlString):
      
        self._session = requests.Session()
        self._session.verify = False
        r = self._session.get(urlString)
        if r.status_code == 200:
            print(r)
            print(r.text)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to QRZ")    

    def sendToEQSL(self, urlString):
          
        self._session = requests.Session()
       # self._session.verify = False
        r = self._session.get(urlString, verify=False)
       # r = requests.get(urlString, verify=False)
        if r.status_code == 200:
            print(r)
            print(r.text)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to eQSL")    
        
    def uploadToEQSL(self, adifEntry):
        print('Uploading to eQSL.cc')
        url='https://eQSL.cc/qslcard/importADIF.cfm?ADIFData={0}&EQSL_USER={1}&EQSL_PSWD={2}'
        #url=url+'&EQSL_USER={1}&EQSL_PSWD={2}'
        url=url.format(adifEntry,self.eqslUser,self.eqslPassword)
        
        print('eqsl '+url)
        self.sendToEQSL(url)
        
    def uploadToQRZ(self, logEntry):
        print('Uploading to QRZ.com')
        url = ' https://logbook.qrz.com/api'
        url = url+'?KEY={0}&'
        url = url+'ACTION=INSERT&ADIF={1}'
        url = url.format(self.qrzAPIKey, logEntry.decode())
        
        print(url)
        self.sendToQRZ(url)
    def setListen(self, listen):
        self.listening=listen
        #if self.listening==False:
        #    if self.sock!=None:
        #        self.sock.close()
    def run(self):
        try:
            try:
                while self.listening:
                    if self.sock!=None:
                        try:
                            content, addr = self.sock.recvfrom(65500)
                            #content, addr = self.sock.listen(5)
                        except Exception as e:
                            err = e.args[0]
                            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                                sleep(1)
                                #print('No data available')
                                continue
                            else:
                                # a "real" error occurred
                                print (e)
                                sys.exit(1)
                    if content!=None and addr!=None:
                        print('Detected ADIF from JS8Call:', ':'.join(map(str, addr)))
                    
                        if self.qrzEnabled:
                            self.uploadToQRZ(content)
                        if self.eqslEnabled:
                            self.uploadToEQSL(content)
                        if not self.qrzEnabled and not self.eqslEnabled:
                            print ('No ADIF upload enabled. ADIF not uploaded.')
                
            finally:
                self.sock.close()
                #self.join()
        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print ("\nKilling Thread...")
            self.listening = False
            self.join() # wait for the thread to finish what it's doing
            print ("Done.\nExiting.")
            
    def close(self):
        self.listening = False


if __name__ == "__main__":
    
    server = UploadServer()
    server.start()
    

