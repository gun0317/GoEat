import requests
from bs4 import BeautifulSoup as BS
import re

def recipe_finder(foodname,num_recipe=3):

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
