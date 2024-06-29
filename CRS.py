import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

df = pd.read_csv("C:\\Users\\Ram kumar\\Downloads\\Crop_recommendation.csv")
# print(df)
le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])
class_labels = df['label'].unique().tolist()
class_labels = le.classes_
class_labels
label_dict = {}
for index,label in enumerate(class_labels):
    label_dict[label] = index
    
print(label_dict)
#dividing Inputs and Outputs
x = df.drop('label',axis=1)
y = df['label']
# features  =  df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]/  #inputs
features = df.drop('label',axis=1)
target = df['label']
# target = df['label'] #outputs
labels = df['label']

#Dividing the Data set into trainging and testing Dataset 

Xtrain , Xtest , Ytrain , Ytest = train_test_split(features , target , test_size=0.2 , random_state=2)

naivebayes = GaussianNB()
naivebayes.fit(Xtrain,Ytrain)
predicted_values = naivebayes.predict(Xtest)
x = metrics.accuracy_score(Ytest , predicted_values)

RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)
predicted_values = RF.predict(Xtest)



def CropProduction(N, P,K,temperature, humidity, ph, rainfall):
    data = pd.DataFrame([[N,P,K,temperature,humidity,ph,rainfall]], columns=features.columns)
    prediction = RF.predict(data)
    predicted_label = class_labels[prediction[0]]
    print(predicted_label)
    return predicted_label