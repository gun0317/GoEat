#This script is to import food rating data from google docs and to split into several data frames.
import pandas as pd
import os
from sklearn.utils import shuffle

class dataStore:
    def __init__(self):
        #import module

        #set indices
        self.user_info_index = [0,1,2,3,4]  + list(range(54,58))
        self.food_drop_index = list(range(0,5)) + list(range(54,58))
        print('new')


    def read(self,directory):
        #set directory
        dir = directory



        self.df_food = pd.read_csv(dir)

        return self.df_food


    def DataStack(self):
        #set user id
        self.df_food_reset_index = self.df_food.reset_index()



        df_food_rating = self.df_food_reset_index.drop(axis =1,columns=self.df_food_reset_index.columns[self.food_drop_index])

        self.df_food_rating_stack = pd.DataFrame(df_food_rating.stack()).reset_index()
        self.df_food_rating_stack = shuffle(self.df_food_rating_stack)
        self.df_food_rating_stack.columns =['personId','contentId','eventStrength']

        return self.df_food_rating_stack


    def addDataStack(self,directory2):

        dir = directory2

        #import food rating data
        df_food2 = pd.read_csv(dir)

        #user id starts from the last one
        df_food2.index = df_food2.index + len(self.df_food)

        #set user id
        self.df_food_reset_index2 = df_food2.reset_index()


        df_food_rating2 = self.df_food_reset_index2.drop(axis =1,columns=self.df_food_reset_index2.columns[self.food_drop_index])



        #create stacked data frame
        self.df_food_rating_stack2 = pd.DataFrame(df_food_rating2.stack()).reset_index()
        self.df_food_rating_stack2 = shuffle(self.df_food_rating_stack2)
        self.df_food_rating_stack2.columns =['personId','contentId','eventStrength']

        # append new data to old one
        self.df_food_rating_stack = self.df_food_rating_stack.append(self.df_food_rating_stack2).reset_index()

        return self.df_food_rating_stack

    def addUserInfo(self):

        self.df_user_info2 = self.df_food_reset_index2.iloc[:,self.user_info_index]

        self.df_user_info2.columns = ['personId','timestamp','userName','sex','age','aloneHow','eatAlone','eatDate','eatTogether']

        self.df_user_info = self.df_user_info.append(self.df_user_info2)

        return self.df_user_info


    def splitUserInfo(self):




        self.df_user_info = self.df_food_reset_index.iloc[:,self.user_info_index]


        self.df_user_info.columns = ['personId','timestamp','userName','sex','age','aloneHow','eatAlone','eatDate','eatTogether']

        #personId : 사용자 고유번호
        #timestamp : 설문시각
        #userName : 사용자 이름
        #sex : 성별
        #age : 나이
        #aloneHow : 혼밥은 주로 어떻게 하나요?
        #eatAlone : 혼밥할 때 주로 먹는 음식 메뉴는 무엇인가요? 한 가지만 적어주세요.
        #eatDate : (선택사항) 데이트를 하는 상황에서는 주로 무슨 음식을 즐겨 먹나요? 한 가지만 적어주세요.
        #eatTogether : 친한 친구들 여럿이서 만나는 자리에서는 무슨 음식을 즐겨 먹나요? 한 가지만 적어 주세요.

        return self.df_user_info

    def splitArticles(self):

        #articles_df
        #ContentId : 음식 고유번호
        #FoodName : 고유번호에 따른 음식 이름

        self.articles_df = pd.DataFrame(self.df_food_rating_stack.contentId.unique()).reset_index()
        self.articles_df.columns = ['contentId','foodName']

        return self.articles_df

    def splitInteractions(self):
        #interactions_full_df
        #personId : 개인 고유번호
        #ContentId : 음식 고유번호
        #eventStrength : 음식에 대한 평가
        articles = self.articles_df
        interactions_full_with_zeros_df = self.df_food_rating_stack.copy().reset_index(drop=True)

        for food in range(len(self.articles_df.foodName)):
            interactions_full_with_zeros_df.loc[interactions_full_with_zeros_df.contentId == articles.foodName[food],'contentId'] = articles.contentId[food]
            self.interactions_df  = interactions_full_with_zeros_df[interactions_full_with_zeros_df['eventStrength'] != 0]

        return self.interactions_df

    def store(self, directory = 'data\\info'):

        import pd
        import os

        path_user_info = os.path.join(directory,'df_user_info.csv')
        path_articles_df = os.path.join(directory,'articles_df.csv')
        interactions_df = os.path.join(directory,'interactions_df.csv')

        self.df_user_info.to_csv(path_user_info,index=False)
        self.articles_df.to_csv(path_articles_df,index=False)
        self.interactions_df.to_csv(interactions_df,index=False)
