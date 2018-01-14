import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

proc = pd.read_csv('data/procedures.csv')
phy = pd.read_csv('data/physicians.csv')
print 'Data Imported.'

phy['Cardiologist'] = pd.get_dummies(phy.specialty)['Cardiology']
phy.columns = ['physician_id','specialty','Cardiologist']
merged = pd.merge(proc, phy, left_on='physician_id',right_on='physician_id',how='outer')
print 'Transformed data.'

#Getting all your procedure words

procedure_words=[]
for line in merged.procedure:
    procedure_words.append(line.replace('_', ' '))

#Fitting the tfidf transform

tfidf = TfidfVectorizer(stop_words='english')
print 'Fitting tfidf.'
bow = tfidf.fit_transform(procedure_words)

indices_of_cards = merged[merged.Cardiologist==1].index
proc_words_for_cards = []
for lul in indices_of_cards:
    for k in bow[lul,:].todense().tolist():
        val= k
        rowwords = []
        indices = []
        weights = []
        for i,values in enumerate(k):
            if values!=0:
                #print(tfidf.get_feature_names()[i],values)
                rowwords.append(tfidf.get_feature_names()[i])
                indices.append(i)
                weights.append(values)
        #print('Top words of the Doc are: \n')
        for i in np.argsort(weights)[-3:][::-1]:
            #print(rowwords[i])
            proc_words_for_cards.append(rowwords[i])
    #print('\n')

seri = pd.Series(proc_words_for_cards)
print('Top 25 classification words for a Cardiologist are : ',seri.value_counts().head(25))

#As we can observe, we have really frequently occurring words like 'patient','office' and 'established'.
#This introduces a lot of unwanted noise into our classification model. 
