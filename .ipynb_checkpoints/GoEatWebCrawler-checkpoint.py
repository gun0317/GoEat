import requests
from bs4 import BeautifulSoup as BS
import re

def recipe_finder(foodname,num_recipe=3):

    #get food name as keyword
    keyword = foodname

    #convert keyword into unicode
    keyword = str(keyword.encode('EUC-KR')).lstrip("b'").rstrip("'").replace("\\x","%")

    # get url
    url = 'https://www.menupan.com/search/cook/cookbook_result.asp?sc=all&kw=' + keyword +'&srt=rank'

    #connect to the site
    response = requests.get(url)
    response.encoding = None
    html = response.text



    #parse using BS
    soup = BS(html,'lxml')

    #get cookbook link

    if soup.find("dt").find('a') == None:
        recipe = ''
        recipe_list = []
    else:
        cook_link_list = soup.find_all("dt")

        cook_urls = []

        for cook_links in cook_link_list:
            cook_link =cook_links.find('a')['href']
            cook_urls.append('https://www.menupan.com' + cook_link)
        cook_urls = cook_urls[0:num_recipe]


        #connect to the site
        recipe_list = []
        for cook_url in cook_urls:
            response = requests.get(cook_url)
            response.encoding = None
            html = response.text

            #parse using BS
            soup2 = BS(html,'lxml')
            contents = soup2.find_all('meta')

            #get recipe
            recipe_content = contents

            recipe = ''

            for rec in recipe_content:
                recipe = recipe +str(rec['content'])

            #replace useless tokens
            recipe = recipe.replace('text/html; charset=euc-kr','')
            recipe = recipe.replace('\r\n','')
            recipe = re.sub('http.+','',recipe)
            recipe_list.append(recipe)

    return recipe_list
