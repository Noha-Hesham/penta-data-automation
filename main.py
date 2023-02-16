from email import header
import json
from Settings import Settings
from DataToPostGis import DataToPostGisService
from DbToGeoserver import DbToGeoserver
from Database import DB
import time
from layerContrbution import Contirubute
from confiugration import Config

if __name__ == '__main__':
    setting = Settings.getSettingJson('setting.json')
    print(setting)
    # startTime=time.time()
    # service = DataToPostGisService('/home/noha/Penta-b/ClimateChange/shapefiles/admin_boundaries_gov/')
    # ListOfShapefiles = service.getShp()
    # print(ListOfShapefiles)
    # shape = service.importToDB()
    # print(time.time()-startTime)
    
    # startTimeGeoserverPublish=time.time()
    # database = DB()
    # tablesList = database.get_tables()
    # print(len(tablesList))
    # serviceGeoserver = DbToGeoserver()
    # layersName = serviceGeoserver.getLayers(Settings.settings['Geoserver']['Workspace'])
    # print(serviceGeoserver.postGisViewPublish(['admin_boundaries_gov']))
    # print(len(layersName))

    # print('geoserverpublish: ',time.time()-startTimeGeoserverPublish)
    
    # startTimecontribute=time.time()
    # print(serviceGeoserver.getWorkspaces())
    #print(setting)
    # serviceGeoserver = DbToGeoserver()
    #print(ListOfShapefiles)
    #print(shape)
    # workspaceList = serviceGeoserver.getWorkspaces()
    # print(workspaceList)
    #serviceGeoserver.createWorkspace(workspaceList)
    # notAllawedStores= serviceGeoserver.listGeoserverStores()
    # print(notAllawedStores)

    # for s in Stores:
    # requStores = Settings.settings['Geoserver']['Stores']
    # print(requStores)
    # serviceGeoserver.createDbStore(requStores,False)

    # startTimecontribute=time.time()
    # contribute = Contirubute()
    # layerResponse = contribute.requestConnect(['adminboundaries_sectors'])
    # print(layerResponse)
    # save = contribute.save(layerResponse)
    # print(save)
    # print('contribute: ',time.time()-startTimecontribute)
    #________________________#
    # timeDb = time.time()
    # database = DB()
    # tablesList = database.get_tables()
    # print(tablesList)
    # # createSQL = database.createView(tablesList)
    # # print(len(createSQL))
    # print('get tables', time.time()-timeDb)

    # startTimeGeoserverPublish=time.time()
    # layerList = database.get_views()
    # layerList = database.get_tables()
    # print(layerList)
    # serviceGeoserver = DbToGeoserver()
    # print(serviceGeoserver.postGisViewPublish(layerList))
    # serviceGeoserver.postGisSqlViewPublish(layerList)
    # layersName = serviceGeoserver.getLayers(Settings.settings['Geoserver']['Workspace'])
    # print(layersName)
    # print(len(layersName))
    # print('geoserverpublish: ',time.time()-startTimeGeoserverPublish)
    
    # startTimecontribute=time.time()
    # contribute = Contirubute()
    # layerResponse = contribute.requestConnect(layersName)
    # print(layerResponse)
    # save = contribute.save(layerResponse)
    # print(save)
    # print('contribute: ',time.time()-startTimecontribute)
    #______________________________#
    # config = Config()

    # tempreature = [
    #             "forecast:tas_degree_rf_1980_2005_monmin_values",
    #             "forecast:tas_degree_rf_1980_2005_monmean_values",
    #             "forecast:tas_degree_rf_1980_2005_monmax_values",
    #             "forecast:mean_of_air_temperature_at_2m_1981_2010_values",
    #             "forecast:mean_of_minimum_air_temperature_1981_2010_values",
    #             "forecast:mean_of_maximum_air_temperature_1981_2010_values",
    #             "forecast:temperature_djf_rcp45_values",
    #             "forecast:tas_degree_rcp45_2006_2100_monmean_nc_remap_values",
    #             "forecast:tas_degree_rcp45_2006_2100_monmin_nc_remap_values",
    #             "forecast:tas_degree_rcp45_2006_2100_monmax_nc_remap_values",
    #             "forecast:ndays_maxt_gt_35_rf_1980_2005_values",
    #             "forecast:ndays_maxt_gt_40_rf_1980_2005_values",
    #             "forecast:heat_waves_rf_1980_2005_3days_1_values",
    #             "forecast:nfdays_mint_lt_0_rf_1980_2005_values",
    #             "forecast:trnights_mint_gt_20_rf_1980_2005_nc_remap_values",
    #             "forecast:ndays_gt_10mm_rf_1980_2005_values",
    #             "forecast:ndays_gt_20mm_rf_1980_2005_values",
    #             "forecast:ndays_maxt_gt_35_rcp45_2006_2100_nc_remap_values",
    #             "forecast:ndays_maxt_gt_40_rcp45_2006_2100_nc_remap_values",
    #             "forecast:heat_waves_rcp45_2006_2100_3days_nc_remap_1_values",
    #             "forecast:nfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values",
    #             "forecast:trnights_mint_gt_20_rcp45_2006_2100_nc_remap_values",
    #             "forecast:ndays_gt_10mm_rcp45_2006_2100_nc_remap_values",
    #             "forecast:ndays_gt_20mm_rcp45_2006_2100_nc_remap_values",
    #             "forecast:ncdry_days_rcp45_2006_2100_1_values"
    #         ]
    # for t in tempreature:
    #     layerIds = config.getPermittedLayers(t)
    #     print(layerIds)
    # tocSetting = config.createPluginSetting(layerIds)
    # headerSetting = config.createHeaderPluginSetting()
    # chartSetting = config.creatChartPluginSetting()
    # print(chartSetting)
    # timeLineSetting = config.createTimelinePluginSetting()
    # print(headerSetting)
    # config.pluginConfig(chartSetting)
