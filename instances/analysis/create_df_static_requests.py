import pandas as pd
import instance_importer

ROOT = '../benchmark/'
FOLDERS = ['ddarp/berbeglia_2012/cordeau_laporte_2003/json_static_instances/',
           'ddarp/berbeglia_2012/ropke_etal_2007/json_static_instances/',
           'pdptw/li_lim_2003/json_instances/pdp_100/',
           'pdptw/li_lim_2003/json_instances/pdp_200/',
           'pdptw/li_lim_2003/json_instances/pdp_400/',
           'pdptw/li_lim_2003/json_instances/pdp_600/',
           'pdptw/li_lim_2003/json_instances/pdptw800/',
           'pdptw/li_lim_2003/json_instances/pdptw1000/',
           ]
df_static_requests = instance_importer.build_all_dataframes(ROOT, FOLDERS)
pd.to_pickle(df_static_requests, './df_static_requests.zip')
