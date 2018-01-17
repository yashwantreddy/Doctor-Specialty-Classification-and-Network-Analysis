import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Obtain the procedures and the physician data
proc = pd.read_csv('data/procedures.csv')
phy = pd.read_csv('data/physicians.csv')

#Let's merge the 2 dataframes.

phy['Cardiologist'] = pd.get_dummies(phy.specialty)['Cardiology']
phy.columns = ['physician_id','specialty','Cardiologist']
merged = pd.merge(proc, phy, left_on='physician_id',right_on='physician_id',how='outer')

#Let's take a look at the distribution of cardiologists

plt.figure(figsize=(15,8))
sns.countplot(merged['Cardiologist'])
plt.title('Distribution of Cardiologists')
plt.show()

#Plot the top 15 most popular doctor specialities

plt.figure(figsize=(15,12))
plt.title('Distribution of top 15 Doctor Specialties')
sns.countplot(y=merged['specialty'],order=merged['specialty'].value_counts().head(15).index)
plt.show()

