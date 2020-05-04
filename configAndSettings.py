import configparser
import os

#creates the config file if it does not exist
def createConfigFile(configFileName):
    #cretes the config file if it does not exist
    #we will add all the default settings here
    if not os.path.isfile(configFileName):
            
        config = configparser.ConfigParser()
        config['JS8CALLSERVER'] = {'serverip': '127.0.0.1',
                             'serverport': 2242
                            }
            
        with open(configFileName, 'w') as configfile:
            config.write(configfile)
            configfile.close()

def getAttribute(sectionName, attributeName):

    attr = None
    
    if os.path.isfile(configfilename):
        config = configparser.ConfigParser()
        config.read(configfilename)

        attr = config.get(sectionName,attributeName)
        
    return attr

configfilename="./settings.gfg"
#create the config file on load if it does not already exist
createConfigFile(configfilename)
