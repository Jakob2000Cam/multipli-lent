import pandas as pd
import os

from cleaner2 import Cleaner

apostrophe_dict = {
            "'s": "is",
            "'re": "are",
            "'r": "are",
            "'t": "not",
            "'m": "am",
            "'ll": "will",
            "'d": "would",
            "'ve": "have",
        }


#creates os independent paths to read and write data
read_path = os.path.join('data', 'original', 'labelled_october.csv')
write_path = os.path.join('data', 'processed', 'normalised_labelled_october3.csv')



column_name_dict = {"User Name": "username", "Job Role": "jobrole", "Who do you report into?": "instructor", "Company Name":"companyname", "Timezone":"timezone", "Company Size":"companysize", "Team Size": "teamsize", "Start Time":"starttime", "End Time":"endtime", "Last Sync":"lastsync", "Meeting Title": "meetingtitle", "Number of Guests":"noguest", "Tag":"tag"}
column_dict = {"username": "string", "jobrole": "string", "instructor": "string", "companyname":"string", "timezone":"timezone", "companysize":"int", "teamsize": "int", "starttime":"datetime", "endtime":"datetime", "lastsync":"datetime", "meetingtitle": "string", "noguest":"int", "tag":"string"}

date_format_dict = {"starttime":"%Y-%m-%dT%H:%M:%S.%fZ", "endtime":"%Y-%m-%dT%H:%M:%S.%fZ", "lastsync":"%m/%d/%Y"}

data_frame = pd.read_csv(read_path)

for key in column_name_dict:
    data_frame.rename(columns={key: column_name_dict[key]}, inplace=True)


cleaner = Cleaner(column_dict, apostrophe_dict, date_format_dict)

cleaned_data_frame = cleaner.clean(data_frame)

cleaned_data_frame.to_csv(write_path)