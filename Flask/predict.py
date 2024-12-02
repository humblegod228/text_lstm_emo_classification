import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow import keras

import re
import pickle

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from keras.utils import pad_sequences

class Emotion_Detector():
    def __init__(self):
        self.lstm_model = keras.models.load_model(r"D:\Emotion Classification\Models\lstm_model.h5")
        
        with open(r"D:\Emotion Classification\Models\tokenizer.pickle", 'rb') as handle:
            self.word_tokenizer = pickle.load(handle)
            
        with open(r"D:\Emotion Classification\Models\encoder.pickle", 'rb') as handle:
            self.encoder = pickle.load(handle)
    
    def text_preprocessing(self,text):
        # Remove punctuations and numbers
        text = re.sub("[^a-zA-Z]"," ",text.lower())
        text = re.sub(r"\s+",' ',text)
    
        # Tokenization
        token = word_tokenize(text)

        # Remove StopWords
        token = [i for i in token if i not in stopwords.words("english")]

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        token = [lemmatizer.lemmatize(word) for word in token]

        processed_text = " ".join(token)
        return processed_text
    
    def string_to_vector(self,text):
        max_len = 35
        text = self.text_preprocessing(text)
        vector = self.word_tokenizer.texts_to_sequences([text])
        padded_vector = pad_sequences(vector,padding="post",maxlen=max_len)

        return padded_vector
    
    def predict(self,text):
        vector = self.string_to_vector(text)
        out = self.lstm_model.predict(vector,verbose=0)

        answer = np.argmax(out)
        ans = self.encoder.inverse_transform([answer])

        ans_dict = {}
        emoji = [" 😠"," 😱"," 😃"," 🥰"," 😢"]
        for i in range(5):
            ans_dict[self.encoder.inverse_transform([i])[0] + emoji[i]] = (out[0][i]/np.sum(out) * 100)
        
        return ans[0],ans_dict