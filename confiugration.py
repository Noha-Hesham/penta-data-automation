from Settings import Settings
import requests
import json
import os


class Config:
    def __init__(self):
        self.host = Settings.settings['MnA']['Host']
        self.gatwayPort = Settings.settings['MnA']['gatewayPort']
        self.application = Settings.settings['MnA']['application']
        self.org = Settings.settings['MnA']['Org']
        self.token = Settings.settings['MnA']['token']
        self.role = Settings.settings['MnA']['Role']
        self.configSetting = Settings.settings['MnA']['config']

        self.header = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': f'http://{self.host}:{self.gatwayPort}',
            'PentaOrgID': self.org,
            'PentaSelectedLocale': 'en',
            'PentaUserRole': self.role,
        }

    def getPermittedLayers(self, startWithFilter=''):
        layersId = []
        url = f'http://{self.host}:{self.gatwayPort}/adminApi/layer/permitted/Admin'
        body = {}
        try:
            response = requests.request(
                "GET", url, headers=self.header, data=json.dumps(body))
            print(response.status_code)
            layersList = response.json()
            for layer in layersList:
                if layer['geometryType']!='Raster':
                        if layer['displayName'].startswith(startWithFilter):
                            layersId.append(layer['id'])

        except Exception as error:
            print(error)

        return layersId


    def getPermittedFields(self, layerId):
        
        url = f'http://{self.host}:{self.gatwayPort}/adminApi/layer/{layerId}/fields'
        body = {}
        response = requests.request(
            "GET", url, headers=self.header, data=json.dumps(body))
        return response.json()
        
    def permmitLayers(self):
        url = ''
        body = {}
        response = requests.request(
            "POST", url, headers=self.header, data=json.dumps(body))

    def getPluginSetting(self):
        pluginName = self.configSetting['pluginName']
        url = f'http://{self.host}:{self.gatwayPort}/configApi/config/role?path={pluginName}&app={self.application}&idsOnly=true&ignoreLocale=true&role={self.role}'
        body = {}
        response = requests.request(
            "GET", url, headers=self.header, data=json.dumps(body))

        return response.json()

    def readSettings(self,pluginName):
        settingFolder = os.path.join(os.getcwd(),f'pluginSettings/{pluginName}.json')
        ofile = open(settingFolder)
        jsonfile = json.load(ofile)
        return jsonfile
    
    def createPluginSetting(self, layerIds):
        pluginName = Settings.settings['MnA']['config']['pluginName']
        if pluginName == 'ma-plugin-ol-map':

            pluginSetting = self.readSettings(pluginName)
            pluginLayersList = pluginSetting['data']['dataSettings']['layers']
            myLayerObject= self.configSetting['variable'][0]


            for id in layerIds:
                pluginSetting['path'] = pluginName
                pluginSetting['roleid'] = self.role
                pluginSetting['appName'] = self.application
                myLayerObject = {
                        "basicSettings": 
                            {
                                "addToLegend": "true",
                                "visible": False,
                                "opacity": "0.5"
                            },
                        "advancedSettings": {},
                        "id": id
                    }
                
                pluginLayersList.append(myLayerObject)

        elif pluginName == 'ma-plugin-identify-climateChange':

            pluginSetting = self.readSettings(pluginName)
            pluginLayersList = pluginSetting['data']['dataSettings']['layers']

            for layerId in layerIds:
                pluginSetting['path'] = pluginName
                pluginSetting['roleid'] = self.role
                pluginSetting['appName'] = self.application
                fields = self.getPermittedFields(layerId)
                myLayerObject = {
                                        "id": layerId,
                                        "fields": [],
                                        "basicSettings": {
                                            "tolerance": 10
                                        },
                                        "advancedSettings": {}
                                    }
                
                for field in fields:
                    if field['fieldName'] != 'id':
                        fieldId = field['id']
                        subfield = myLayerObject['fields']
                        subfield.append(
                                            {
                                            "id": fieldId,
                                            "basicSettings": {},
                                            "advancedSettings": {}
                                            }
                                        )  
                pluginLayersList.append(myLayerObject)

        elif pluginName == 'ma-plugin-toc-climate':
            pluginSetting = self.readSettings(pluginName)
            pluginLayersList = pluginSetting['data']['dataSettings']['layers']

            for layerId in layerIds:
                pluginSetting['path'] = pluginName
                pluginSetting['roleid'] = self.role
                pluginSetting['appName'] = self.application

                myLayerObject = { 
                    "id": layerId,
                    "basicSettings": {}, 
                    "advancedSettings": {} 
                    }
                pluginLayersList.append(myLayerObject)

        return json.dumps(pluginSetting)

    def createHeaderPluginSetting(self):

        pluginName = Settings.settings['MnA']['config']['pluginName']

        if pluginName == 'ma-plugin-header-climate':
            pluginSetting = self.readSettings(pluginName)
            groupLayersList = pluginSetting['data']['dataSettings']['LayersGroup']
            subLayersList = pluginSetting['data']['dataSettings']['subLayers']
            
            subLayersNames = [] ## add sublayersNames in list

            for name in subLayersNames:
                layerList = self.getPermittedLayers(name)
                for id in layerList:
                    subLayersObject = {
                                        "subLayersField": [],
                                        "basicSettings": {
                                        "isSecondaryLayer": False
                                        },
                                        "advancedSettings": {},
                                        "id": id
                                    }       
                    subLayersFields = subLayersObject['subLayersField']
                    subLayerFieldList = self.getPermittedFields(id)
                    for fieldID in subLayerFieldList:
                        subLayersFields.append(
                            { "basicSettings": {}, "advancedSettings": {}, "id": fieldID }
                        )
                    subLayersList.append(subLayersObject)
                                    
            groups = self.getGroupName()
            for group in groups:
                categories = self.getCategories(group)
                strCategories = ",".join(categories)
                groupObject = {
                            "headerLayers": [],
                            "hasCategories": True,
                            "Categories": strCategories,
                            "GroupName": group
                            }
                headerLayersList = groupObject['headerLayers']
                for category in categories:
                    layersList = self.getCategoryLayers(category)
                    for layer in layersList:
                        
                        layerIdList = self.getPermittedLayers(layer)
                        for layerId in layerIdList:
                            pluginSetting['path'] = pluginName
                            pluginSetting['roleid'] = self.role
                            pluginSetting['appName'] = self.application
                            ##add condition to set subgroups ids
                            ##add condition to set svgs
                            ##clear displaynames
                            ##fix dupplication bug
                            headerLayerObject = {
                                "basicSettings": {
                                    "isSecondaryLayer": False,
                                    "hasSubLayer": False,
                                    "CategoryName": category,
                                    "LayerIcon": [
                                        {
                                        "name": "TemperatureSvg1662073697010.svg",
                                        "fileurl": "/penta-service-storage/downloadFile/1662073698110/TemperatureSvg1662073697010.svg?orgId=climatechanges&category=",
                                        "type": "image/svg+xml"
                                        }
                                    ],
                                    "subLayersNames": ""
                                },
                                "advancedSettings": {},
                                "id": layerId,
                                "fields": []
                            }
                            
                            fields = self.getPermittedFields(layerId)
                            for field in fields:
                                fieldId = field['id']
                                subfield = headerLayerObject['fields']
                                subfield.append(
                                                    { "advancedSettings": {}, "id": fieldId }
                                                )

                            headerLayersList.append(headerLayerObject)
                groupLayersList.append(groupObject)
                            

        return json.dumps(pluginSetting)

    def getHeaderMapping(self):
        headerMapping = self.configSetting['headerMapping']
        return headerMapping

    def headerSVG(self,layerName):
        svgUrl = ''
        tempreature = [
                    "forecast:tas_degree_rf_1980_2005_monmin_values",
                    "forecast:tas_degree_rf_1980_2005_monmean_values",
                    "forecast:tas_degree_rf_1980_2005_monmax_values",
                    "forecast:mean_of_air_temperature_at_2m_1981_2010_values",
                    "forecast:mean_of_minimum_air_temperature_1981_2010_values",
                    "forecast:mean_of_maximum_air_temperature_1981_2010_values",
                    "forecast:temperature_djf_rcp45_values",
                    "forecast:tas_degree_rcp45_2006_2100_monmean_nc_remap_values",
                    "forecast:tas_degree_rcp45_2006_2100_monmin_nc_remap_values",
                    "forecast:tas_degree_rcp45_2006_2100_monmax_nc_remap_values",
                    "forecast:ndays_maxt_gt_35_rf_1980_2005_values",
                    "forecast:ndays_maxt_gt_40_rf_1980_2005_values",
                    "forecast:heat_waves_rf_1980_2005_3days_1_values",
                    "forecast:nfdays_mint_lt_0_rf_1980_2005_values",
                    "forecast:trnights_mint_gt_20_rf_1980_2005_nc_remap_values",
                    "forecast:ndays_gt_10mm_rf_1980_2005_values",
                    "forecast:ndays_gt_20mm_rf_1980_2005_values",
                    "forecast:ndays_maxt_gt_35_rcp45_2006_2100_nc_remap_values",
                    "forecast:ndays_maxt_gt_40_rcp45_2006_2100_nc_remap_values",
                    "forecast:heat_waves_rcp45_2006_2100_3days_nc_remap_1_values",
                    "forecast:nfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values",
                    "forecast:trnights_mint_gt_20_rcp45_2006_2100_nc_remap_values",
                    "forecast:ndays_gt_10mm_rcp45_2006_2100_nc_remap_values",
                    "forecast:ndays_gt_20mm_rcp45_2006_2100_nc_remap_values",
                    "forecast:ncdry_days_rcp45_2006_2100_1_values"
                ]
        rain = [
                "forecast:pr_rf_1980_2005_monsum_mm_month_values",
                "forecast:mean_of_monthly_total_precipita_1981_2010_values",
                "forecast:pr_mm_rcp45_2006_2100_monsum_nc_remap_values"
            ]
        sund =[
                "forecast:sund_hour_rcp45_2006_2100_monsum_nc_remap_values"
            ]
        humidity = [
        "forecast:relhumid_rf_1980_2005_monmean_values",
        "forecast:relhumid_rf_1980_2005_monmin_values",
        "forecast:relhumid_rf_1980_2005_monmax_values",
        "forecast:mean_of_relative_humidity_1981_2010_values",
        "forecast:mean_of_relative_humidity_1981_2010_values",
        "forecast:rainfall_djf_rcp45_values",
        "forecast:hurs_rcp45_2006_2100_monmean_nc_remap_values",
        "forecast:hurs_rcp45_2006_2100_monmin_nc_remap_values",
        "forecast:hurs_rcp45_2006_2100_monmax_nc_remap_values"

        ]  
        wind=[]
        pressure=[
            "forecast:psl_rf_1980_2005_monmean_values",
            "forecast:mean_sea_level_pressure_1981_2010_values",
            "forecast:psl_rcp45_2006_2100_monmean_nc_remap_values"
        ]
        dust=[
            "forecast:rf_percent_dust_75p_1980_2005_nc_remap_values",
            "forecast:rf_percent_dust_90p_1980_2005_nc_remap_values",
            "forecast:rf_percent_dust_95p_1980_2005_nc_remap_values",
            "forecast:rf_percent_dust_99p_1980_2005_nc_remap_values",
            "forecast:rcp45_percent_dust_75p_2006_2100_nc_remap_values",
            "forecast:rcp45_percent_dust_90p_2006_2100_nc_remap_values",
            "forecast:rcp45_percent_dust_95p_2006_2100_nc_remap_values",
            "forecast:rcp45_percent_dust_99p_2006_2100_nc_remap_values"
        ]
        plant =[
            "forecast:potential_evapotranspiration_rcp45_2006_2100_remap_values"
        ]

        if layerName in tempreature:
            svgUrl = 'http://mna.eastus.cloudapp.azure.com:8080/penta-service-storage/downloadFile/1666045112532/tempreature.svg?orgId=climatechanges&category=headerSVG'
        elif layerName in rain : 
            svgUrl = 'http://mna.eastus.cloudapp.azure.com:8080/penta-service-storage/downloadFile/1666045300661/rain.svg?orgId=climatechanges&category=headerSVG'
        elif layerName in humidity:
            svgUrl = 'http://mna.eastus.cloudapp.azure.com:8080/penta-service-storage/downloadFile/1666045490569/humedity.svg?orgId=climatechanges&category=headerSVG'
        elif layerName in pressure:
            svgUrl = 'http://mna.eastus.cloudapp.azure.com:8080/penta-service-storage/downloadFile/1666046231675/Pressure.svg?orgId=climatechanges&category=headerSVG'

        elif layerName in dust:
            svgUrl = 'http://mna.eastus.cloudapp.azure.com:8080/penta-service-storage/downloadFile/1666047772992/Dust.svg?orgId=climatechanges&category=headerSVG'
        return svgUrl
    def getGroupName(self):
        groups = self.getHeaderMapping()
        groupsList = []
        for group in groups:
            groupName = group['GroupName']
            groupsList.append(groupName)
        return groupsList

    def getCategories(self, groupName):
        groups = self.getHeaderMapping()
        categoriesList = []
        for group in groups:
            if groupName == group['GroupName']:
                for category in group['Categories']:
                    categoriesList.append(category['name'])
        return categoriesList

    def getCategoryLayers(self, categoryName):
        groups = self.getHeaderMapping()
        for group in groups:
            Categories = group['Categories']
            for category in Categories:
                if categoryName == category['name']:
                    return category['layers']
        
    def creatChartPluginSetting(self):
        tempreature= [
        "forecast:tas_degree_rf_1980_2005_monmin_values",
        "forecast:tas_degree_rf_1980_2005_monmean_values",
        "forecast:tas_degree_rf_1980_2005_monmax_values",
        "forecast:mean_of_air_temperature_at_2m_1981_2010_values",
        "forecast:mean_of_minimum_air_temperature_1981_2010_values",
        "forecast:mean_of_maximum_air_temperature_1981_2010_values",
        "forecast:temperature_djf_rcp45_values",
        "forecast:tas_degree_rcp45_2006_2100_monmean_nc_remap_values",
        "forecast:tas_degree_rcp45_2006_2100_monmin_nc_remap_values",
        "forecast:tas_degree_rcp45_2006_2100_monmax_nc_remap_values",
        "forecast:ndays_maxt_gt_35_rf_1980_2005_values",
        "forecast:ndays_maxt_gt_40_rf_1980_2005_values",
        "forecast:heat_waves_rf_1980_2005_3days_1_values",
        "forecast:nfdays_mint_lt_0_rf_1980_2005_values",
        "forecast:trnights_mint_gt_20_rf_1980_2005_nc_remap_values",
        "forecast:ndays_gt_10mm_rf_1980_2005_values",
        "forecast:ndays_gt_20mm_rf_1980_2005_values",
        "forecast:ndays_maxt_gt_35_rcp45_2006_2100_nc_remap_values",
        "forecast:ndays_maxt_gt_40_rcp45_2006_2100_nc_remap_values",
        "forecast:heat_waves_rcp45_2006_2100_3days_nc_remap_1_values",
        "forecast:nfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values",
        "forecast:trnights_mint_gt_20_rcp45_2006_2100_nc_remap_values",
        "forecast:ndays_gt_10mm_rcp45_2006_2100_nc_remap_values",
        "forecast:ndays_gt_20mm_rcp45_2006_2100_nc_remap_values",
        "forecast:ncdry_days_rcp45_2006_2100_1_values"]
        pluginName = Settings.settings['MnA']['config']['pluginName']
        joinSchema = Settings.settings['DataBase']['joinTables']

        if pluginName == 'ma-plugin-climate-charts':
            pluginSetting = self.readSettings(pluginName)

            pluginName = Settings.settings['MnA']['config']['pluginName']
            pluginLayersList = pluginSetting['data']['dataSettings']['layers']
            chartMapping = self.configSetting['chartMapping']
            timeChart = self.configSetting['timeChart']
            boundaryChart = self.configSetting['boundaryChart']

            #line,spline,bar,scatter
            #Violet,Carmine,Contrast,Dark Moon

            for chart in chartMapping:
                valueTable = chart['viewParams']['v_table']
                locationTable = ''
                chartEnName = chart['entityData']['chart']['title_en']
                chartUnit = chart['entityData']['chart']['unit']
                layerName = 'forecast:'+valueTable
                layerIds = self.getPermittedLayers(layerName)

                if valueTable in joinSchema['location_50']:
                    locationTable = 'location_50'
                elif valueTable in joinSchema['location_262144']:
                    locationTable = 'location_262144'
                elif valueTable in joinSchema['location_5006']:
                    locationTable = 'location_5006'
                else:
                    locationTable = 'location_13225'

                for layerId in layerIds:
                    pluginSetting['path'] = pluginName
                    pluginSetting['roleid'] = self.role
                    pluginSetting['appName'] = self.application
                    fields = self.getPermittedFields(layerId)
                    myLayerObject = {
                            "id": layerId,
                            "fields": [],          
                            "basicSettings": {
                                    "DATA_SRC": {
                                        "LYR_LOC": locationTable,
                                        "LYR_VAL": valueTable
                                    },
                                    "CHART_TIME": {
                                        "theme": timeChart['theme'],
                                        "caption": chartEnName ,
                                        "xAxisName": "Hour",
                                        "yAxisName": chartUnit,
                                        "CHART_TYPE": timeChart['type'],
                                        "subCaption": "Last 24 Hours",
                                        "CHRT_TIME_CONFIG": "Label"
                                    },
                                    "TABLE_TIME": {
                                        "USE_IMG": False,
                                        "table_key": "Date",
                                        "table_value": chartUnit,
                                        "IMAGE_VALUES": [],
                                        "TBL_TIME_CONFIG": "Label"
                                    },
                                    "CHART_BOUNDARY": {
                                        "theme": boundaryChart['theme'],
                                        "caption": chartEnName,
                                        "xAxisName": "Gov Code",
                                        "yAxisName": chartUnit,
                                        "CHART_TYPE": boundaryChart['type'],
                                        "subCaption": "By Boundary",
                                        "CHRT_BOUND_CONFIG": "Label"
                                    },
                                    "TABLE_BOUNDARY": {
                                        "USE_IMG": False,
                                        "table_key": "Government Code",
                                        "table_value": chartUnit,
                                        "TBL_BOUND_CONFIG": "Label",
                                        "IMAGE_VALUES": [
                                        {
                                            "TO": "20",
                                            "IMG": [
                                            {
                                                "name": "winter1662242155768.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242159973/winter1662242155768.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "0"
                                        },
                                        {
                                            "TO": "30",
                                            "IMG": [
                                            {
                                                "name": "21662242185960.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242188605/21662242185960.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "21"
                                        },
                                        {
                                            "TO": "40",
                                            "IMG": [
                                            {
                                                "name": "31662242213423.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242216005/31662242213423.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "31"
                                        }
                                    ]
                                    }
                                },
                            "advancedSettings": {}
                            }
                    imageTimeTable = myLayerObject['basicSettings']['TABLE_TIME']
                    timeImageList = imageTimeTable['IMAGE_VALUES']
                    imageBoundaryTable = myLayerObject['basicSettings']['TABLE_BOUNDARY']
                    boundaryImageList = imageBoundaryTable['IMAGE_VALUES']
                    if layerName in tempreature:
                        imageTimeTable = True
                        timeImageList =[
                                        {
                                            "TO": "20",
                                            "IMG": [
                                            {
                                                "name": "winter1662242155768.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242159973/winter1662242155768.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "0"
                                        },
                                        {
                                            "TO": "30",
                                            "IMG": [
                                            {
                                                "name": "21662242185960.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242188605/21662242185960.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "21"
                                        },
                                        {
                                            "TO": "40",
                                            "IMG": [
                                            {
                                                "name": "31662242213423.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242216005/31662242213423.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "31"
                                        }
                                    ]
                        imageBoundaryTable = True
                        boundaryImageList = [
                                        {
                                            "TO": "20",
                                            "IMG": [
                                            {
                                                "name": "winter1662242155768.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242159973/winter1662242155768.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "0"
                                        },
                                        {
                                            "TO": "30",
                                            "IMG": [
                                            {
                                                "name": "21662242185960.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242188605/21662242185960.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "21"
                                        },
                                        {
                                            "TO": "40",
                                            "IMG": [
                                            {
                                                "name": "31662242213423.png",
                                                "type": "image/png",
                                                "fileurl": "/penta-service-storage/downloadFile/1662242216005/31662242213423.png?orgId=climatechanges&category="
                                            }
                                            ],
                                            "FROM": "31"
                                        }
                                    ]
                    imageValues = [
                                    {
                                        "TO": "20",
                                        "IMG": [
                                        {
                                            "name": "winter1662242155768.png",
                                            "type": "image/png",
                                            "fileurl": "/penta-service-storage/downloadFile/1662242159973/winter1662242155768.png?orgId=climatechanges&category="
                                        }
                                        ],
                                        "FROM": "0"
                                    },
                                    {
                                        "TO": "30",
                                        "IMG": [
                                        {
                                            "name": "21662242185960.png",
                                            "type": "image/png",
                                            "fileurl": "/penta-service-storage/downloadFile/1662242188605/21662242185960.png?orgId=climatechanges&category="
                                        }
                                        ],
                                        "FROM": "21"
                                    },
                                    {
                                        "TO": "40",
                                        "IMG": [
                                        {
                                            "name": "31662242213423.png",
                                            "type": "image/png",
                                            "fileurl": "/penta-service-storage/downloadFile/1662242216005/31662242213423.png?orgId=climatechanges&category="
                                        }
                                        ],
                                        "FROM": "31"
                                    }
                                ]
                    subfield = myLayerObject['fields']
                    for field in fields:
                        if field['fieldName'] != 'id':
                            fieldId = field['id']
                            subfield.append(
                                                {
                                                "id": fieldId,
                                                "basicSettings": {},
                                                "advancedSettings": {}
                                                }
                                            )
                
                    pluginLayersList.append(myLayerObject)
        # print(json.dumps(pluginSetting))
            return json.dumps(pluginSetting)

    def setChartImages(self):
        tempreature= [
        "forecast:tas_degree_rf_1980_2005_monmin_values",
        "forecast:tas_degree_rf_1980_2005_monmean_values",
        "forecast:tas_degree_rf_1980_2005_monmax_values",
        "forecast:mean_of_air_temperature_at_2m_1981_2010_values",
        "forecast:mean_of_minimum_air_temperature_1981_2010_values",
        "forecast:mean_of_maximum_air_temperature_1981_2010_values",
        "forecast:temperature_djf_rcp45_values",
        "forecast:tas_degree_rcp45_2006_2100_monmean_nc_remap_values",
        "forecast:tas_degree_rcp45_2006_2100_monmin_nc_remap_values",
        "forecast:tas_degree_rcp45_2006_2100_monmax_nc_remap_values",
        "forecast:ndays_maxt_gt_35_rf_1980_2005_values",
        "forecast:ndays_maxt_gt_40_rf_1980_2005_values",
        "forecast:heat_waves_rf_1980_2005_3days_1_values",
        "forecast:nfdays_mint_lt_0_rf_1980_2005_values",
        "forecast:trnights_mint_gt_20_rf_1980_2005_nc_remap_values",
        "forecast:ndays_gt_10mm_rf_1980_2005_values",
        "forecast:ndays_gt_20mm_rf_1980_2005_values",
        "forecast:ndays_maxt_gt_35_rcp45_2006_2100_nc_remap_values",
        "forecast:ndays_maxt_gt_40_rcp45_2006_2100_nc_remap_values",
        "forecast:heat_waves_rcp45_2006_2100_3days_nc_remap_1_values",
        "forecast:nfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values",
        "forecast:trnights_mint_gt_20_rcp45_2006_2100_nc_remap_values",
        "forecast:ndays_gt_10mm_rcp45_2006_2100_nc_remap_values",
        "forecast:ndays_gt_20mm_rcp45_2006_2100_nc_remap_values",
        "forecast:ncdry_days_rcp45_2006_2100_1_values"]

        imageValues = [
                        {
                            "TO": "20",
                            "IMG": [
                            {
                                "name": "winter1662242155768.png",
                                "type": "image/png",
                                "fileurl": "/penta-service-storage/downloadFile/1662242159973/winter1662242155768.png?orgId=climatechanges&category="
                            }
                            ],
                            "FROM": "0"
                        },
                        {
                            "TO": "30",
                            "IMG": [
                            {
                                "name": "21662242185960.png",
                                "type": "image/png",
                                "fileurl": "/penta-service-storage/downloadFile/1662242188605/21662242185960.png?orgId=climatechanges&category="
                            }
                            ],
                            "FROM": "21"
                        },
                        {
                            "TO": "40",
                            "IMG": [
                            {
                                "name": "31662242213423.png",
                                "type": "image/png",
                                "fileurl": "/penta-service-storage/downloadFile/1662242216005/31662242213423.png?orgId=climatechanges&category="
                            }
                            ],
                            "FROM": "31"
                        }
                    ]

    def createTimelinePluginSetting(self):
        pluginName = Settings.settings['MnA']['config']['pluginName']
        pluginSetting = self.readSettings(pluginName)
        if pluginName == 'ma-plugin-timeline':
            pluginLayersList = pluginSetting['data']['dataSettings']['layers']
            groups = self.getGroupName()
            monthList = ['forecast:moderate_wet_days_percent_rf_1980_2005_nc_remap_values', 'forecast:moderate_wet_days_percent_rcp85_2006_2100_nc_remap_values', 'forecast:moderate_wet_days_percent_rcp45_2006_2100_nc_remap_values', 'forecast:moderate_wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'forecast:moderate_wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'forecast:moderate_wet_days_amount_ratio_rf_1980_2005_values', 'forecast:wet_days_percent_rcp85_2006_2100_nc_remap_values', 'forecast:wet_days_percent_rf_1980_2005_nc_remap_values', 'forecast:wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'forecast:wet_days_percent_rcp45_2006_2100_nc_remap_values', 'forecast:wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'forecast:wet_days_amount_ratio_rf_1980_2005_nc_remap_values', 'forecast:extremely_wet_days_percent_rcp85_2006_2100_nc_remap_values', 'forecast:extremely_wet_days_percent_rcp45_2006_2100_nc_remap_values', 'forecast:extremely_wet_days_amount_ratio_rf_1980_2005_nc_remap_values', 'forecast:extremely_wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'forecast:extremely_wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'forecast:extremely_wet_days_percent_rf_1980_2005_nc_remap_values', 'forecast:ndays_gt_25mm_rcp85_2006_2100_nc_remap_values', 'forecast:ndays_gt_25mm_rcp45_2006_2100_nc_remap_values', 'forecast:ndays_gt_25mm_rf_1980_2005_nc_remap_values', 'forecast:sdii_rcp85_2006_2100_nc_remap_values', 'forecast:sdii_rcp45_2006_2100_nc_remap_values', 'forecast:sdii_rf_1980_2005_nc_remap_values', 'forecast:nwet_days_rcp45_2006_2100_nc_remap_values', 'forecast:nwet_days_rcp85_2006_2100_nc_remap_values', 'forecast:nwet_days_rf_1980_2005_nc_remap_values', 'forecast:very_wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'forecast:very_wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'forecast:very_wet_days_amount_ratio_rf_1980_2005_nc_remap_values', 'forecast:very_wet_days_percent_rcp85_2006_2100_nc_remap_values', 'forecast:very_wet_days_percent_rf_1980_2005_nc_remap_values', 'forecast:very_wet_days_percent_rcp45_2006_2100_nc_remap_values', 'forecast:max_pr_rcp45_monthly_2006_2100_nc_remap_values', 'forecast:max_pr_rf_yearly_1980_2005_nc_remap_values', 'forecast:max_pr_rf_monthly_1980_2005_nc_remap_values', 'forecast:max_pr_rcp45_yearly_2006_2100_nc_remap_values', 'forecast:max_pr_rcp85_yearly_2006_2100_nc_remap_values', 'forecast:max_pr_rcp85_monthly_2006_2100_nc_remap_values', 'forecast:sund_hour_rcp85_2006_2100_monsum_nc_remap_values', 'forecast:hurs_rcp85_2006_2100_monmin_nc_remap_values', 'forecast:sfcWind_rcp85_2006_2100_monmean_nc_remap_values', 'forecast:tas_degree_rcp85_2006_2100_monmax_nc_remap_values', 'forecast:psl_rcp85_2006_2100_monmean_nc_remap_values', 'forecast:sfcWind_rcp85_2006_2100_monmax_nc_remap_values', 'forecast:tas_degree_rcp85_2006_2100_monmin_nc_remap_values', 'forecast:hurs_rcp85_2006_2100_monmean_nc_remap_values', 'forecast:sfcWind_rcp85_2006_2100_monmin_nc_remap_values', 'forecast:tas_degree_rcp85_2006_2100_monmean_nc_remap_values', 'forecast:hurs_rcp85_2006_2100_monmax_nc_remap_values', 'forecast:pr_mm_rcp85_2006_2100_monsum_nc_remap_values', 'forecast:sfcwind_rcp45_2006_2100_monmean_nc_remap_values', 'forecast:hurs_rcp45_2006_2100_monmin_nc_remap_values', 'forecast:hurs_rcp45_2006_2100_monmean_nc_remap_values', 'forecast:hurs_rcp45_2006_2100_monmax_nc_remap_values', 'forecast:tas_degree_rcp45_2006_2100_monmax_nc_remap_values', 'forecast:sfcwind_rcp45_2006_2100_monmin_nc_remap_values', 'forecast:psl_rcp45_2006_2100_monmean_nc_remap_values', 'forecast:sfcwind_rcp45_2006_2100_monmax_nc_remap_values', 'forecast:tas_degree_rcp45_2006_2100_monmin_nc_remap_values', 'forecast:sund_hour_rcp45_2006_2100_monsum_nc_remap_values', 'forecast:tas_degree_rcp45_2006_2100_monmean_nc_remap_values', 'forecast:pr_mm_rcp45_2006_2100_monsum_nc_remap_values', 'forecast:cold_waves_rcp45_2006_2100_3days_nc_remap_values', 'forecast:cold_waves_rf_1980_2005_3days_nc_remap_values', 'forecast:cold_waves_rcp85_2006_2100_3days_nc_remap_values', 'forecast:cold_spells_rf_1980_2005_nc_remap_values', 'forecast:cold_spells_rcp85_2006_2100_nc_remap_values', 'forecast:cold_spells_rcp45_2006_2100_nc_remap_values', 'forecast:warm_nights_percent_rf_1980_2005_values', 'forecast:very_cold_days_percent_rcp45_2006_2030_values', 'forecast:cold_nights_percent_rf_1980_2005_values', 'forecast:warm_days_percent_rf_1980_2005_values', 'forecast:warm_nights_percent_rcp45_2006_2030_values', 'forecast:cold_days_percent_rcp85_2006_2030_values', 'forecast:very_warm_days_percent_rf_1980_2005_values', 'forecast:cold_days_percent_rf_1980_2005_values', 'forecast:cold_days_percent_rcp45_2006_2030_values', 'forecast:very_cold_days_percent_rf_1980_2005_values', 'forecast:very_warm_days_percent_rcp45_2006_2030_values', 'forecast:cold_nights_percent_rcp85_2006_2030_values', 'forecast:cold_nights_percent_rcp45_2006_2030_values', 'forecast:warm_nights_percent_rcp85_2006_2030_values', 'forecast:warm_days_percent_rcp45_2006_2030_values', 'forecast:warm_days_percent_rcp85_2006_2030_values', 'forecast:very_cold_days_percent_rcp85_2006_2030_values', 'forecast:very_warm_days_percent_rcp85_2006_2030_values', 'forecast:ndays_maxt_gt_25_rf_1980_2005_nc_remap_values', 'forecast:ndays_maxt_gt_25_rcp85_2006_2100_nc_remap_values', 'forecast:ndays_maxt_gt_25_rcp45_2006_2100_nc_remap_values', 'forecast:ndays_maxt_gt_45_rcp45_2006_2100_nc_remap_values', 'forecast:ndays_maxt_gt_45_rf_1980_2005_nc_remap_values', 'forecast:ndays_maxt_gt_30_rcp85_2006_2100_nc_remap_values', 'forecast:ndays_maxt_gt_45_rcp85_2006_2100_nc_remap_values', 'forecast:ndays_maxt_gt_30_rf_1980_2005_nc_remap_values', 'forecast:ndays_maxt_gt_30_rcp45_2006_2100_nc_remap_values', 'forecast:warm_spells_rf_1980_2005_nc_remap_values', 'forecast:warm_spells_rcp85_2006_2100_nc_remap_values', 'forecast:warm_spells_rcp45_2006_2100_nc_remap_values', 'forecast:ncfdays_mint_lt_0_rf_1980_2005_nc_remap_values', 'forecast:ncfdays_mint_lt_0_rcp85_2006_2100_nc_remap_values', 'forecast:ncfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_40_rf_1980_2005_nc_remap_values', 'forecast:ncsudays_maxt_gt_30_rf_1980_2005_nc_remap_values', 'forecast:ncsudays_maxt_gt_40_rcp45_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_45_rcp85_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_30_rcp45_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_35_rcp85_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_30_rcp85_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_35_rcp45_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_35_rf_1980_2005_nc_remap_values', 'forecast:ncsudays_maxt_gt_40_rcp85_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_45_rcp45_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_25_rf_1980_2005_nc_remap_values', 'forecast:ncsudays_maxt_gt_25_rcp45_2006_2100_nc_remap_values', 'forecast:ncsudays_maxt_gt_35_rf_1980_2005_values', 'forecast:ncsudays_maxt_gt_45_rf_1980_2005_nc_remap_values', 'forecast:tas_degree_rf_1980_2005_monmax_values', 'forecast:tas_degree_rf_1980_2005_monmin_values', 'forecast:relhumid_rf_1980_2005_monmean_values', 'forecast:tas_degree_rf_1980_2005_monmean_values', 'forecast:sund_rf_1980_2005_monsum_values', 'forecast:sfcwind_rf_1980_2005_monmin_nc_remap_values', 'forecast:pr_rf_1980_2005_monsum_mm_month_values', 'forecast:relhumid_rf_1980_2005_monmax_values', 'forecast:psl_rf_1980_2005_monmean_values', 'forecast:relhumid_rf_1980_2005_monmin_values', 'forecast:sfcwind_rf_1980_2005_monmean_nc_remap_values', 'forecast:sfcwind_rf_1980_2005_monmax_nc_remap_values', 'forecast:potential_evapotranspiration_rcp45_2006_2100_remap_values', 'forecast:potential_evapotranspiration_rf_1980_2005_remap_values', 'forecast:potential_evapotranspiration_rcp85_2006_2100_remap_values', 'forecast:moderate_wet_days_amount_ratio_rf_2006_2100_nc_remap_values', 'forecast:mean_of_air_temperature_at_2m_1981_2010_values', 'forecast:mean_of_maximum_air_temperature_1981_2010_values', 'forecast:mean_of_minimum_air_temperature_1981_2010_values', 'forecast:mean_of_monthly_total_precipita_1981_2010_values', 'forecast:mean_of_relative_humidity_1981_2010_values', 'forecast:mean_sea_level_pressure_1981_2010_values']
            fromYear = None
            toYear = None

            
            for group in groups:
                categories = self.getCategories(group)
                for category in categories:
                    layersList = self.getCategoryLayers(category)

                    for layer in layersList:
                        if '1980_2005' in layer:
                            fromYear = 1980
                            toYear = 2005

                        elif '1981_2010'in layer:
                            fromYear = 1981
                            toYear = 2010

                        elif '2006_2100'in layer:
                            fromYear = 2006
                            toYear = 2100

                        elif '1980_2005'in layer:
                            fromYear = 1980
                            toYear = 2005
                        elif layer == 'forecast:temperature_djf_rcp45_values':
                            fromYear = 2010
                            toYear = 2090
                            
                        elif layer == 'forecast:rainfall_djf_rcp45_values':
                            fromYear = 2010
                            toYear = 2090


                        if layer in monthList:
                            layerIdList = self.getPermittedLayers(layer)
                            
                            for layerId in layerIdList:
                                myLayerObject = {
                                                "id": layerId,
                                                "basicSettings": {
                                                    "toYear": toYear,
                                                    "fromYear": fromYear,
                                                    "dropdownItems": {
                                                    "month": True,
                                                    "season": True
                                                    },
                                                    "useCustomgRid": False
                                                },
                                                "advancedSettings": {}
                                                }
                                
                                pluginSetting['path'] = pluginName
                                pluginSetting['roleid'] = self.role
                                pluginSetting['appName'] = self.application
                                myLayerObject['id'] = layerId

                                pluginLayersList.append(myLayerObject)

                        else:
                            layerIdList = self.getPermittedLayers(layer)
                            for layerId in layerIdList:
                                myLayerObject = {
                                                "id": layerId,
                                                "basicSettings": {
                                                    "toYear": toYear,
                                                    "fromYear": fromYear,
                                                    "dropdownItems": {
                                                    "month": False,
                                                    "season": False
                                                    },
                                                    "useCustomgRid": False
                                                },
                                                "advancedSettings": {}
                                                }
                                pluginSetting['path'] = pluginName
                                pluginSetting['roleid'] = self.role
                                pluginSetting['appName'] = self.application
                                myLayerObject['id'] = layerId


                                pluginLayersList.append(myLayerObject)
                        
            return json.dumps(pluginSetting)

                
                
                
            

    def pluginConfig(self,pluginSetting):

        url = f'http://{self.host}:{self.gatwayPort}/configApi/config'
        body = pluginSetting

        try:
            response = requests.request(
                "POST", url, headers=self.header, data=str(body))
            print(response.text)
        except Exception as error:
            print(error)
