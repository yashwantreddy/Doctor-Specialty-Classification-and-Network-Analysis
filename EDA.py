import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Obtain the procedures and the physician data
proc = pd.read_csv('data/procedures.csv')

phy = pd.read_csv('data/physicians.csv')

#Plot the top 15 most popular doctor specialities
plt.figure(figsize=(15,12))
sns.countplot(y = phy.specialty,order=phy['specialty'].value_counts().head(15).index)
plt.show()

