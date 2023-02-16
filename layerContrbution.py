import requests
from Settings import Settings
import json


class Contirubute:
    def __init__(self):
        self.host = Settings.settings['MnA']['Host']
        self.gatewayPort = Settings.settings['MnA']['gatewayPort']
        self.token = Settings.settings['MnA']['token']
        self.org = Settings.settings['MnA']['Org']
        self.role = Settings.settings['MnA']['Role']
        self.local = Settings.settings['MnA']['local']
        self.geoserverHost = Settings.settings['Geoserver']['Host']
        self.geoserverPort = Settings.settings['Geoserver']['Port']
        self.geoserverWorkspace = Settings.settings['Geoserver']['Workspace']
        self.geoserverPass = Settings.settings['Geoserver']['Pass']
        self.geoserverUser = Settings.settings['Geoserver']['User']

    def requestConnect(self, layersName):
        listData = []
        apiURL = f'http://{self.host}:{self.gatewayPort}/adminApi/connect/geoserver/layer'
        geoserverURL = 'http://{}:{}/geoserver/{}/wfs'.format(
            self.geoserverHost, self.geoserverPort, self.geoserverWorkspace)

        for layer in layersName:
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": self.token,
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "http://mna.eastus.cloudapp.azure.com:8080",
                "PentaOrgID": self.org,
                "PentaSelectedLocale": self.local,
                "PentaUserRole": self.role,
                "Pragma": "no-cache",
                "Referer": "http://mna.eastus.cloudapp.azure.com:8080/penta-app-admin/connectwizard",
            }

            data = {
                "adminDatasourceType": "geoserver",
                "url": geoserverURL,
                "username": self.geoserverUser,
                "password": self.geoserverPass,
                "layerName": layer
            }
            
            response = requests.request(
                "POST", apiURL, headers=headers, data=json.dumps(data))
            listData.append(response.text)

            print(response.status_code)
        return listData

    def save(self, layersResponseList):
        savedCount = 0
        bodyList = []
        props = Settings.settings['MnA']['save']
        for layer in layersResponseList:

            jsonLayer: dict = json.loads(layer)
            if jsonLayer.get('layerName'):

                jsonLayer['purchasingPrice'] = props['purchasingPrice']
                jsonLayer['permissions'] = props['permissions']
                jsonLayer['rentingPrice'] = props['rentingPrice']
                jsonLayer['supportedLanguages'] = props['supportedLanguages']
                jsonLayer['displayName'] = jsonLayer['layerName']
                jsonLayer['description'] = jsonLayer['layerName']
                jsonLayer['approvalCondition'] = props['approvalCondition']
                jsonLayer['sharedWith'] = props['sharedWith']

                for field in jsonLayer['fields']:
                    field['supportedLanguages'] = props['fields']['supportedLanguages']
                    field['isSelected'] = props['fields']['isSelected']
                    field['displayName'] = field['fieldName']
                    if field['fieldName'] == props['keyFields']:
                        field['isKeyField'] = True
                    if field['fieldName'] in props['basicFields']:
                        field['isBasicInfo'] == True
                bodyList.append(jsonLayer)
            else:
                print(jsonLayer['message'])
            # print('Done')
            # return bodyList

        apiUrl = f'http://{self.host}:{self.gatewayPort}/adminApi/connect/geoserver/save'
        for body in bodyList:
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": self.token,
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "http://mna.eastus.cloudapp.azure.com:8080",
                "PentaOrgID": self.org,
                "PentaSelectedLocale": self.local,
                "PentaUserRole": self.role,
                "Pragma": "no-cache",
                "Referer": "http://mna.eastus.cloudapp.azure.com:8080/penta-app-admin/connectwizard",
            }

            body = body

            response = requests.request(
                "POST", apiUrl, headers=headers, data=json.dumps(body))
            
            self.updateDocument(response.text)
            
            print(f'{response.status_code}:layer saved sucssesfully')

            savedCount+=1
            print(savedCount)
    
    def updateDocument(self, saveResponse):
        apiUrl = f'http://{self.host}:{self.gatewayPort}/penta-service-metadata/updateDocument'
        
        jsonResponse:dict = json.loads(saveResponse)
        if jsonResponse.get('id'):
            body = {
                "content": {
                    "type": "LAYER",
                    "title": jsonResponse['layerName'],
                    "displayName": jsonResponse['displayName'],
                    "description": jsonResponse['description'],
                    "publisher": "Noha Hesham",
                    "updatedBy": "Noha Hesham",
                    "identifier": jsonResponse['id'],
                    "language": [
                        "ar",
                        "en"
                    ],
                    "organization": jsonResponse['ownedBy'],
                    "capabilities": [
                        "enableSearch",
                        "enableDownload"
                    ],
                    "sharingPermission": "ONLY_ME",
                    "sharedWith": [],
                    "pricing": [
                        10
                    ],
                    "layerExtent": f"{jsonResponse['geometryType'].upper()} ((null null,null null,null null,null null,null null))",
                    "geometryType": jsonResponse['geometryType'],  
                    "twinningPrice": 0,
                    "purchasingPrice": 10,
                    "rentingPrice": 0,
                    "enableAttachment": False,
                    "enableOfflineEdit": False,
                    "subject": [],
                    "subjectsMenu": []
                },
                "id": f"LAYER_{jsonResponse['id']}",
                "index": "mna"
            }

            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": self.token,
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "http://mna.eastus.cloudapp.azure.com:8080",
                "PentaOrgID": self.org,
                "PentaSelectedLocale": self.local,
                "PentaUserRole": self.role,
                "Pragma": "no-cache",
                "Referer": "http://mna.eastus.cloudapp.azure.com:8080/penta-app-admin/connectwizard",
            }

            response = requests.request(
                "PUT", apiUrl, headers=headers, data=json.dumps(body))

            print('MetaData Upate Status', response.text)