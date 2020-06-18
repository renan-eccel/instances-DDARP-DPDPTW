import pandas as pd
import instance_importer

ROOT = '../benchmark/'

FOLDERS = ['ddarp/berbeglia_2012/cordeau_laporte_2003/json_dynamic_instances/',
           'ddarp/berbeglia_2012/ropke_etal_2007/json_dynamic_instances/',
           'dpdptw/fabri_and_recht_2006/json_instances/',
           'dpdptw/gendreau_etal_2006/json_instances/',
           'dpdptw/mitrovic-minic_etal_2003/json_instances/',
           'dpdptw/pankratz_2005/json_instances/',
           'dpdptw/pureza_laporte_2008/json_dynamic_instances/']

df_requests = instance_importer.build_all_dataframes(ROOT, FOLDERS)
pd.to_pickle(df_requests, './df_requests.zip')
