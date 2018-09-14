import json
import os
import pandas as pd


def for_all_files_in(directory):
    for filename in os.listdir(directory):
        create_dataframe(directory, filename)


def create_dataframe(directory, filename):
    df = pd.read_csv(directory + filename, sep=" ")
    df.columns = ['request_arrival_time',
                  'pickup_service_time',
                  'pickup_x_coord', 'pickup_y_coord',
                  'pickup_lower_tw', 'pickup_upper_tw',
                  'delivery_service_time',
                  'delivery_x_coord', 'delivery_y_cooord',
                  'delivery_lower_tw', 'delivery_upper_tw',
                  'garbage']
    last_row = df.shape[0]-1
    df = df.drop(labels='garbage', axis=1).drop(last_row, axis=0)
    return df.transpose()


directory = "./requests/"
filetest = "req_rapide_1_240_24.txt"

df = create_dataframe(directory, filetest)
df_json = df.to_json()
