#!/usr/bin/env python
# coding: utf-8

# ### Optimizing Raisin Classification with Machine Learning Hyperparameter Tuning
# 
# 
# #### Introduction
# 
# In this project, we analyze the Raisin Dataset to classify raisin types using machine learning models. We perform hyperparameter tuning for a Decision Tree and Logistic Regression model to optimize performance. 
# 
# **Workflow:**
# 1. Load and explore the dataset (EDA).
# 2. Preprocess the data: split into training and testing sets.
# 3. Train and optimize models with GridSearchCV and RandomizedSearchCV.
# 4. Evaluate the models and analyze hyperparameter effects.
# 5. Draw conclusions based on the findings.

# ##### Libraries and Setup

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV


# ##### Load and Explore the Dataset and explore the first rows

# In[2]:


raisins = pd.read_excel('Raisin_Dataset.xlsx')
raisins.head()


# ##### Summary statistics and Dataset basic Info for numerical columns

# In[3]:


raisins.info()
raisins.describe()


# ##### Class distribution visualizatios
# 

# In[4]:


sns.countplot(data=raisins, x="Class")
plt.title("Class Distribution")
plt.show()


# ##### Explore and  Visualize relationships between features
# 

# In[5]:


sns.pairplot(raisins, hue="Class")
plt.suptitle("Feature Relationships by Class", y=1.02)
plt.show()


# #### Preprocessing Data for our Models
# 
# ##### Create predictor and target variables, X and y
# 

# In[6]:


X = raisins.drop(columns=['Class']) # the rest of the columns together compose the predictor variable matrix
y = raisins['Class'] #The column 'Class' represents the target variable


# ##### Examine the dataset. We want to check total number of features, total number of samples and different values for the Class column

# In[7]:


print("NUmber of rows and columns:", X.shape) # rows x columns
print("Uniue values for y target variable:", y.unique())
print(type(y))


# ##### Split into training and testing sets

# In[8]:


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 19)


# #### Grid Search with Decision Tree Classifier
# 
# ##### We create a Decision Tree model
# 

# In[9]:


tree = DecisionTreeClassifier()


# ##### Hyperparameters definition for GridSearchCV

# In[10]:


parameters = {'min_samples_split': [2,3,4], 'max_depth': [3,5,7]}


# ##### Create a GridSearchCV model and then we can fit the GridSearchCV model to the training data

# In[11]:


grid = GridSearchCV(tree, parameters)
grid.fit(X_train, y_train)


# ##### Down, we will:
# 
# - Print the model and hyperparameters obtained by GridSearchCV
# - Print best score, it gives the best score
# - Print the accuracy of the final model on the test data with: gives the best score on test data.
# 
# 

# In[12]:


print(grid.best_estimator_)
print(grid.best_score_)
print(grid.score(X_test, y_test))


# ##### As summary, we can print a table summarizing the results of GridSearchCV

# In[13]:


print(grid.cv_results_, "\n")
print(grid.cv_results_['params'])

hyperparameter_values = pd.DataFrame(grid.cv_results_['params'])
randomsearch_scores = pd.DataFrame(grid.cv_results_['mean_test_score'], columns = ['score'])
df = pd.concat([hyperparameter_values, randomsearch_scores], axis = 1)
print(df)


# #### Random Search with Logistic Regression
# 
# ##### Prepare The logistic regression model

# In[14]:


lr = LogisticRegression(solver='liblinear', max_iter = 1000)


# ##### Define distributions to choose hyperparameters from

# In[15]:


from scipy.stats import uniform

distributions = {'penalty': ['l1', 'l2'], 'C': uniform(loc=0, scale=100)}


# ##### Create a RandomizedSearchCV model and fit it with trainin data

# In[16]:


clf = RandomizedSearchCV(lr, distributions, n_iter=8)
clf.fit(X_train, y_train)


# ##### We print:
# 
# - the best esimator
# - the best score
# - a table summarizing the results of RandomSearchCV

# In[17]:


print(clf.best_estimator_)
print(clf.best_score_)

df = pd.concat([pd.DataFrame(clf.cv_results_['params']), pd.DataFrame(clf.cv_results_['mean_test_score'], columns=['Accuracy'])] ,axis=1)
print(df.sort_values('Accuracy', ascending = False))


# ### Conclusion
# 
# **Key Findings:**
# - The Decision Tree classifier performed well after hyperparameter tuning, achieving a test accuracy of 0.82.
# - Logistic Regression with random search optimization also provided competitive results with a test accuracy of 0,87.
# - Hyperparameter tuning demonstrated the importance of optimizing model parameters for improved performance.
