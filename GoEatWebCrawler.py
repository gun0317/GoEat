import requests
from bs4 import BeautifulSoup as BS
import re
from collections import Counter
from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.utils import concordance, pprint


class GoEatWebCrawler:

    def recipe_finder(self,foodname,num_recipe=3):

        #get food name as keyword
        keyword = foodname

        #convert keyword into unicode
        keyword = str(keyword.encode('utf-8')).lstrip("b'").rstrip("'").replace("\\x","%")

        # get url
        url = 'http://www.10000recipe.com/recipe/list.html?q=' + keyword

        #connect to the site
        response = requests.get(url)

        html = response.text



        #parse using BS
        soup = BS(html,'lxml')

        #get cookbook link

        if soup.find("a","thumbnail") == None:
            recipe = ''
            recipe_list = []
        else:
            cook_link_list = soup.find_all('a',"thumbnail")

            cook_urls = []

            for cook_links in cook_link_list:
                cook_link =cook_links['href']
                cook_urls.append('http://www.10000recipe.com' + cook_link)
            cook_urls = cook_urls[0:num_recipe]


            #connect to the site
            recipe_list = []
            for cook_url in cook_urls:
                response = requests.get(cook_url)

                html = response.text

                #parse using BS
                soup2 = BS(html,'lxml')
                contents = soup2.find_all('meta',{'name':"keywords"})

                #get recipe
                recipe_content = contents

                recipe = ''

                for rec in recipe_content:
                    recipe = recipe +str(rec['content'])

                #replace useless tokens
                #recipe = recipe.replace('text/html; charset=euc-kr','')
                #recipe = recipe.replace('\r\n','')
                #recipe = re.sub('http.+','',recipe)
                recipe_list.append(recipe)

        return recipe_list

    def crawl(self,food_detail_df):
        print('[Recipe Web Crawling Start]')
        for index in range(len(food_detail_df)):

            food = food_detail_df.foodName[index]
            recipe = self,recipe_finder(food,2)
            food_detail_df.loc[index ,'foodRecipe'] = str(recipe)

            if (index+1) % 5 == 0:
                print(round((index+1)/len(food_df)*100,2),'percent Done')

        print('Complete!!')
        print('')
        print('[noun extract start]')

        food_detail_df['foodRecipeNoun'] = ''
        for i in range(len(food_detail_df)):

            doc = food_detail_df.foodRecipe[i]
            noun = Hannanum().nouns(doc)
            cnt = Counter(noun)
            only_word = []
            for key, value in cnt.items():
                if int(value) < 3:
                    noun.remove(key)
            for word in noun:
                m = re.match('^\D*\D$',word)
                if m:
                    only_word.append(m.group())

            food_detail_df.loc[i,'foodRecipeNoun'] = str(only_word)
            if (i % 5) == 0:
                print(round(i/len(food_detail_df)*100,2), ' perent done')
        print('Complete')

    def NLP(self,food_detail_df):

        print('[noun extract start]')

        food_detail_df['foodRecipeNoun'] = ''
        for i in range(len(food_detail_df)):

            doc = food_detail_df.foodRecipe[i]
            noun = Hannanum().nouns(doc)

            for word in noun:
                word = word.replace('ㅎ','').replace('ㅋ','').replace('ㅜㅜ','').replace('ㅠㅠ','').replace('\\n','')

            cnt = Counter(noun)
            only_word = []
            for key, value in cnt.items():


                #if (len(key) < 2)|(len(key) > 6):
                    #noun.remove(key)

                if int(value) < 3:
                    noun.remove(key)

            for word in noun:


                m = re.match('^\D*\D$',word)
                if m:
                    only_word.append(m.group())

            food_detail_df.loc[i,'foodRecipeNoun'] = str(only_word)
            if (i % 5) == 0:
                print(round(i/len(food_detail_df)*100,2), ' perent done')
        print('Complete')

    def replace_useless(self,food_detail_df):
        count=0
        for word in food_detail_df['foodRecipeNoun']:
            food_detail_df['foodRecipeNoun'][count] = word.replace("[","").replace("]","").replace("'","").replace(","," ")\
            .replace("ㅎ","").replace("ㅋ","").replace("ㅜ","").replace("n","")
            count = count + 1
