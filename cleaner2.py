import pandas as pd
import numpy as np
import re
import twokenize
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
from textblob import TextBlob
from datetime import timedelta
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import demoji
from statistics import mean

demoji.download_codes()

class Cleaner:

    #the Cleaner aims to maintain all information from within the dataset and simply aims 
    # to return a more readable/ informative version of it
    def __init__(self, data_type_dict, apostrophes, date_time_format_dict):

        self.apostrophes = apostrophes
        self.data_type_dict = data_type_dict
        self.date_time_format_dict = date_time_format_dict


        

    def clean(self, data):
        for key in self.data_type_dict:
            if self.data_type_dict[key] == "string":
                data[key] = data[key].transform(self.handle_apostrophes)
                data[key] = data[key].transform(self.convert_emojis)
                data[key] = data[key].transform(self.convert_emoticons)
                data[key] = data[key].transform(self.simplify_punctuation)
                data[key] = data[key].transform(self.normalize_whitespace)
                #data[key] = data[key].transform(self.correct_spelling)
                data[key].fillna("unknown", inplace=True)
                data[key].replace("?", "unknown", inplace=True)
                data[key].replace("nan", "unknown", inplace=True)

            elif self.data_type_dict[key] == "int":
                data[key] = data[key].transform(self.extract_numbers)
                data[key].fillna(data[key].mode()[0], inplace=True)

            elif self.data_type_dict[key] == "timezone":
                pass

            elif self.data_type_dict[key] == "datetime":

                data[key] = pd.to_datetime(data[key], format=self.date_time_format_dict[key], errors='coerce')
                self.date_mean = self.get_mean_date(data[key])
                print(self.date_mean)
                data[key].transform(self.date_imputer)

            else:
                print("Unknown datatype:", self.data_type_dict[key])

        data = data.transform(self.dates_and_times_corrector, axis=1)
        data.at[0, 'starttime'] -=timedelta(hours=7)
        data.at[0, 'endtime'] -=timedelta(hours=7) 

        return data


     #convert emoticons to text equivalent
    @staticmethod
    def convert_emoticons(text):
        try:
            for emot in EMOTICONS:
                text = re.sub(u'('+emot+')', (" ".join(EMOTICONS[emot].replace(",","").split()) + " emoticon."), text)  
            return text
        except TypeError:
            return np.NaN

    
    #convert emojis to text equivalent
    @staticmethod
    def convert_emojis(text):
        
        try:
            emojis = demoji.findall(text)
            for emot in emojis:
                text = text.replace(emot, (str(emojis[emot])+" emoji "))   
        except TypeError:
            pass
        
        return text
        
    
    def handle_apostrophes(self, sentence):

        try:
            apostrophes_expansion = self.apostrophes

            words = twokenize.tokenizeRawTweetText(sentence)

            processed_text = [apostrophes_expansion[word] if word in apostrophes_expansion else word for word in words]
            processed_text= " ".join(processed_text)
            
            return processed_text
        except AttributeError:
            return np.NaN

    @staticmethod
    def correct_spelling(sentence):
        try:
            return TextBlob(sentence).correct()
        except AttributeError:
            return np.NaN

    @staticmethod
    def simplify_punctuation(text):
        try:
            corrected = str(text)
            corrected = re.sub(r'([!?,;])\1+', r'\1', corrected)
            corrected = re.sub(r'\.{2,}', r'...', corrected)
            return corrected
        except AttributeError:
            return np.NaN

    #removes double whitespaces
    @staticmethod
    def normalize_whitespace(text):
        try:
            corrected = str(text)
            corrected = re.sub(r"//t",r"\t", corrected)
            corrected = re.sub(r"( )\1+",r"\1", corrected)
            corrected = re.sub(r"(\n)\1+",r"\1", corrected)
            corrected = re.sub(r"(\r)\1+",r"\1", corrected)
            corrected = re.sub(r"(\t)\1+",r"\1", corrected)
            return corrected.strip(" ")
        except AttributeError:
            return np.NaN

    #function that converts <x values to x
    @staticmethod
    def extract_numbers(item):
        try:
            number = re.search(r"\d+", item)
    

            if number == None:
                return np.NaN
            else:
                return int(number.group(0))
        except TypeError:
            return np.NaN
        except AttributeError:
            return np.NaN

    @staticmethod
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

    @staticmethod
    def get_mean_date(column):
        dates = pd.to_datetime(column).values.astype(np.int64)
        
        return pd.to_datetime(dates.mean())

    
    def date_imputer(self, value):
        if value == np.NaN:
            return self.date_mean
        else:
            return value





    