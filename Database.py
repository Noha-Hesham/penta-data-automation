import psycopg2
from psycopg2 import Error
import psycopg2.extras
from Settings import Settings
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import text
from sqlalchemy_views import CreateView,DropView

class DB:
    def __init__(self):
        self.settings = Settings.settings
        self.schema = Settings.settings['DataBase']['schema']
        self.tableName = Settings.settings['DataBase']['tableName']
        self.conn = self.getDbConnection()
        

    def getDbConnection(self):
        '''connection to db data source'''
        dbconn = self.settings['DataBase']

        try:
            conn = psycopg2.connect(
                user=dbconn['User'],
                password=dbconn['Pass'],
                host=dbconn['Host'],
                port=dbconn['Port'],
                database=dbconn['DB'])

            conn.autocommit = True
            return conn

        except (Exception, Error) as error:
            print("Postgres Error: ", error)

    def getCurser(self):
        if self.conn != None:
            curs = self.conn.cursor()
            return curs

    def get_tables(self):
        sql=f"SELECT distinct(table_name) FROM INFORMATION_SCHEMA.COLUMNS where table_schema = '{self.schema}' and udt_name = 'geometry'"
        cr = self.getCurser()
        cr.execute(sql)
        tables = cr .fetchall()
        # return tables
        return [table[0] for table in tables]

    def createView(self,tables=[]):
        setting = Settings.settings
        schema = setting['DataBase']['schema']
        joinSchema = setting['DataBase']['joinTables']
        targetSchema=setting['DataBase']['viewSchema']
        finalViewlist=[]
        location=''
        for table in tables:
            viewName = table
            if table not in ['NewCities','admin_boundaries_gov','admin_names','adminboundaries_sectors','adminboundaries_subsectors','bookmarks','climate_avg_sql_view__new','climate_avg_sql_view_new','extremely_wet_days_amount_ratio_RCP45_2006_2100_nc_remap_locati','extremely_wet_days_amount_ratio_RCP85_2006_2100_nc_remap_locati','location_50','location_262144','location_13225','location_5006','spatial_ref_sys']:
                if table in joinSchema['location_50']:

                    try:

                        location = 'location_50'

                        sql=f"""
                        CREATE OR REPLACE VIEW {targetSchema}.{viewName} as
                        SELECT l.ogc_fid id, l.gov_code, l.the_geom geom, l.gov_name_ar, l.gov_name_en, l.sec_name_ar, l.sec_name_en, l.ssec_name_ar, l.ssec_name_en, v.*
                        FROM {schema}."{location}" l
                        JOIN {schema}."{table}" v
                        ON l.ogc_fid = v.location_id
                        """
                        cr = self.getCurser()
                        cr.execute(sql)
                        # print('Done')
                        
                        finalViewlist.append(viewName)
                    except(Exception, Error) as error:
                            print(f"Postgres Error:{table}>> ", error)


                elif table in joinSchema['location_262144']:
                    try: 
                        location = 'location_262144'

                        sql=f"""
                        CREATE OR REPLACE VIEW {targetSchema}.{viewName} as
                        SELECT l.ogc_fid id, l.gov_code, l.the_geom geom, l.gov_name_ar, l.gov_name_en, l.sec_name_ar, l.sec_name_en, l.ssec_name_ar, l.ssec_name_en, v.*
                        FROM {schema}."{location}" l
                        JOIN {schema}."{table}" v
                        ON l.ogc_fid = v.location_id
                        """
                        cr = self.getCurser()
                        cr.execute(sql)
                        # print('Done')
                        finalViewlist.append(viewName)
                    except(Exception, Error) as error:
                            print(f"Postgres Error:{table}>> ", error)

                elif table in joinSchema['location_5006']:
                    try:

                        location = 'location_5006'

                        sql=f"""
                        CREATE OR REPLACE VIEW {targetSchema}.{viewName} as
                        SELECT l.ogc_fid id, l.gov_code, l.the_geom geom, l.gov_name_ar, l.gov_name_en, l.sec_name_ar, l.sec_name_en, l.ssec_name_ar, l.ssec_name_en, v.*
                        FROM {schema}."{location}" l
                        JOIN {schema}."{table}" v
                        ON l.ogc_fid = v.location_id
                        """
                        cr = self.getCurser()
                        cr.execute(sql)
                        # print('Done')
                        finalViewlist.append(viewName)
                    except(Exception, Error) as error:
                            print(f"Postgres Error:{table}>> ", error)

                else:

                    location = 'location_13225'
                    try:
                        sql=f"""
                        CREATE OR REPLACE VIEW {targetSchema}.{viewName} as
                        SELECT l.ogc_fid id, l.gov_code, l.the_geom geom, l.gov_name_ar, l.gov_name_en, l.sec_name_ar, l.sec_name_en, l.ssec_name_ar, l.ssec_name_en, v.*
                        FROM {schema}."{location}" l
                        JOIN {schema}."{table}" v
                        ON l.ogc_fid = v.location_id
                        """
                        cr = self.getCurser()
                        cr.execute(sql)
                        finalViewlist.append(viewName)
                        # print('Done')
                    except(Exception, Error) as error:
                            print(f"Postgres Error:{table}>> ", error)

        return finalViewlist

    def get_views(self):

        setting = Settings.settings
        schema = setting['DataBase']['viewSchema']
        sql=f"""
        SELECT table_name
        FROM information_schema.views
        WHERE table_schema = '{schema}'
        """
        cr = self.getCurser()
        cr.execute(sql)
        tables = cr .fetchall()

        return [table[0] for table in tables]


