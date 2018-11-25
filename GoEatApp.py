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
import pymysql


db = pymysql.connect(host = 'DESKTOP-PD3BJSG',port=3306,user='mysql',password ='mysql93',db='goeat',charset = 'utf8')

cursor = db.cursor()

sql ="SELECT table_name FROM information_schema.tables where table_schema='goeat'"
cursor.execute(sql)
table = cursor.fetchall()

table_names = []
for name in table:
    table_names.append(name[0])

for table_name in table_names:
    table_select = "SELECT * FROM " + table_name
    col_show = col = "SHOW COLUMNS FROM " + table_name

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []
    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))

    vars()[table_name +'_df'] = pd.DataFrame(list(data),columns = col_name)
    vars()[table_name +'_df'].index = vars()[table_name +'_df'].index + 1

#smooth_user_preference
interactions_full_df = interactions_df \
                    .groupby(['userIndex', 'foodIndex'])['eventStrength'].mean() \
                    .apply(GoEat.smooth_user_preference).reset_index()

#get tfidf
tfidf_df = tfidf_df.drop('foodIndex',axis=1)

tfidf_feature_names = tfidf_df.columns
tfidf_matrix = scipy.sparse.csr_matrix(tfidf_df)



#build user profiles

user_profiles = {}
for key, value in list(zip(user_profiles_df.loc[:,'userIndex'].values, user_profiles_df.loc[:,user_profiles_df.columns != 'userIndex'].values)):
    user_profiles[key] = value.reshape(1, -1)


#get new user info

print('음식 추천을 시작합니다!', rec_start_time)

user_index = int(input('userIndex를 입력해주세요 : '))
new_user = GoEat.cold_start_question(user_index,food_df,15)



interactions_df = interactions_df.append(new_user,ignore_index=True)

interactions_full_df = interactions_df \
                    .groupby(['userIndex', 'foodIndex'])['eventStrength'].mean() \
                    .apply(GoEat.smooth_user_preference).reset_index()

##Content-based filtering##

#build user profile
#builder.get_interacted_indexed_df(interactions_full_df,food_df)
#user_profiles[user_index] = builder.build_users_profile(user_index)


builder= GoEat.user_profiles_builder()
builder.get_interacted_indexed_df(interactions_full_df,food_df)
user_profiles = builder.build_users_profiles(interactions_df,food_df,tfidf_matrix)
#builder.get_interacted_indexed_df(interactions_full_df,food_df)

#content-based model building
cb_model = GoEat.CBRecommender(food_df,user_profiles,tfidf_matrix)

##Collaborative model building##



#build users X items SVD
cf_preds_df = GoEat.users_items_svd(interactions_full_df, nfactors = 5)

#collaborative model building
cf_model = GoEat.CFRecommender(cf_preds_df, food_df)

#Hybrid Model buliding
hybrid_model = GoEat.HybridRecommender(cb_model,cf_model,food_df,method='harmonic')
rec_foods = hybrid_model.recommend_items(user_index,topn=3,items_to_ignore=new_user.foodIndex.tolist(),verbose=True)


print('\n')
print('당신께 추천드리는 음식은!!!\n')
print('1번 째!  ' + rec_foods.loc[0,'foodName'])
print('2번 째!  ' + rec_foods.loc[1,'foodName'])
print('3번 째!  ' + rec_foods.loc[2,'foodName'])

#
#interaction_df
