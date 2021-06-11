import pickle
from os import listdir
import re
from bs4 import BeautifulSoup
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from collections import defaultdict
from nltk.corpus import wordnet as wn

class Tager:
    def __init__(self, models_path, encoders_path):
        print('init')
        self.models = self.modelsLoader(models_path)
        self.encoders = self.encodersLoader(encoders_path)
       

    def modelsLoader(self, models_path):
        models = {}
        dir_models = listdir(models_path)

        for model in dir_models :
            models[model.split(".")[0]] = pickle.load(open(models_path+model, 'rb'))
        return models
    
    def encodersLoader(self, encoders_path):
        
        encoders = {}
        dir_encoders = listdir(encoders_path)
        for encoder in dir_encoders :
            encoders[encoder.split(".")[0]] = pickle.load(open(encoders_path+encoder, 'rb'))
        
        return encoders
    
    def txtCleaner(self, txt   ):

        sw = set()

        sw.update(tuple(nltk.corpus.stopwords.words('english')))
        raw = BeautifulSoup(txt, "lxml").get_text() 
        characters_reg='[^a-zA-Z0-9#+]'
        words = re.sub(characters_reg, " ", raw).lower()
        words = re.sub(" \d+", " ", words).split()

        lemmatizer = WordNetLemmatizer()

        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
        meaningful_words = [lemmatizer.lemmatize(w, tag_map[t[0]]) for w, t in pos_tag(words) if not w in sw ]
        return  ' '.join(map(str, meaningful_words))
    
    def pridict(self, txt, model_name='LogisticRegression'):
        model = self.models[model_name]
        txt_cleaned = self.txtCleaner(txt)
        xt = self.encoders['tfidf'].transform([txt_cleaned])

        # for model in self.models:
        #     print(model)
        #     print(self.encoders['multilabel'].inverse_transform(self.models[model].predict(xt)))
        return   self.encoders['multilabel'].inverse_transform(model.predict(xt))
        
        