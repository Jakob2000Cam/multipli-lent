# Multiplii Hackbridge Project
&nbsp;
**Please refer to [Multiplii](https://www.multiplii.io/) for details on the product.**
&nbsp;

---
## Contents

* Structure of the repository
* How to use this
* Outline of general workflow
* Technical documentation

## Structure of the repository

All python files are contained in the root directory. The data directory contains the original and processed folders, which contain data before and after any type of processing respectively.

## How to use this

In order to develop this code please ask the owner of the directory to make you a developerand install git, then please run the following in your terminal.

`git clone https://github.com/Jakob2000Cam/multipli-lent.git`

`git checkout -b insert-your-name`

Please make sure that you don't develop in the main branch, by running `git branch` and ensuring that the asterisk is next to your own branch rather than the main branch.

## General Approach

* Preprocess text to get it as close to natural language as possible
* Use a NER to filter out names and replace with the generic terms eg "John" could be replaced with "manager"
* Use transfer learning to retrain a trained word embedding it on the labelled dataset
* Normalise numerical features
* Train two classifiers, for meeting type and "impactfulness"
* Use active learning to label more data and improve the classifiers
* Use unsupervised clustering algorithm to group together similar people in order to personalise nudge suggestions


## Technical documentation

This documentation outlines the functionality of the code and explains all the statistical decisions made along the process. It is intended as an aid for future developers.

**main**

This file runs the main pipeline, loads in a csv file and uses the other modules to clean and preprocess that file. It will also be used to train the model.

**cleaner2**

Replaces the old cleaner and normaliser files. This normalises text, extracts entities etc. Numerical values are imputed using the mode and datetime values are imputed using the mean. Has issues imputing enddates, but shouldn't matter too much as the variance on those will too large for it to be a useful feature. Could maybe think about using mean time later. Need to make sure that we don't run into issues with NaT values.

**cleaner**

This file is responsible for cleaning data. It loads a csv file in from the data/original path as a pandas dataframe and changes column names for ease of use. It then applies a number of functions outlined below and stores data as a pkl file in order to preserve all features within the data/processed directory.

*Note: the pandas.transform operates twice on the first row of the dataframe. As a result we manually subtract the introduced error. Ideally we would prevent this from happening in the first place.*

The defined functions are:

* data_cleaner
* impute_columns
* dates_and_times_corrector
* extract_numbers

data_cleaner

This function calls on the extract_numbers function to clean a number of mixed data type columns. Additionally, dates are converted to pandas.datetime objects. Finally the dates_and_times_corrector is called to correct all times for timezones.

impute_columns

This serves to fill missing values. Two different imputers are created for text and numeric data types respectively. Missing text values are replaced with "unknown" for lack of a better strategy and missing numeric values are replaced with the mode of the column. This would ideally be replaced by a more sophisticated strategy later on. Dates are left as they are, hopefully later on they too can be imputed for example by converting to a numeric data type, finding some sort of average measure and then converting back to date. Data is returned as a dataframe, however with scrambled column order.

dates_and_times_corrector

This extracts the time zone and then changes start and end times of meetings.

extract_numbers

This extracts numbers from strings. This function calls on the extract_numbers function to extract numbers from string data types that are not fully numerical (eg. "<10" would return 10).


**multipli_experiment_1**

This is just some playarund with the data, achieving prediction accuracies above 70% from only the meeting titles with different classifiers (Decision Tree, SVC, Random Forest). Shows some of the weaknesses of our data too. Feel free to continue experimentation on this (maybe add guestno to the classifiers)!


