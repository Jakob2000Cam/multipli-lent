import pandas as pd
import nltk
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
import re
from nltk.stem import WordNetLemmatizer
import os

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


#creates os independent paths to read and write data
read_path = os.path.join('data', 'processed', 'cleaned_labelled_october.pkl')
write_path = os.path.join('data', 'processed', 'normalised_labelled_october.pkl')
#load the labelled cleaned data into the data_frame
data_frame = pd.read_pickle(r'data/processed/cleaned_labelled_october.pkl')

class Normaliser:

    def normalise(self, text):
        text = self.convert_emojis(text)
        text = self.convert_emoticons(text)
        text = self.lemmatize_text(text)
        text = self.simplify_punctuation_and_whitespace(text)
        return text

    #convert emojis to text equivalent
    @staticmethod
    def convert_emojis(text):
        for emot in UNICODE_EMO:
            text = text.replace(emot,
                                ("".join(UNICODE_EMO[emot].replace(",","").replace(":","").replace("_"," ")) +" emoji."))   
        return text

    #convert emoticons to text equivalent
    @staticmethod
    def convert_emoticons(text):
        for emot in EMOTICONS:
            text = re.sub(u'('+emot+')', (" ".join(EMOTICONS[emot].replace(",","").split()) + " emoticon."), text)  
        return text

    #simplifies complicated punctuation except for ellipsis (...)
    @staticmethod
    def simplify_punctuation(text):
        corrected = str(text)
        corrected = re.sub(r'([!?,;])\1+', r'\1', corrected)
        corrected = re.sub(r'\.{2,}', r'...', corrected)
        return corrected

    #removes double whitespaces
    @staticmethod
    def normalize_whitespace(text):
        corrected = str(text)
        corrected = re.sub(r"//t",r"\t", corrected)
        corrected = re.sub(r"( )\1+",r"\1", corrected)
        corrected = re.sub(r"(\n)\1+",r"\1", corrected)
        corrected = re.sub(r"(\r)\1+",r"\1", corrected)
        corrected = re.sub(r"(\t)\1+",r"\1", corrected)
        return corrected.strip(" ")

    #implements above two methods
    def simplify_punctuation_and_whitespace(self, sentence):
        sent = self.simplify_punctuation(sentence)
        sent = self.normalize_whitespace(sent)
        return sent

    #lemmatize words
    @staticmethod
    def lemmatize_text(text):
        lemmatizer = WordNetLemmatizer()
        lemmatized_output = ''.join([lemmatizer.lemmatize(w) for w in text])
        return lemmatized_output


normalise = Normaliser()
data_frame['meetingtitle'] = data_frame['meetingtitle'].transform(normalise.normalise)
data_frame.to_pickle(write_path)