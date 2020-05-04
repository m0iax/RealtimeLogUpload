import threading

#from __future__ import print_function

from socket import socket, AF_INET, SOCK_DGRAM

import json
import time
import configparser
import os
import configAndSettings
import UploadADIF

def createConfigFile(configFileName):
    #cretes the config file if it does not exist
    if not os.path.isfile(configFileName):
            
        config = configparser.ConfigParser()
        config['NETWORK'] = {'serverip': '127.0.0.1',
                             'serverport': 2242
                            }
            
        with open(configFileName, 'w') as configfile:
            config.write(configfile)
            configfile.close()
    

configfilename="./js8call.cfg"
createConfigFile(configfilename)

if os.path.isfile(configfilename):
    config = configparser.ConfigParser()
    config.read(configfilename)

    serverip = config.get('NETWORK','serverip')
    serverport = int(config.get('NETWORK', 'serverport'))

listen = (serverip, serverport)


def from_message(content):
    try:
        return json.loads(content)
    except ValueError:
        return {}


def to_message(typ, value='', params=None):
    if params is None:
        params = {}
    return json.dumps({'type': typ, 'value': value, 'params': params})


class Server(threading.Thread):
    messageType='';
    messageText=''
    pttCount=0
    
    def __init__(self, uploadadif):
        t = threading.Thread.__init__(self)
        
        if uploadadif==None:
            self.uploadADIF = UploadADIF.UploadServer()
        else:
            self.uploadADIF = uploadadif 
               
        self.showoutput = False
        self.showLogOutput = True
        self.first = False
        self.messageText=None
        self.messageType=None
        self.pttCount = 0
        
    def setMessage(self, mType, mText):
        self.messageText=mText
        self.messageType=mType
        
    def process(self, message):
        typ = message.get('type', '')
        value = message.get('value', '')
        params = message.get('params', {})
        
            
        if self.messageType!=None:
            self.send(self.messageType, self.messageText)
            self.messageText=None
            self.messageType=None
            
        if not typ:
            return

        if typ == 'LOG.QSO':
            value = value+' <eor>'
            
            if self.showLogOutput:
                print('===========logging========= ')
                print(value)
                self.uploadADIF.processMessage(value)
                print('=========================== ')
            
        if self.showoutput:
            print('->', typ)
    
            if value:
                print('-> value', value)

            if params:
                print('-> params: ', params)

        if typ == 'RIG.PTT':
            if value == 'on':
                self.pttCount = self.pttCount+1
                print("PTT COUNT=====",self.pttCount)

        elif typ == 'CLOSE':
            self.close()

    def send(self, *args, **kwargs):
        params = kwargs.get('params', {})
        if '_ID' not in params:
            params['_ID'] = int(time.time()*1000)
            kwargs['params'] = params
        message = to_message(*args, **kwargs)
        print('outgoing message:', message)
        self.sock.sendto(message.encode(), self.reply_to)
    
    def run(self):
        print('listening on', ':'.join(map(str, listen)))
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(listen)
        self.listening = True
        try:
            while self.listening:
                content, addr = self.sock.recvfrom(65500)
                
                #'print('incoming message:', ':'.join(map(str, addr)))
                if self.showoutput:
                    print(content)
                
                try:
                    message = json.loads(content)
                    if self.showoutput:
                        print('got message '+message)
                except ValueError:
                    message = {}

                if not message:
                    continue

                self.reply_to = addr
                self.process(message)

        finally:
            self.sock.close()

    def close(self):
        self.listening = False


if __name__ == "__main__":
    #def main():
    server = Server(None)
    #server.uploadADIF.toggleEQSL()
    server.start()
    #s.listen()

