import os
import json

class Settings:
    settings = None
    def __init__(self):
        pass

    @classmethod
    def getSettingJson(cls, fName=''):
        '''
        Info: reading setting from json file

        Requirments: setting files mmust be in the same dir as the script
        Input: No input
        Output: JSON
        '''

        fPath = os.path.join(os.getcwd(), fName)
        oFile = open(fPath)
        readf = json.load(oFile)
        oFile.close()
        cls.settings=readf

        