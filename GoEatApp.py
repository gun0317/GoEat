import numpy as np
import pickle
import pandas as pd
import GoEat
from GoEatWebCrawler import GoEatWebCrawler
from collections import Counter
from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.utils import concordance, pprint
import scipy
import sklearn
import konlpy
import re

#import dataframes
df_user_info = pd.read_csv('data\\info\\df_user_info.csv')
df_user_detail =pd.read_csv('data\\info\\df_user_detail.csv')
food_df = pd.read_csv('data\\info\\food_df.csv')
food_detail_df = pd.read_csv('data\\info\\food_detail_df.csv')
interactions_df = pd.read_csv('data\\info\\interactions_df.csv')


#get new user info

new_user = GoEat.cold_start_question(999,food_df,15)

interactions_df = interactions_df.append(new_user,ignore_index=True)
##Content-based filtering##
#import tfidf_matrix
with open('tfidf.pickle', 'rb') as f:
    tfidf_matrix, tfidf_feature_names = pickle.load(f)

#build user profiles
builder= GoEat.user_profiles_builder()
user_profiles = builder.build_users_profiles(interactions_df,food_df,tfidf_matrix)

#content-based model building
cb_model = GoEat.CBRecommender(food_df,user_profiles,tfidf_matrix)

##Collaborative model building##

#smooth_user_preference
interactions_full_df = interactions_df \
                    .groupby(['userId', 'foodId'])['eventStrength'].mean() \
                    .apply(GoEat.smooth_user_preference).reset_index()

#build users X items SVD
cf_preds_df = GoEat.users_items_svd(interactions_full_df, nfactors = 20)

#collaborative model building
cf_model = GoEat.CFRecommender(cf_preds_df, food_df)

print('CB')
print(cb_model.recommend_items(999,topn=10,items_to_ignore=new_user.foodId.tolist(),verbose=True).foodName)
print('\nCF')
print(cf_model.recommend_items(999,topn=10,items_to_ignore=new_user.foodId.tolist(),verbose=True).foodName)
