from geo.Geoserver import Geoserver
from DataToPostGis import Settings
import requests

class DbToGeoserver:
    def __init__(self):
        self.geoserverConnect()

    def geoserverConnect(self):
        setting = Settings.settings['Geoserver']
        host=setting['Host']
        port = setting['Port']
        user = setting['User']
        password = setting['Pass']

        self.connection = Geoserver(f'http://{host}:{port}/geoserver',username=f'{user}',password=f'{password}')
        


    def getWorkspaces(self):
        conn = self.connection
        existingWorkspacees = []
        workspaces = conn.get_workspaces()['workspaces']['workspace']
        for w in workspaces:
            existingWorkspacees.append(w['name'])

        return existingWorkspacees
        
    def createWorkspace(self,WsList):
        """create workspace """
        conn = self.connection
        requiredWorkspace = Settings.settings['Geoserver']['Workspace']
        if requiredWorkspace not in WsList:
            createWorkspace = conn.create_workspace(requiredWorkspace)
            print(createWorkspace)
        else:
            print(conn.create_workspace(requiredWorkspace))

        
    def listGeoserverStores(self):
        """Output: return list of stores in specific workspace"""
        storeList=[]
        workspace = Settings.settings['Geoserver']['Workspace']
        stores = self.connection.get_datastores(workspace)['dataStores']['dataStore']
        for s in stores:
            storeList.append(s['name'])
        return storeList

    def createFeatureStore(self,store,overwriteStatus,schema):
        return self.connection.create_featurestore(
            store_name=store,
            schema=schema,
            workspace=Settings.settings['Geoserver']['Workspace'],
            db=Settings.settings['DataBase']['DB'],
            host=Settings.settings['DataBase']['privateIP'],
            port=Settings.settings['DataBase']['Port'],
            pg_user=Settings.settings['DataBase']['User'],
            pg_password=Settings.settings['DataBase']['Pass'],
            expose_primary_keys=True,
            overwrite=overwriteStatus
        )

    def createDbStore(self,requStores,overwrite=False):
        
        for store in requStores:
            # if store not in notAllawedStores:
            try:
                self.createFeatureStore(store,overwriteStatus=False,schema=Settings.settings['DataBase']['schema'])
                return store
            except(Exception) as error:
                                print(error)

            # else:
            #     overwrite=input(f'Do you want to overwrite the store{store}?(Y/N)')
            #     if overwrite == 'Y':
            #         overwrite = True
            #         self.createFeatureStore(store,overwriteStatus=True)
            #     else:
            #         break
                


    def postGisLayerPublish(self):
        pass
    
    def postGisViewPublish(self,layerList=[]):
        """
        get all layers from workspace > filter > append to list > publish all layers in the list.
        """

        for table in layerList:
            publish = self.connection.publish_featurestore(Settings.settings['Geoserver']['publishToStore'],table,Settings.settings['Geoserver']['Workspace'])
        print(publish)    
        return layerList

    def postGisSqlViewPublish(self,layerList=[]):
        
        table = ''
        setting = Settings.settings
        schema = setting['DataBase']['schema']
        joinSchema = setting['DataBase']['joinTables']
        store = setting['Geoserver']['publishToStore']
        workspace = setting['Geoserver']['Workspace']
        host = setting['Geoserver']['Host']
        port = setting['Geoserver']['Port']
        yearList = [
            'ncdry_days_rcp45_2006_2100_2_values',
                    'ncdry_days_rcp45_2006_2100_1_values',
                    'ncdry_days_rcp85_2006_2100_1_values',
                    'ncdry_days_rf_1980_2005_2_values',
                    'ncdry_days_rf_1980_2005_1_values',
                    'ndays_gt_10mm_rcp45_2006_2100_nc_remap_values',
                    'ndays_gt_10mm_rf_1980_2005_values',
                    'ndays_gt_10mm_rcp85_2006_2100_nc_remap_values',
                    'ndays_gt_20mm_rcp85_2006_2100_nc_remap_values',
                    'ndays_gt_20mm_rf_1980_2005_values',
                    'ndays_gt_20mm_rcp45_2006_2100_nc_remap_values',
                    'ndays_maxt_gt_35_rf_1980_2005_values',
                    'ndays_maxt_gt_40_rf_1980_2005_values',
                    'ndays_maxt_gt_40_rcp85_2006_2100_nc_remap_values',
                    'ndays_maxt_gt_35_rcp85_2006_2100_nc_remap_values',
                    'ndays_maxt_gt_35_rcp45_2006_2100_nc_remap_values',
                    'ndays_maxt_gt_40_rcp45_2006_2100_nc_remap_values',
                    'trnights_mint_gt_30_rf_1980_2005_values',
                    'trnights_mint_gt_30_rcp45_2006_2100_nc_remap_values',
                    'trnights_mint_gt_30_rcp85_2006_2100_nc_remap_values',
                    'trnights_mint_gt_20_rcp45_2006_2100_nc_remap_values',
                    'trnights_mint_gt_20_rcp85_2006_2100_nc_remap_values',
                    'trnights_mint_gt_20_rf_1980_2005_nc_remap_values',
                    'heat_waves_rf_1980_2005_3days_2_values',
                    'heat_waves_rf_1980_2005_3days_1_values',
                    'heat_waves_rcp85_2006_2100_3days_nc_remap_1_values',
                    'heat_waves_rcp85_2006_2100_3days_nc_remap_2_values',
                    'heat_waves_rcp45_2006_2100_3days_nc_remap_2_values',
                    'heat_waves_rcp45_2006_2100_3days_nc_remap_1_values',
                    'nfdays_mint_lt_0_rcp85_2006_2100_nc_remap_values',
                    'nfdays_mint_lt_0_rf_1980_2005_values',
                    'nfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values',
                    'rainfall_djf_rcp45_values',
                    'rainfall_djf_rcp85_values',
                    'rainfall_jja_rcp85_values',
                    'rainfall_jja_rcp45_values',
                    'rainfall_son_rcp45_values',
                    'rainfall_son_rcp85_values',
                    'rainfall_mam_rcp85_values',
                    'rainfall_mam_rcp45_values',
                    'temperature_mam_rcp85_values',
                    'temperature_mam_rcp45_values',
                    'temperature_jja_rcp85_values',
                    'temperature_jja_rcp45_values',
                    'temperature_djf_rcp85_values',
                    'temperature_djf_rcp45_values',
                    'temperature_son_rcp85_values',
                    'temperature_son_rcp45_values',
                    'rf_percent_dust_75p_1980_2005_nc_remap_values',
                    'rf_percent_dust_90p_1980_2005_nc_remap_values',
                    'rf_percent_dust_95p_1980_2005_nc_remap_values',
                    'rf_percent_dust_99p_1980_2005_nc_remap_values',
                    'rcp45_percent_dust_75p_2006_2100_nc_remap_values',
                    'rcp45_percent_dust_90p_2006_2100_nc_remap_values',
                    'rcp45_percent_dust_95p_2006_2100_nc_remap_values',
                    'rcp45_percent_dust_99p_2006_2100_nc_remap_values',
                    'rcp85_percent_dust_75p_2006_2100_nc_remap_values',
                    'rcp85_percent_dust_90p_2006_2100_nc_remap_values',
                    'rcp85_percent_dust_95p_2006_2100_nc_remap_values',
                    'rcp85_percent_dust_99p_2006_2100_nc_remap_values',
                    'trnights_mint_gt_25_rcp45_2006_2100_nc_remap_values',
                    'trnights_mint_gt_25_rcp85_2006_2100_nc_remap_values',
                    'trnights_mint_gt_25_rf_1980_2005_nc_remap_values']
        monthList = ['moderate_wet_days_percent_rf_1980_2005_nc_remap_values', 'moderate_wet_days_percent_rcp85_2006_2100_nc_remap_values', 'moderate_wet_days_percent_rcp45_2006_2100_nc_remap_values', 'moderate_wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'moderate_wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'moderate_wet_days_amount_ratio_rf_1980_2005_values', 'wet_days_percent_rcp85_2006_2100_nc_remap_values', 'wet_days_percent_rf_1980_2005_nc_remap_values', 'wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'wet_days_percent_rcp45_2006_2100_nc_remap_values', 'wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'wet_days_amount_ratio_rf_1980_2005_nc_remap_values', 'extremely_wet_days_percent_rcp85_2006_2100_nc_remap_values', 'extremely_wet_days_percent_rcp45_2006_2100_nc_remap_values', 'extremely_wet_days_amount_ratio_rf_1980_2005_nc_remap_values', 'extremely_wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'extremely_wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'extremely_wet_days_percent_rf_1980_2005_nc_remap_values', 'ndays_gt_25mm_rcp85_2006_2100_nc_remap_values', 'ndays_gt_25mm_rcp45_2006_2100_nc_remap_values', 'ndays_gt_25mm_rf_1980_2005_nc_remap_values', 'sdii_rcp85_2006_2100_nc_remap_values', 'sdii_rcp45_2006_2100_nc_remap_values', 'sdii_rf_1980_2005_nc_remap_values', 'nwet_days_rcp45_2006_2100_nc_remap_values', 'nwet_days_rcp85_2006_2100_nc_remap_values', 'nwet_days_rf_1980_2005_nc_remap_values', 'very_wet_days_amount_ratio_rcp85_2006_2100_nc_remap_values', 'very_wet_days_amount_ratio_rcp45_2006_2100_nc_remap_values', 'very_wet_days_amount_ratio_rf_1980_2005_nc_remap_values', 'very_wet_days_percent_rcp85_2006_2100_nc_remap_values', 'very_wet_days_percent_rf_1980_2005_nc_remap_values', 'very_wet_days_percent_rcp45_2006_2100_nc_remap_values', 'max_pr_rcp45_monthly_2006_2100_nc_remap_values', 'max_pr_rf_yearly_1980_2005_nc_remap_values', 'max_pr_rf_monthly_1980_2005_nc_remap_values', 'max_pr_rcp45_yearly_2006_2100_nc_remap_values', 'max_pr_rcp85_yearly_2006_2100_nc_remap_values', 'max_pr_rcp85_monthly_2006_2100_nc_remap_values', 'sund_hour_rcp85_2006_2100_monsum_nc_remap_values', 'hurs_rcp85_2006_2100_monmin_nc_remap_values', 'sfcWind_rcp85_2006_2100_monmean_nc_remap_values', 'tas_degree_rcp85_2006_2100_monmax_nc_remap_values', 'psl_rcp85_2006_2100_monmean_nc_remap_values', 'sfcWind_rcp85_2006_2100_monmax_nc_remap_values', 'tas_degree_rcp85_2006_2100_monmin_nc_remap_values', 'hurs_rcp85_2006_2100_monmean_nc_remap_values', 'sfcWind_rcp85_2006_2100_monmin_nc_remap_values', 'tas_degree_rcp85_2006_2100_monmean_nc_remap_values', 'hurs_rcp85_2006_2100_monmax_nc_remap_values', 'pr_mm_rcp85_2006_2100_monsum_nc_remap_values', 'sfcwind_rcp45_2006_2100_monmean_nc_remap_values', 'hurs_rcp45_2006_2100_monmin_nc_remap_values', 'hurs_rcp45_2006_2100_monmean_nc_remap_values', 'hurs_rcp45_2006_2100_monmax_nc_remap_values', 'tas_degree_rcp45_2006_2100_monmax_nc_remap_values', 'sfcwind_rcp45_2006_2100_monmin_nc_remap_values', 'psl_rcp45_2006_2100_monmean_nc_remap_values', 'sfcwind_rcp45_2006_2100_monmax_nc_remap_values', 'tas_degree_rcp45_2006_2100_monmin_nc_remap_values', 'sund_hour_rcp45_2006_2100_monsum_nc_remap_values', 'tas_degree_rcp45_2006_2100_monmean_nc_remap_values', 'pr_mm_rcp45_2006_2100_monsum_nc_remap_values', 'cold_waves_rcp45_2006_2100_3days_nc_remap_values', 'cold_waves_rf_1980_2005_3days_nc_remap_values', 'cold_waves_rcp85_2006_2100_3days_nc_remap_values', 'cold_spells_rf_1980_2005_nc_remap_values', 'cold_spells_rcp85_2006_2100_nc_remap_values', 'cold_spells_rcp45_2006_2100_nc_remap_values', 'warm_nights_percent_rf_1980_2005_values', 'very_cold_days_percent_rcp45_2006_2030_values', 'cold_nights_percent_rf_1980_2005_values', 'warm_days_percent_rf_1980_2005_values', 'warm_nights_percent_rcp45_2006_2030_values', 'cold_days_percent_rcp85_2006_2030_values', 'very_warm_days_percent_rf_1980_2005_values', 'cold_days_percent_rf_1980_2005_values', 'cold_days_percent_rcp45_2006_2030_values', 'very_cold_days_percent_rf_1980_2005_values', 'very_warm_days_percent_rcp45_2006_2030_values', 'cold_nights_percent_rcp85_2006_2030_values', 'cold_nights_percent_rcp45_2006_2030_values', 'warm_nights_percent_rcp85_2006_2030_values', 'warm_days_percent_rcp45_2006_2030_values', 'warm_days_percent_rcp85_2006_2030_values', 'very_cold_days_percent_rcp85_2006_2030_values', 'very_warm_days_percent_rcp85_2006_2030_values', 'ndays_maxt_gt_25_rf_1980_2005_nc_remap_values', 'ndays_maxt_gt_25_rcp85_2006_2100_nc_remap_values', 'ndays_maxt_gt_25_rcp45_2006_2100_nc_remap_values', 'ndays_maxt_gt_45_rcp45_2006_2100_nc_remap_values', 'ndays_maxt_gt_45_rf_1980_2005_nc_remap_values', 'ndays_maxt_gt_30_rcp85_2006_2100_nc_remap_values', 'ndays_maxt_gt_45_rcp85_2006_2100_nc_remap_values', 'ndays_maxt_gt_30_rf_1980_2005_nc_remap_values', 'ndays_maxt_gt_30_rcp45_2006_2100_nc_remap_values', 'warm_spells_rf_1980_2005_nc_remap_values', 'warm_spells_rcp85_2006_2100_nc_remap_values', 'warm_spells_rcp45_2006_2100_nc_remap_values', 'ncfdays_mint_lt_0_rf_1980_2005_nc_remap_values', 'ncfdays_mint_lt_0_rcp85_2006_2100_nc_remap_values', 'ncfdays_mint_lt_0_rcp45_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_40_rf_1980_2005_nc_remap_values', 'ncsudays_maxt_gt_30_rf_1980_2005_nc_remap_values', 'ncsudays_maxt_gt_40_rcp45_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_45_rcp85_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_30_rcp45_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_35_rcp85_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_30_rcp85_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_35_rcp45_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_35_rf_1980_2005_nc_remap_values', 'ncsudays_maxt_gt_40_rcp85_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_45_rcp45_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_25_rf_1980_2005_nc_remap_values', 'ncsudays_maxt_gt_25_rcp45_2006_2100_nc_remap_values', 'ncsudays_maxt_gt_35_rf_1980_2005_values', 'ncsudays_maxt_gt_45_rf_1980_2005_nc_remap_values', 'tas_degree_rf_1980_2005_monmax_values', 'tas_degree_rf_1980_2005_monmin_values', 'relhumid_rf_1980_2005_monmean_values', 'tas_degree_rf_1980_2005_monmean_values', 'sund_rf_1980_2005_monsum_values', 'sfcwind_rf_1980_2005_monmin_nc_remap_values', 'pr_rf_1980_2005_monsum_mm_month_values', 'relhumid_rf_1980_2005_monmax_values', 'psl_rf_1980_2005_monmean_values', 'relhumid_rf_1980_2005_monmin_values', 'sfcwind_rf_1980_2005_monmean_nc_remap_values', 'sfcwind_rf_1980_2005_monmax_nc_remap_values', 'potential_evapotranspiration_rcp45_2006_2100_remap_values', 'potential_evapotranspiration_rf_1980_2005_remap_values', 'potential_evapotranspiration_rcp85_2006_2100_remap_values', 'moderate_wet_days_amount_ratio_rf_2006_2100_nc_remap_values', 'mean_of_air_temperature_at_2m_1981_2010_values', 'mean_of_maximum_air_temperature_1981_2010_values', 'mean_of_minimum_air_temperature_1981_2010_values', 'mean_of_monthly_total_precipita_1981_2010_values', 'mean_of_relative_humidity_1981_2010_values', 'mean_sea_level_pressure_1981_2010_values']
        notAllawedTables = ['NewCities','admin_boundaries_gov','admin_names','adminboundaries_sectors','adminboundaries_subsectors','bookmarks','climate_avg_sql_view__new','climate_avg_sql_view_new','extremely_wet_days_amount_ratio_RCP45_2006_2100_nc_remap_locati','extremely_wet_days_amount_ratio_RCP85_2006_2100_nc_remap_locati','location_50','location_262144','location_13225','location_5006','spatial_ref_sys']
        headers = {'Content-Type': 'application/xml' , 'Accept-Encoding':'gzip, deflate, br' , 'Connection' : 'keep-alive' , 'Accept':'*/*'}
        auth = (setting['Geoserver']['User'], setting['Geoserver']['Pass'])
        url = f"http://{host}:{port}/geoserver/rest/workspaces/{workspace}/datastores/{store}/featuretypes/"
        
        for table in layerList:
            if table not in notAllawedTables:
                if table in monthList:
                    
                    for i in joinSchema['location_50']: 
                        location = 'location_50'
                        if table.startswith(i):
                            
                            try:
                                response = requests.request("POST", url, headers=headers, data=self.generateMonthBody("location_50",table,store),auth=auth)
                                # print(response.text)
                                if response.status_code != 201:
                                    print(table)
                                continue
                            except(Exception) as error:
                                print(error)

                    for i in joinSchema['location_262144']:
                        location = 'location_262144'
                        if table.startswith(i):
                            
                            try:
                                response = requests.request("POST", url, headers=headers, data=self.generateMonthBody("location_262144",table,store),auth=auth)
                                # print(response.text)
                                if response.status_code != 201:
                                    print(table)
                                continue

                            except(Exception) as error:
                                print(error)

                    for i in joinSchema['location_5006']:
                        location = 'location_5006'
                        if table.startswith(i):
                            
                            try:
                                response = requests.request("POST", url, headers=headers, data=self.generateMonthBody("location_5006",table,store),auth=auth)
                                # print(response.text)
                                if response.status_code != 201:
                                    print(table)
                                continue

                            except(Exception) as error:
                                print(error)

                    location = 'location_13225'
                    try:
                        response = requests.request("POST", url, headers=headers, data=self.generateMonthBody("location_13225",table,store),auth=auth)
                        # print(response.text)
                        if response.status_code != 201:
                            print(table)
                            print(response.text)
                        continue
                    except(Exception) as error:
                        print(error)

                else:
                    
                    
                    for i in joinSchema['location_50']:
                        location = 'location_50'
                        if table.startswith(i):
                            
                            try:
                                response = requests.request("POST", url, headers=headers, data=self.generateYearBody("location_50",table,store),auth=auth)
                                # print(response.text)
                                if response.status_code != 201:
                                    print(table)
                                continue

                            except(Exception) as error:
                                print(error)

                    for i in joinSchema['location_262144']:
                        location = 'location_262144'
                        if table.startswith(i):
                            
                            try:
                                response = requests.request("POST", url, headers=headers, data=self.generateYearBody("location_262144",table,store),auth=auth)
                                # print(response.text)
                                if response.status_code != 201:
                                    print(table)
                                continue

                            except(Exception) as error:
                                print(error)

                    for i in joinSchema['location_5006']:
                        location = 'location_5006'
                        if table.startswith(i):
                            
                            try:
                                response = requests.request("POST", url, headers=headers, data=self.generateYearBody("location_5006",table,store),auth=auth)
                                # print(response.text)
                                if response.status_code != 201:
                                    print(table)
                                continue

                            except(Exception) as error:
                                print(error)
                                
                    location = 'location_13225'
                    try:
                        # print(self.generateYearBody('location_13225',table,store))
                        response = requests.post( url, headers=headers, data=self.generateYearBody('location_13225',table,store),auth=auth)
                        # print(response.text)
                        if response.status_code != 201:
                            print(table)
                            print(response.text)
                        continue
                    except(Exception) as error:
                        print(error)


    def generateMonthBody(self,location,table,store):
        
        bodyMonth = f'''
                    <featureType>
    <name>{table}</name>
    <enabled>true</enabled>
    <namespace>
        <name>{store}</name>
    </namespace>
    <title>{table}</title>
    <srs>EPSG:4326</srs>
    <metadata>
        <entry key="JDBC_VIRTUAL_TABLE">
            <virtualTable>
                <name>{table}</name>
                <sql>SELECT l.ogc_fid AS id,
                            l.gov_code,
                            l.the_geom AS geom,
                            l.gov_name_ar,
                            l.gov_name_en,
                            l.sec_name_ar,
                            l.sec_name_en,
                            l.ssec_name_ar,
                            l.ssec_name_en,
                            avg(v.value) AS value
                        FROM {location} l
                        JOIN "{table}" v 
                        ON l.ogc_fid = v.location_id
                        WHERE (v.year between %y_from% and %y_to%)
                        and (v.month between %m_from% and %m_to%)
                        GROUP BY l.ogc_fid, l.gov_code,l.gov_name_ar,l.gov_name_en,l.sec_name_ar,l.sec_name_en,l.ssec_name_ar,l.ssec_name_en, l.the_geom</sql>
                <escapeSql>true</escapeSql>
                <keyColumn>id</keyColumn>
                <geometry>
                    <name>geom</name>
                    <type>Point</type>
                    <srid>4326</srid>
                </geometry>
                <parameter>
                    <name>y_from</name>
                    <defaultValue>2006</defaultValue>
                    <regexpValidator>.*</regexpValidator>
                </parameter>
                <parameter>
                    <name>y_to</name>
                    <defaultValue>2010</defaultValue>
                    <regexpValidator>.*</regexpValidator>
                </parameter>
                <parameter>
                    <name>m_from</name>
                    <defaultValue>1</defaultValue>
                    <regexpValidator>.*</regexpValidator>
                </parameter>
                <parameter>
                    <name>m_to</name>
                    <defaultValue>12</defaultValue>
                    <regexpValidator>.*</regexpValidator>
                </parameter>
            </virtualTable>
        </entry>
    </metadata>
</featureType>
                        '''
        return bodyMonth
    
    def generateYearBody(self,location,table,store):
        
        bodyYear = f'''
                    <featureType>
    <name>{table}</name>
    <enabled>true</enabled>
    <namespace>
        <name>{store}</name>
    </namespace>
    <title>{table}</title>
    <srs>EPSG:4326</srs>
    <metadata>
        <entry key="JDBC_VIRTUAL_TABLE">
            <virtualTable>
                <name>{table}</name>
                <sql>SELECT l.ogc_fid AS id,
                            l.gov_code,
                            l.the_geom AS geom,
                            l.gov_name_ar,
                            l.gov_name_en,
                            l.sec_name_ar,
                            l.sec_name_en,
                            l.ssec_name_ar,
                            l.ssec_name_en,
                            avg(v.value) AS value
                        FROM {location} l
                        JOIN "{table}" v 
                        ON l.ogc_fid = v.location_id
                        WHERE (v.year between %y_from% and %y_to%)
                        GROUP BY l.ogc_fid, l.gov_code,l.gov_name_ar,l.gov_name_en,l.sec_name_ar,l.sec_name_en,l.ssec_name_ar,l.ssec_name_en, l.the_geom</sql>
                <escapeSql>true</escapeSql>
                <keyColumn>id</keyColumn>
                <geometry>
                    <name>geom</name>
                    <type>Point</type>
                    <srid>4326</srid>
                </geometry>
                <parameter>
                    <name>y_from</name>
                    <defaultValue>2006</defaultValue>
                    <regexpValidator>.*</regexpValidator>
                </parameter>
                <parameter>
                    <name>y_to</name>
                    <defaultValue>2010</defaultValue>
                    <regexpValidator>.*</regexpValidator>
                </parameter>
            </virtualTable>
        </entry>
    </metadata>
</featureType>
                        '''

        return bodyYear


    def getLayers(self,workspace=''):
        workspace = Settings.settings['Geoserver']['Workspace']
        layers = self.connection.get_layers(workspace)
        return [workspace+':'+l['name'] for l in layers['layers']['layer']]
        