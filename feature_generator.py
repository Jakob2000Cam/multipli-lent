from features import *
import pandas as pd
import os

#creates os independent paths to read and write data
read_path = os.path.join('data', 'processed', 'cleaned_labelled_october.pkl')
write_path = os.path.join('data', 'processed', 'features_october.pkl')

data_frame = pd.read_pickle(read_path)


def feature_creator(data_frame):

    userfullname = data_frame.apply(users_fullname, axis=1)
    workday = data_frame.apply(not_workday, axis=1)
    worktime = data_frame.apply(not_worktime, axis=1)
    usercompany = data_frame.apply(user_company_in_title, axis=1)
    onlyuserfirst = data_frame.apply(first_name_only, axis=1)
    #bracketsafterperson = data_frame.apply(brackets_following_person, axis=1)
    #andbetweenpersons = data_frame.apply(and_between_persons, axis=1)
    #firstnameandsurname = data_frame.apply(firstname_and_surname, axis=1)
    #onlyfirstname = data_frame.apply(only_firstname, axis=1)
    #personinmeeting = data_frame.apply(person_in_meeting, axis=1)
    teamspiritcheck = data_frame.apply(word_list_check, args=(teamspirit_keywords), axis=1)
    projectcheck = data_frame.apply(word_list_check, args=(project_keywords), axis=1)
    timekeywordscheck = data_frame.apply(word_list_check, args=(time_keywords), axis=1)
    onetoonecheck = data_frame.apply(word_list_check, args=(time_keywords), axis=1)
    broadcastcheck = data_frame.apply(word_list_check, args=(broadcast_keywords), axis=1)
    performancecheck = data_frame.apply(word_list_check, args=(performance_keywords), axis=1)
    irrelevantcheck = data_frame.apply(word_list_check, args=(irrelevant_keywords_all), axis=1)
    externalcheck = data_frame.apply(word_list_check, args=(external_keywords), axis=1)

    noguest = data_frame["noguest"]
    labels = data_frame['tag']

    feature_df = pd.DataFrame()

    feature_df["userfullname"] = userfullname
    feature_df["workday"] = workday
    feature_df["worktime"] = worktime
    feature_df["usercompany"] = usercompany
    feature_df["onlyuserfirst"] = onlyuserfirst
    #feature_df["bracketsafterperson"] = bracketsafterperson
    #feature_df["andbetweenpersons"] = andbetweenpersons
    #feature_df["firstnameandsurname"] = firstnameandsurname
    #feature_df["onlyfirstname"] = onlyfirstname
    #feature_df["personinmeeting"] = personinmeeting
    feature_df["teamspiritcheck"] = teamspiritcheck
    feature_df["projectcheck"] = projectcheck
    feature_df["timekeywordscheck"] = timekeywordscheck
    feature_df["onetoonecheck"] = onetoonecheck
    feature_df["broadcastcheck"] = broadcastcheck
    feature_df["performancecheck"] = performancecheck
    feature_df["irrelevantcheck"] = irrelevantcheck
    feature_df["externalcheck"] = externalcheck
    feature_df["noguest"] = noguest
    feature_df['labels'] = labels

    return feature_df

feature_frame =feature_creator(data_frame) 

feature_frame.to_pickle(write_path)