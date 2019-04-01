# -*- coding: utf-8 -*-
"""Project_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HXBNVKBb8yRe5fty0RQmQVTiaevsfF5p
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as st
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.metrics import confusion_matrix
import matplotlib.mlab as mlab
# %matplotlib inline
import io
import pandas as pd

from google.colab import files
uploaded = files.upload()

df = pd.read_csv(io.BytesIO(uploaded["framingham.csv"]))

#Called Function
def data_cleaning(df):
  
  #count the number of null values
  print("#count the number of null values  \n",df.isna().sum())
  
  #rename the columns
  df.rename(columns = {'male':'gender','TenYearCHD':"heart_attack"},inplace = True) 
  
  
  #remove education column
  df.drop(['education'],axis = 1,inplace = True)
  
  #drop all rows with null values
  df.dropna(inplace = True,axis = 0) 
  
  print("                ")
  
  
  #count the number of null values
  print(df.isna().sum())
  
  
  
  
  print("                 ")
  #count number of rows
  print(df.count())
  
  
  
  print("                 ")
  
  return df

#calling Function
df = data_cleaning(df)
df.head()

#Called Function
def draw_histograms(dataframe, features, rows, cols):
    fig=plt.figure(figsize=(20,20))
    for i, feature in enumerate(features):
        ax=fig.add_subplot(rows,cols,i+1)
        dataframe[feature].hist(bins=20,ax=ax,facecolor='Darkblue')
        ax.set_title(feature+" Distribution",color='DarkRed')
        
    fig.tight_layout()  
    plt.show()

#calling Function    
draw_histograms(df,df.columns,9,2)

print(df.heart_attack.value_counts())
sn.countplot(x = 'heart_attack',data=df)

sn.pairplot(data=df)

"""# Implementing Logit method to extract only those predictors which effect the target Variable"""

#Calling Function
def build_logit(df):
  from statsmodels.tools import add_constant as add_constant
  heart_df_constant = add_constant(df)
  heart_df_constant.head()
  st.chisqprob = lambda chisq, df: st.chi2.sf(chisq, df)
  cols=heart_df_constant.columns[:-1]
  model=sm.Logit(df.heart_attack,heart_df_constant[cols])
  result=model.fit()
  print(result.summary())
  return cols,heart_df_constant

#Called Function
cols,heart_df_constant = build_logit(df)

#Calling Function
def back_feature_elem (data_frame,dep_var,col_list):
    
    while len(col_list)>0 :
        model=sm.Logit(dep_var,data_frame[col_list])
        result=model.fit(disp=0)
        largest_pvalue=round(result.pvalues,3).nlargest(1)
        if largest_pvalue[0]<(0.05):
            return result
            break
        else:
            col_list=col_list.drop(largest_pvalue.index)


#Calling Function            
result=back_feature_elem(heart_df_constant,df.heart_attack,cols)
print(result.summary())

"""# **Implementing Logistic Regression Model on selective columns**"""

cols = ['gender','age','cigsPerDay','totChol','sysBP','glucose']
y = df.iloc[:,-1]
X = df[cols]

#Called Function
def build_logistic_regression(X,y):
  from sklearn.model_selection import train_test_split
  x_train ,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.20,random_state = 5)
  
  from sklearn.linear_model import LogisticRegression
  model = LogisticRegression()
  model.fit(x_train,y_train)  
#   print("model co-effcients are")
#   print("Beta1,Beta2,Beta3,Beta4,Beta5",model.coef_)
  
  y_pred = model.predict(x_test)
  y_prob = model.predict_proba(x_test)
  
  #plotting confusion matrix
  cm = plot_confusion_matrix(y_test,y_pred)  
  
  return y_test,y_pred,cm,y_prob,model

#Called Function
def plot_confusion_matrix(y_test,y_pred):
  from sklearn.metrics import confusion_matrix
  cm=confusion_matrix(y_test,y_pred)
  conf_matrix=pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
  plt.figure(figsize = (10,7))
  sn.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")
  return cm

y_test,y_pred,Confusion_Matrix_logistic,y_prob,model_logistic = build_logistic_regression(X,y)

import sklearn
print("Accuracy Score Percentage of model is :",sklearn.metrics.accuracy_score(y_test,y_pred)*100)

def Evaluate_model(Confusion_Matrix):  
  TN = Confusion_Matrix[0,0]
  TP = Confusion_Matrix[1,1]
  FN = Confusion_Matrix[1,0]
  FP = Confusion_Matrix[0,1]
  Actual_yes = TP+FN
  Actual_no = TN+FP
  Predicted_yes = TP+FP
  Total = TN+TP+FN+FP

  #Accuracy of the model...
  Accuracy = (TN+TP)/Total

  #Sensitivity of the model or recall of the model

  Sensitivity = TP/Actual_yes


  #True negative Rate or Specificity of the model

  Specificity = TN/Actual_no


  #Precision of the model
  Precision = TP/Predicted_yes
  
  return Accuracy,Sensitivity,Specificity,Precision

Accuracy_logistic,Sensitivity_logistic,Specificity_logistic,Precision_logistic = Evaluate_model(Confusion_Matrix_logistic)

#Called Function
def precision_recall_curve_values(y_test,y_prob): 
  from sklearn.metrics import precision_recall_curve
  precision, recall, thresholds = precision_recall_curve(y_test, y_prob[:,1]) 
  pr_auc = sklearn.metrics.auc(recall, precision)
  return precision, recall, thresholds

#Calling Function
precision, recall, thresholds = precision_recall_curve_values(y_test,y_prob)

#Called Function
def plot_Precision_recall_threshold(thresholds,precision,recall):
  plt.title("Precision-Recall vs Threshold Chart")
  plt.plot(thresholds, precision[: -1], "b--", label="Precision")
  plt.plot(thresholds, recall[: -1], "r--", label="Recall")
  plt.ylabel("Precision, Recall")
  plt.xlabel("Threshold")
  plt.legend(loc="lower left")
  plt.ylim([0,1])
  
#Calling Function  
plot_Precision_recall_threshold(thresholds,precision,recall)

def minimize_threshold(y_test,y_prob):
  from sklearn.preprocessing import binarize
  for i in range(1,5):
      cm2=0    
      y_pred2=binarize(y_prob,i/10)[:,1]
      cm2=confusion_matrix(y_test,y_pred2)
      print('with',i/10,'Threshold value Accuracy of the model is ',(cm2[0,0]+cm2[1,1])/(cm2[0,0]+cm2[1,1]+cm2[1,0]+cm2[0,1]),'\n')
      print ('With',i/10,'threshold the Confusion Matrix is ','\n',cm2,'\n',
              'with',cm2[0,0]+cm2[1,1],'correct predictions and',cm2[1,0],'Type II errors( False Negatives)','\n\n',
            'Sensitivity: ',cm2[1,1]/(float(cm2[1,1]+cm2[1,0])),'Specificity: ',cm2[0,0]/(float(cm2[0,0]+cm2[0,1])),'\n\n\n')
minimize_threshold(y_test,y_prob)

#Called Function 
def plot_roc_curve(y_test,y_prob):
  from sklearn.metrics import roc_curve
  fpr, tpr, thresholds = roc_curve(y_test, y_prob[:,1])
  plt.plot(fpr,tpr,linewidth = 3)
  plt.plot([0, 1], [0, 1], 'r', linewidth=2)
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.0])
  plt.title('ROC curve for Heart disease classifier')
  plt.xlabel('False positive rate (1-Specificity)')
  plt.ylabel('True positive rate (Sensitivity)')
  plt.grid(True)
  roc_score = sklearn.metrics.roc_auc_score(y_test,y_prob[:,1])
  return roc_score

#Calling Function  
roc_score = plot_roc_curve(y_test,y_prob)

print("ROC Score percentage or area under the curve score Percentage is :",roc_score*100)

#Called Function 
def plot_roc_curve_neural(y_test,y_prob):
  from sklearn.metrics import roc_curve
  fpr, tpr, thresholds = roc_curve(y_test, y_prob)
  plt.plot(fpr,tpr,linewidth = 3)
  plt.plot([0, 1], [0, 1], 'r', linewidth=2)
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.0])
  plt.title('ROC curve for Heart disease classifier')
  plt.xlabel('False positive rate (1-Specificity)')
  plt.ylabel('True positive rate (Sensitivity)')
  plt.grid(True)
  roc_score = sklearn.metrics.roc_auc_score(y_test,y_prob)
  return roc_score

"""# Implementing Neural Networks for Heart Disease Classification"""

y = df.iloc[:,-1]
X = df[cols]


#Called Function
def build_Neural_Network(X,y):
  from sklearn.model_selection import train_test_split
  x_train ,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.20,random_state = 5)

  from sklearn.preprocessing import StandardScaler
  sc = StandardScaler()
  x_train  = sc.fit_transform(x_train)
  x_test = sc.transform(x_test)


  import keras
  from keras.models import Sequential
  from keras.layers import Dense
  from keras.layers import Activation, Dropout, Flatten, Dense


  classifer = Sequential()
  classifer.add(Dense(units = 7,init = 'uniform',activation  = 'relu',input_dim = 6))
  classifer.add(Dense(units = 14,init = 'uniform',activation = 'relu'))
  classifer.add(Dense(1))
  classifer.add(Activation('sigmoid'))
  classifer.compile(optimizer='adam',loss='binary_crossentropy',metrics = ['accuracy'])
  classifer.fit(x_train,y_train,batch_size = 15,epochs =100)

  y_pred = classifer.predict(x_test)
  
  y_pred = y_pred>0.5
  y_prob = classifer.predict_proba(x_test)
  

  cm=plot_confusion_matrix(y_test,y_pred)

  return y_test,y_pred,cm,y_prob,classifer




#Calling Function
y_test,y_pred,Confusion_Matrix_Neural,y_prob,model_neural = build_Neural_Network(X,y)

#Evaluating Neural Network Modelurve
Accuracy_neural,Sensitivity_neural,Specificity_neural,Precision_neural = Evaluate_model(Confusion_Matrix_Neural)

#plotting roc C
roc_score = plot_roc_curve_neural(y_test,y_prob)

print("ROC Score percentage or area under the curve score Percentage is :",roc_score*100)

"""# Implementing Random Forest Classifier"""

X = df[cols]
y = df.iloc[:,-1]

#Called Function
def building_random_forest(X,y):
  
  from sklearn.model_selection import train_test_split
  x_train ,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.20,random_state = 5)

   
  from sklearn.preprocessing import StandardScaler
  sc = StandardScaler()
  x_train = sc.fit_transform(x_train)
  x_test = sc.transform(x_test)
  
  from sklearn.ensemble import RandomForestClassifier
  model =  RandomForestClassifier(n_estimators = 10,criterion  = "entropy" ,random_state   = 0)
  model.fit(x_train,y_train)
  
  
  y_pred = model.predict(x_test)
  y_prob = model.predict_proba(x_test)
  
  #plotting confusion matrix
  cm = plot_confusion_matrix(y_test,y_pred)  
  
  return y_test,y_pred,cm,y_prob,model
  
  
  
#Calling Function
y_test,y_pred,Confusion_Matrix_random_forest,y_prob,model_random = building_random_forest(X,y)

#Evaluating random Forest Network Modelurve
Accuracy_forest,Sensitivity_forest,Specificity_forest,Precision_forest = Evaluate_model(Confusion_Matrix_random_forest)

#plotting roc C
roc_score = plot_roc_curve_neural(y_test,y_prob[:,1])

print("ROC Score percentage or area under the curve score Percentage is :",roc_score*100)

#Calling Function
precision, recall, thresholds = precision_recall_curve_values(y_test,y_prob)



#Calling Function
plot_Precision_recall_threshold(thresholds,precision,recall)

data = {'Model_Name':['Logistic_Regression','Neural_Network','RandomTreeForest'],'Accuracy':[Accuracy_logistic*100,Accuracy_neural*100,Accuracy_forest*100],'Specificity':[Specificity_logistic*100,Specificity_neural*100,Specificity_forest*100]
        ,'Sensitivity':[Sensitivity_logistic*100,Sensitivity_neural*100,Sensitivity_forest*100]}
frame = pd.DataFrame(data,index=['1','2','3'],columns=['Model_Name','Accuracy','Sensitivity','Specificity'])

frame

#called Function

def predict_heart_attack(model):
  
  gender = int(input("Enter the gender information 1->male,0->female: "))
  age = int(input("enter the person age: "))
  cigsPerDay = int(input("Enter the number of cigerate you intake Per Day: "))
  totChol = float(input("Enter the total cholestrol level ----->  normal Readings '180-200' : "))
  sysBP = float(input("Enter the BP level ----->  normal Readings '90-140': "))
  glucose = float(input("Enter the glucose level  ----->  normal Readings '80-110' : "))

  data = {'gender':gender,'age':age,'cigsPerDay':cigsPerDay,'totChol':totChol,'sysBP':sysBP,'glucose':glucose}
  x = pd.DataFrame(data,columns = ['gender','age','cigsPerDay','totChol','sysBP','glucose'],index = ['0'])

  
  y = model.predict(x)
  return x,y

#calling Function
data ,prediction = predict_heart_attack(model_logistic)

data

print("From the above data we came up with prediction that the person")
if(prediction[0]==0):
  print("Wont get heart attack")
else:
  print("May have heart attack")



