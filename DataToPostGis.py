import psycopg2
from psycopg2 import Error
import json
import os
import geopandas as gdf
from sqlalchemy import create_engine
import geoalchemy2
import time
from Settings import Settings



class DataToPostGisService:
    def __init__(self, dataDir):
        self.dataDir = dataDir
        self.shapefiles=[]

    def getShp(self):
        '''
        Input: path for data directory
        Output: list of shapefiles
        Examples: ['shapefile1','shapefile2']
        '''
        
        files = os.listdir(self.dataDir)
        for f in files:
            if f.endswith('.shp'):
                self.shapefiles.append(f.split(".")[0])
        return self.shapefiles


    def importToDB(self):
        """
        Input: list of shapefiles
        Output: 
        """
        ListOfShapefiles = self.shapefiles

        dbConnection = Settings.settings['DataBase']
        dbConnectionStr ="postgresql://{}:{}@{}:{}/{}".format(dbConnection['User'],dbConnection['Pass'],dbConnection['Host'],dbConnection['Port'],dbConnection['DB'])
        conn = create_engine(dbConnectionStr)
        

        for shp in ListOfShapefiles:
            finalName = self.dataDir+shp+'.shp'
            try:
                reader = gdf.read_file(finalName)
                df = gdf.GeoDataFrame(reader)
                db = df.to_postgis(shp,conn,schema=dbConnection['schema'])
            except Exception as error:
                print(shp, "is not valid, can't upload to postgres")
        #return db


    def shpToGeojson(self):
        pass

    def getFields(self):
        reader = self.shape
        pass


