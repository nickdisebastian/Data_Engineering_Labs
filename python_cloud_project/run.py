#!/usr/bin python3

import requests
import json
import toml
import pandas as pd
from collections import ChainMap
import os
import subprocess


#reads API and returns response
def read_api(url):
    response = requests.get(url)
    return response.json()

# main function
if __name__=='__main__':
    app_config = toml.load('config.toml')
    url = app_config['api']['url']

    # read the API
    print('Reading the API...')
    data=read_api(url)
    print('API Reading Done!')

    # the company name
    print('Building the dataframe...')
    company_list = [data['results'][i]['company']['name'] for i in range(len(data['results']))]
    company_name = {'company':company_list}

    # the locations
    location_list = [data['results'][i]['locations'][0]['name'] for i in range(len(data['results']))]
    location_name = {'locations':location_list}
    
    # the job name
    job_list = [data['results'][i]['name'] for i in range(len(data['results']))]
    job_name = {'job':job_list}

    # the job type
    job_type_list = [data['results'][i]['type'] for i in range(len(data['results']))]
    job_type = {'job_type':job_type_list}

    # the publication date
    publication_date_list = [data['results'][i]['publication_date'] for i in range(len(data['results']))]
    publication_date = {'publication_date':publication_date_list}

    # merge the dictionaries and create data frame
    data = dict(ChainMap(company_name, location_name, job_name, job_type, publication_date))
    df=pd.DataFrame.from_dict(data)

    # Cut publication date to date
    df['publication_date'] = df['publication_date'].str[:10]

    # split location to city and country and drop the location column
    df['city'] = df['locations'].str.split(',').str[0]
    df['country'] = df['locations'].str.split(',').str[1]
    df.drop('locations', axis=1, inplace=True)

    # save the dataframe to a csv file locally first
    df.to_csv('jobs.csv', index=False)
    print('dataframe saved to local')

    # use linux command to upload file to S3
    subprocess.run(['aws', 's3', 'cp', 'jobs.csv', 's3://wcd-de-python-project/input/'])
  
    # Success.
    print('File uploading Done!')





    


    

