import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder , StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeRegressor

df  = pd.read_csv("C:\\Users\\Ram kumar\\Downloads\\yield_df (1).csv")
df = df.drop(['Unnamed: 0'] , axis=1)
df['average_rain_fall_mm_per_year'] = df['average_rain_fall_mm_per_year'].astype(np.float64)


col = ['Year' , 'average_rain_fall_mm_per_year' , 'pesticides_tonnes' , 'avg_temp' , 'Area' , 'Item' , 'hg/ha_yield']
df = df[col]


X = df.drop(['hg/ha_yield'] , axis = 1)
y = df['hg/ha_yield']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ohe  = OneHotEncoder(drop = 'first')
scaler = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ('onehotencoder' , ohe , [4,5]),
        ('standrization' , scaler , [0,1,2,3])
    ],
    remainder='passthrough'
)

X_train_dummy = preprocessor.fit_transform(X_train)
X_test_dummy = preprocessor.transform(X_test)


from sklearn.tree import DecisionTreeRegressor
dtree = DecisionTreeRegressor()
dtree.fit(X_train_dummy,y_train)
y_pred = dtree.predict(X_test_dummy)


def yeildPrediction(year , avg_rain_fall , pest , avg_temp , Area , Item):
    data  =  pd.DataFrame([[year , avg_rain_fall , pest , avg_temp , Area , Item]] ,  columns= X.columns)
    transformed_data = preprocessor.transform(data)
    res = dtree.predict(transformed_data)
    return res