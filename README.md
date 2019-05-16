# Heart_attack
This is a small survey on heart attack prediction System using Machine Learning approach

we have used 3 techniques to evaluate how well the system approches and also on how well it will give result for Specificity

    a)logistic Regression
    b)Neural Network
    c)Random Forest Classifier

1)Data collection: Data is in the format of csv and it contains predictors like education ,sysBP,currentSmoker,and many more ,and also target variable TenYearCHD.It contains around 4241 rows.

2) Data pre-Processing: In this step we renamed some of the columns and also remove the row with null values.

3)Data Mining: Data Mining is the process of extracting the hidden pattern in the data .we used logit Function.Logit Function will give how important predictor attributes.If the p-value is less than 0.05 it says that particular feature is significally different.If the p-value is more than 0.05 remove those attributes.

4)Building the model:
    a) Logistic regression : Logistic regression is  appropriate regression analysis to conduct when the dependent variable is dichotomous.Also we are able to say stats from the co-efficients.
    b)Neural Network: Neural Network have the ability to learn and improve every time in predicting an output.we used feed forward neural network.The purpose of a neural network is to learn to recognize patterns in data.
    c) Random Forest tree classifier:It is an ensemble method where it creates number of decision tree and output the means of prediction of all tree.It avoids over-fitting. 
    
5)Evaluating Model:
  Finally Table is created of logistic,Neural,RandomForestTree with each having values of accuracy ,sensitivity,specificity.
  Model is checked with new Patient information asking values for age ,gender and other 4 predictors values.
  

