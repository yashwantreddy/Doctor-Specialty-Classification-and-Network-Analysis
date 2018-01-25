import pandas as pd
from os import path
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

proc = pd.read_csv('data/procedures.csv')
phy = pd.read_csv('data/physicians.csv')
phy['Cardiologist'] = pd.get_dummies(phy.specialty)['Cardiology']
phy.columns = ['physician_id','specialty','Cardiologist']
merged = pd.merge(proc, phy, left_on='physician_id',right_on='physician_id',how='outer')
indices=[]
for i,proc in enumerate(merged.procedure):
    w=[]
    w.append(proc.replace('_', ' '))
    if 'typically' in w[0].split():
        indices.append(i)

merged_not_typically = merged.drop(merged.index[list(indices)])
merged_not_typically = merged_not_typically.reset_index()
merged_not_typically.drop('index',axis=1,inplace=True)
merged_not_typically_only_cards = merged_not_typically[merged_not_typically.specialty=='Cardiology']

card_words=[]
for line in merged_not_typically_only_cards.procedure:
    card_words.append(line.replace('_', ' '))


d = path.dirname(__file__)
doc_mask = np.array(Image.open(path.join(d, "public-heart.png")))
wc = WordCloud(font_path='C:\Windows\Fonts\FREESCPT.TTF',width = 1200, height = 750,scale=5, background_color="white", max_words=2000, mask=doc_mask,colormap='Reds')
wc.generate(' '.join(card_words))
wc.to_file(path.join(d, "heart_cloud1.png"))


#plt.figure(figsize=(15,8))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(doc_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()