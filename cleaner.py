import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from datetime import timedelta
import numpy as np
import re
import os

#creates os independent paths to read and write data
read_path = os.path.join('data', 'processed','validation.csv')
write_path = os.path.join('data', 'processed', 'cleaned_validation_october.pkl')

col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize',
			 'teamsize', 'starttime', 'endtime', 'lastsync', 'meetingtitle', 'noguest', 'tag']
data_frame = pd.read_csv(read_path, header=0, names=col_names)

#impute numeric and string type columns
def impute_columns(data, col_names):

    text_imputer = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.NaN, strategy='constant', fill_value="unknown"))
    ])
    
    numeric_imputer = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.NaN, strategy="most_frequent"))
    ])


    preprocessor = ColumnTransformer(transformers=[('text_imputer', text_imputer, ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'meetingtitle', 'tag']),
    ('numeric_imputer', numeric_imputer, ['teamsize', 'companysize', 'noguest'])])

    preprocessed_data = preprocessor.fit_transform(data)
    data = pd.concat([pd.DataFrame(data=preprocessed_data, columns=['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'meetingtitle', 'tag', 'teamsize', 'companysize', 'noguest']), data[['starttime', 'endtime', 'lastsync']]], axis=1)
    return data

def data_cleaner(data):
    data['companysize'] = data['companysize'].transform(extract_numbers)
    data['teamsize'] = data['teamsize'].transform(extract_numbers)
    data['starttime'] = pd.to_datetime(data['starttime'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
    data['endtime'] = pd.to_datetime(data['endtime'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
    data['lastsync'] = pd.to_datetime(data['lastsync'], format='%m/%d/%Y', errors='coerce')
    data['noguest'] = pd.to_numeric(data['noguest'], errors='coerce').fillna(0).astype(np.int64)
    data = data.transform(dates_and_times_corrector, axis=1)

    return data


#function that converts <x values to x
def extract_numbers(item):
    try:
        number = re.search(r"\d+", item)
 

        if number == None:
            return np.NaN
        else:
            return int(number.group(0))
    except TypeError:
       return np.NaN


#corrects the start time in a datetime object with the correct timezone
def dates_and_times_corrector(meeting):

    #converts start and end strings into datetime objects
    start_datetime = meeting["starttime"]
    end_datetime = meeting["endtime"]

    #finds the timechange of the datetime due to the timezone
    if meeting["timezone"] == "":
        time_change = 0
    elif  "+" in str(meeting["timezone"]):
        time_change = int(re.findall(r"\d+", meeting["timezone"])[0])
    elif  "-" in str(meeting["timezone"]):
        time_change = -int(re.findall(r"\d+", meeting["timezone"])[0])
    else:
        time_change = 0

    #changes the datetime by the timezone
    
    start_datetime = start_datetime + timedelta(hours = time_change)
    
    end_datetime = end_datetime + timedelta(hours = time_change)

    #updates the meeting
    meeting["starttime"] = start_datetime
    meeting["endtime"] = end_datetime
    
    return meeting


cleaned_data = data_cleaner(data_frame)

#the following is necessary because the pd.transform applies to the first row twice by design
#if you know how to fix this, please do so and let me know at jab302@cam.ac.uk
cleaned_data.at[0, 'starttime'] -=timedelta(hours=7)
cleaned_data.at[0, 'endtime'] -=timedelta(hours=7) 


cleaned_data = impute_columns(cleaned_data, col_names)

cleaned_data.to_pickle(write_path)