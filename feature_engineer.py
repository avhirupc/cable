import pandas as pd 
import numpy as np 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_iris
import category_encoders as ce

class Fisher(BaseEstimator, TransformerMixin):
    def __init__(self,percentile=0.95):
            self.percentile = percentile
    def fit(self, X, y):
            from numpy import shape, argsort, ceil
            X_pos, X_neg = X[y==1], X[y==0]
            X_mean = X.mean(axis=0)
            X_pos_mean, X_neg_mean = X_pos.mean(axis=0), X_neg.mean(axis=0)
            deno = (1.0/(shape(X_pos)[0]-1))*X_pos.var(axis=0) + (1.0/(shape(X_neg)[0]-1))*X_neg.var(axis=0)
            num = (X_pos_mean - X_mean)**2 + (X_neg_mean - X_mean)**2
            F = num/deno
            sort_F = argsort(F)[::-1]
            n_feature = (float(self.percentile)/100)*shape(X)[1]
            self.ind_feature = sort_F[:ceil(n_feature)]
            return self
    def transform(self, x):
            return x[self.ind_feature,:]

class DateTimeEngineer(BaseEstimator,TransformerMixin):
	"""Helper to Add Date/Time features to data"""
	def __init__(self,columns,options=["day_of_week","dayofweek","dayofyear","dayofmonth","days_in_month","daysinmonth","hour","is_leap_year","is_month_end","is_month_start","is_quarter_end","is_year_start","is_year_end","minute","month","month_name","quarter","second","week","weekday","weekday_name","weekofyear"]):
		self.options_supported=["day_of_week","absolute_time","day_of_year","day_of_month","hour_of_day","minute_of_hour","dayofweek","dayofyear","dayofmonth","days_in_month","daysinmonth","hour","is_leap_year","is_month_end","is_month_start","is_quarter_end","is_year_start","is_year_end","minute","month","month_name","quarter","second","week","weekday","weekday_name","weekofyear"]
		self.__check_options(options)
		self.options=options
		self.columns_to_transform=columns
		self.each_column_transform={}

	def __check_options(self,options):
		for opt in options: 
			if opt not in self.options_supported:
				raise NotImplementedError

	def __check_columns(self,X):
		for i in self.columns_to_transform:
			try:
				X[i].dt
			except Exception as e:
				raise Exception(f"Column {i} not in correct format"+str(e))

	def __transform_column(self,data,column):
		temp=pd.DataFrame()
		x=data[column].dt
		if 'day_name' in self.options:
			temp[column+'_day_name']=x.day_name()
		# replace by getattr 
		for opt in self.options:
			temp[column+'_'+opt]=getattr(x,opt)
		self.each_column_transform[column]=temp

	def fit(self,X,y=None):
		self.__check_columns(X)
		for column in self.columns_to_transform :
			self.__transform_column(X,column)
		return self

	def transform(self,x):
		all_concat=pd.concat(list(self.each_column_transform.values()),axis=1)
		return pd.concat([x,all_concat],axis=1)




class CategoryEngineer(object):
	"""docstring for CategoryEngineer"""
	def __init__(self, options=["OneHotEncoder"]):
		super(CategoryEngineer, self).__init__()
		self.options_supported= ["BackwardDifferenceEncoder","BinaryEncoder","HashingEncoder","HelmertEncoder","OneHotEncoder","OrdinalEncoder","SumEncoder","PolynomialEncoder","BaseNEncoder","TargetEncoder","LeaveOneOutEncoder"]

	def __check_options(self,options):
		for opt in options: 
			if opt not in self.options_supported:
				raise NotImplementedError

	def fit(self,X,y=None):



	def transform(self,x):



class NumericalEngineer(object):
	"""docstring for NumericalEngineer"""
	def __init__(self, arg):
		super(NumericalEngineer, self).__init__()
		self.arg = arg
		raise NotImplementedError
		

		

