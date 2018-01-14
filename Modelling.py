import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn import metrics

#importing and merging dataframes
proc = pd.read_csv('data/procedures.csv')
phy = pd.read_csv('data/physicians.csv')
phy['Cardiologist'] = pd.get_dummies(phy.specialty)['Cardiology']
phy.columns = ['physician_id','specialty','Cardiologist']
merged = pd.merge(proc, phy, left_on='physician_id',right_on='physician_id',how='outer')

#The procedure descriptions seems to have an '_' in place of a space. Let's fix it.

procedure_words=[]
for line in merged.procedure:
    procedure_words.append(line.replace('_', ' '))

#Now that we have clean sentences, let's apply tfidf vectorizer on it.

tfidf = TfidfVectorizer(stop_words='english')
X = procedure_words
y = merged.Cardiologist.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
X_train = tfidf.fit_transform(X_train)
X_test = tfidf.transform(X_test)

nb = MultinomialNB()
nb.fit(X_train,y_train)
preds = nb.predict(X_test)

print 'The accuracy score of base model : ',metrics.accuracy_score(y_test,preds)
print 'The precision score of base model : ',metrics.precision_score(y_test,preds)
print 'The recall score of base model : ',metrics.recall_score(y_test,preds)
print 'The ROC AUC score of base model : ',metrics.roc_auc_score(y_test,preds)

#It seems like the model is not fantastic, given that it has a poor recall score. We will examine this is the
#advanced_feature_engineering.py