#! /usr/bin/python3

#Realtime ADIF uploaded for JS8Call
#By Mark - M0IAX
#http://m0iax.com/findme


from tkinter import *
import settings
from tkinter import Frame
import udpServer
import UploadADIF

WIDTH=270
HEIGHT=100
appName="ADIF Uploader for JS8Call"

class UI(Tk):
    def loadSettings(self, settingValues):
        print('Loading settings')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
            print("Main Window is closing, call any function you'd like here!")

    def __enter__(self):
      
        print('Starting')
    def ask_quit(self):
        if self.upLoader!=None:
            print('Shutting down ADIF Listener')
            self.upLoader.setListen(False)
            self.upLoader.join()
        if self.udpserver!=None:
            print('Shutting down UDP Server')
            self.udpserver.close()
            
        print('Exiting. Thanks for using '+appName+' By M0IAX')
        
        self.destroy() 
    def updateeQSL(self):
        if self.upLoader!=None:
            enabled=self.upLoader.toggleEQSL()
            self.configureEQSLButton(enabled)
        if self.uploadADIF!=None:
            enabled=self.uploadADIF.toggleEQSL()
            self.configureEQSLButton(enabled)
            
    def updateQRZ(self):
        if self.upLoader!=None:
            enabled=self.upLoader.toggleQRZ()
            self.configureQRZButton(enabled)
        if self.uploadADIF!=None:
            enabled=self.uploadADIF.toggleQRZ()
            self.configureQRZButton(enabled)
            
    def configureQRZButton(self, enable):
        if enable:
            self.enableQRZButton.configure(bg="green")
            self.enableQRZButton.configure(text="QRZ Upload Enabled")
            
        else:
            self.enableQRZButton.configure(bg="red")
            self.enableQRZButton.configure(text="QRZ Upload Disabled")
            

    def configureEQSLButton(self, enable):
        if enable:
            self.enableQSLButton.configure(bg="green")
            self.enableQSLButton.configure(text="eQSL Upload Enabled")
            
        else:
            self.enableQSLButton.configure(bg="red")
            self.enableQSLButton.configure(text="eQSL Upload Disabled")
                
    def show_buttons(self, frame, controller):


        self.enableQRZButton=Button(frame,text='QRZ Upload Disabled', bg="red", command=self.updateQRZ)
        self.enableQRZButton.grid(row=0, column=0, padx=5, pady=5)
        
        
        self.enableQSLButton=Button(frame,text='Enable eQSL Upload', bg="red", command=self.updateeQSL)
        self.enableQSLButton.grid(row=1, column=0, padx=5, pady=5)
        
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
    
        self.settingValues = settings.Settings()
        self.loadSettings(self.settingValues)
        
        self.upLoader=None
        #self.upLoader = adifListener.UploadServer()
        #self.upLoader.daemon = True
        #self.upLoader.start()
        
        self.uploadADIF = UploadADIF.UploadServer()
        
        self.udpserver = udpServer.Server(self.uploadADIF)
        self.udpserver.daemon = True
        self.udpserver.start()
        
        self.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.title(appName+" by M0IAX")
        
        buttonFrame=Frame(self)
        buttonFrame.pack()
        
        self.show_buttons(buttonFrame, self)
        
        if self.upLoader!=None:
            self.configureEQSLButton(self.upLoader.getEQSLEnabled())
            self.configureQRZButton(self.upLoader.getQRZEnabled())
        if self.uploadADIF!=None:
            self.configureEQSLButton(self.uploadADIF.getEQSLEnabled())
            self.configureQRZButton(self.uploadADIF.getQRZEnabled())
        

if __name__=="__main__":
    
    try:

        app = UI()
        app.protocol("WM_DELETE_WINDOW", app.ask_quit)
        app.mainloop()
        
    finally:
        print('Finally Quit')
    # if app.gpsl!=None:
    #     app.gpsl.setReadGPS(False)
    #     app.gpsl.join()
    
    
    