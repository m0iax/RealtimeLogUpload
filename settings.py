import configparser
import os
import sys

configfilename=sys.path[0]+"/utils.cfg"

class Settings():
    def getSettingValue(self, section, settingName):
        settingValue=""

        settingValue=self.config.get(section, settingName)
    
        return settingValue
    def saveConfigFile(self,
                       serverip,serverport,
                       autotimeperiod,
                       autoonatstart,
                       autoselected,
                       precision,
                       gpscomport,
                       gpsportspeed,
                       gpsoption,
                       showdebug):
            
        config = configparser.ConfigParser()
        config['NETWORK'] = {'serverip': serverip,
                                'serverport': int(serverport)}
        config['APP'] = {'autotimeperiod': int(autotimeperiod),
                        'autoonatstart':int(autoonatstart),
                        'autoselectedoption':int(autoselected),
                        'precision': int(precision)
                        }
        config['GPSHARDWARE'] = {'gpscomport': gpscomport,
                                'gpsportspeed': gpsportspeed,
                                'option': gpsoption,
                                }
        config['DEBUG'] = {'showoutput': int(showdebug) }
        
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
            configfile.close()
        
        return config
    
    def createConfigFile(self,configFileName):
        #creates the config file if it does not exist
        if not os.path.isfile(configFileName):
            
            config = configparser.ConfigParser()
            config['NETWORK'] = {'serverip': '127.0.0.1',
                                 'serverport': 2242}
            config['APP'] = {'autotimeperiod': 10,
                            'autoonatstart':0,
                            'autoselectedoption':0,
                            'precision': 4
                            }
            config['GPSHARDWARE'] = {'gpscomport': 'COM15',
                                    'gpsportspeed': '9600',
                                    'option': 'None',
                                    }
            config['DEBUG'] = {'showoutput': 0 }
           
            with open(configFileName, 'w') as configfile:
                config.write(configfile)
                configfile.close()
        
        return config
    
    def __init__(self, *args, **kwargs):
        
        self.config=None
        self.config = self.loadconfig()
    
    def getNetworkSettingValue(self, settingName):
        return self.getSettingValue('NETWORK', settingName)
    def getAppSettingValue(self, settingName):
        return self.getSettingValue('APP', settingName)
    def getGPSHardwareSettingValue(self, settingName):
        return self.getSettingValue('GPSHARDWARE', settingName)
    def getDebugSettingValue(self, settingName):
        return self.getSettingValue('DEBUG', settingName)
          
    def loadconfig(self):
        config = None
        if os.path.isfile(configfilename):
            config = configparser.ConfigParser()
            config.read(configfilename)
        else:
            config = self.createConfigFile(configfilename)
        return config
    

    