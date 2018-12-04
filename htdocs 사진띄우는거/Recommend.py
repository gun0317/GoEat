import sys
import GoEat
import numpy as np
import pandas as pd
import scipy
import pymysql
from sklearn.model_selection import train_test_split

def get_rec(user_index,mode='default'):

    '''user_index :  [user_index]에게 음식 추천

    mode = 'default'
    'default' : 기본(상황 적용하지 않음)
    'Alone' : 혼자 먹을 때
    'Together' : 같이 먹을 때
    'Date' : 데이트 할 때'''

    #영건 DB
    db = pymysql.connect(host = 'localhost',port=3306,user='root',password ='xlsh5201',db='goeat',charset = 'utf8')
    #태년 DB
    #db = pymysql.connect(host = 'DESKTOP-PD3BJSG',port=3306,user='mysql',password ='mysql93',db='goeat',charset = 'utf8')
    

    cursor = db.cursor()

    sql ="SELECT table_name FROM information_schema.tables where table_schema='goeat'"
    cursor.execute(sql)


    table_select = "SELECT * FROM user_profiles"
    col_show = col = "SHOW COLUMNS FROM user_profiles"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))



    user_profiles_df = pd.DataFrame(list(data),columns = col_name)
    user_profiles_df.index = user_profiles_df.index + 1

    table_select = "SELECT * FROM user_info"
    col_show = col = "SHOW COLUMNS FROM user_info"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))



    user_info_df = pd.DataFrame(list(data),columns = col_name)
    user_info_df.index = user_info_df.index + 1


    table_select = "SELECT * FROM user_detail"
    col_show = col = "SHOW COLUMNS FROM user_detail"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))



    user_detail_df = pd.DataFrame(list(data),columns = col_name)
    user_detail_df.index = user_detail_df.index + 1


    table_select = "SELECT * FROM tfidf"
    col_show = col = "SHOW COLUMNS FROM tfidf"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))



    tfidf_df = pd.DataFrame(list(data),columns = col_name)

    #test
    #tfidf_df = pd.read_csv('tfidf.csv',encoding = 'cp949')

    tfidf_df.index = tfidf_df.index + 1

    table_select = "SELECT * FROM interactions"
    col_show = col = "SHOW COLUMNS FROM interactions"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))


    interactions_df = pd.DataFrame(list(data),columns = col_name)
    interactions_df.index = interactions_df.index + 1



    if mode == 'Alone':
            table_select = "SELECT * FROM interactions_eatAlone"
            col_show = col = "SHOW COLUMNS FROM interactions_eatAlone"

            cursor.execute(table_select)
            data = cursor.fetchall()

            cursor.execute(col_show)
            columns = cursor.fetchall()

            cursor.execute(col_show)
            columns = cursor.fetchall()

            col_name = []

            for column in columns:
                col_name.append(column[0].replace('\ufeff',''))

            interactions_situation_df = pd.DataFrame(list(data),columns = col_name)
            interactions_situation_df.index = interactions_situation_df.index + 1

            #interactions_situation_df = pd.read_csv('interactions_eatAlone.csv')

    elif mode == 'Together':
            table_select = "SELECT * FROM interactions_eatTogether"
            col_show = col = "SHOW COLUMNS FROM interactions_eatTogether"

            cursor.execute(table_select)
            data = cursor.fetchall()

            cursor.execute(col_show)
            columns = cursor.fetchall()

            cursor.execute(col_show)
            columns = cursor.fetchall()

            col_name = []

            for column in columns:
                col_name.append(column[0].replace('\ufeff',''))

            interactions_situation_df = pd.DataFrame(list(data),columns = col_name)
            interactions_situation_df.index = interactions_situation_df.index + 1

            #interactions_situation_df = pd.read_csv('interactions_eatTogether.csv')



    elif mode == 'Date':
            table_select = "SELECT * FROM interactions_eatDate"
            col_show = col = "SHOW COLUMNS FROM interactions_eatDate"

            cursor.execute(table_select)
            data = cursor.fetchall()

            cursor.execute(col_show)
            columns = cursor.fetchall()

            cursor.execute(col_show)
            columns = cursor.fetchall()

            col_name = []

            for column in columns:
                col_name.append(column[0].replace('\ufeff',''))


            interactions_situation_df = pd.DataFrame(list(data),columns = col_name)
            interactions_situation_df.index = interactions_situation_df.index + 1



            #interactions_situation_df = pd.read_csv('interactions_eatDate.csv')



    table_select = "SELECT * FROM food"
    col_show = col = "SHOW COLUMNS FROM food"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))



    food_df = pd.DataFrame(list(data),columns = col_name)
    food_df.index = food_df.index + 1

    table_select = "SELECT * FROM food_detail"
    col_show = col = "SHOW COLUMNS FROM food_detail"

    cursor.execute(table_select)
    data = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    cursor.execute(col_show)
    columns = cursor.fetchall()

    col_name = []

    for column in columns:
        col_name.append(column[0].replace('\ufeff',''))


    food_detail_df = pd.DataFrame(list(data),columns = col_name)
    food_detail_df.index = food_detail_df.index + 1

    #smooth_user_preference
    interactions_full_df = interactions_df \
                        .groupby(['userIndex', 'foodIndex'])['eventStrength'].mean() \
                        .apply(GoEat.smooth_user_preference).reset_index()

    #get tfidf

    #tfidf_df = tfidf_df.drop('foodIndex',axis=1)

    tfidf_feature_names = tfidf_df.columns
    tfidf_matrix = scipy.sparse.csr_matrix(tfidf_df)



    #build user profiles

    #user_profiles = {}
    #for key, value in list(zip(user_profiles_df.loc[:,'userIndex'].values, user_profiles_df.loc[:,user_profiles_df.columns != 'userIndex'].values)):
    #    user_profiles[key] = value.reshape(1, -1)


    #get new user info







    #interactions_df = interactions_df.append(new_user,ignore_index=True)

    interactions_full_df = interactions_df \
                        .groupby(['userIndex', 'foodIndex'])['eventStrength'].mean() \
                        .apply(GoEat.smooth_user_preference).reset_index()


    interactions_train_df, interactions_test_df = train_test_split(interactions_full_df,
                                   stratify=interactions_full_df['userIndex'],
                                   test_size=0.2)

    ##Content-based filtering##

    #build user profile
    #builder.get_interacted_indexed_df(interactions_full_df,food_df)
    #user_profiles[user_index] = builder.build_users_profile(user_index)


    builder= GoEat.user_profiles_builder()
    builder.get_interacted_indexed_df(interactions_train_df,food_df)
    user_profiles = builder.build_users_profiles(interactions_train_df,food_df,tfidf_matrix)
    #builder.get_interacted_indexed_df(interactions_full_df,food_df)

    #content-based model building
    cb_model = GoEat.CBRecommender(food_df,user_profiles,tfidf_matrix)

    ##Collaborative model building##



    #build users X items SVD
    cf_preds_df = GoEat.users_items_svd(interactions_train_df, nfactors = 2)

    #collaborative model building
    cf_model = GoEat.CFRecommender(cf_preds_df, food_df)

    #Hybrid Model buliding
    hybrid_model = GoEat.HybridRecommender(cb_model,cf_model,food_df,method='harmonic')
    rec_foods = hybrid_model.recommend_items(user_index,topn=100,items_to_ignore=[],verbose=True)
    recommend_foods = list(rec_foods.foodName)

    if mode != 'default':


        try:
            interactions_situation_full_df = interactions_situation_df \
                                .groupby(['userIndex', 'foodIndex'])['eventStrength'].mean() \
                                .apply(GoEat.smooth_user_preference).reset_index()

            cf_preds_sit_df = GoEat.users_items_svd(interactions_situation_full_df, nfactors = 20)
            cf_situation_model = GoEat.CFRecommender(cf_preds_sit_df, food_df)

            rec_situation = cf_situation_model.recommend_items(user_index,topn=100)

            rec_situation = rec_situation.rename(columns = {'recStrength':'recStrength_sit'})
            rec_by_sit = pd.merge(rec_foods,rec_situation,on ='foodIndex',how= 'outer').fillna(1e-5)
            rec_by_sit['recStrength'] = 2*rec_by_sit.recStrengthHybrid*rec_by_sit.recStrength_sit/(rec_by_sit.recStrengthHybrid + rec_by_sit.recStrength_sit)
            rec_by_sit= rec_by_sit.sort_values(by='recStrength',ascending =False)

            recommend_foods = list(rec_by_sit.foodName)


        except:

            recommend_foods = list(rec_foods.foodName)






    print(recommend_foods[0])
    print(recommend_foods[1])
    print(recommend_foods[2])

    #return [rec_foods.loc[0,'foodName'], rec_foods.loc[1,'foodName'],rec_foods.loc[2,'foodName']]
    #split test and test set


if __name__ == "__main__":
    requestedIndex = sys.argv[1]
    if len(sys.argv) == 3:
        mode_ = sys.argv[2]
    else :
        mode_ = 'default'
    get_rec(int(requestedIndex),mode_)
    #
    #interaction_df
