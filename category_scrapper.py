 #importé les package necessaire pour récuperer les infos des livres
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
import csv
import book_scraper as bscrap
import pep8


urls = 'https://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html'

reponses = requests.get(urls)
category_link = []

#Récuperer les urls des categories
def get_url_category():
    urls = 'https://books.toscrape.com/index.html'
    reponses = requests.get(urls)
    if reponses.ok: 
        soup = BeautifulSoup(reponses.content, 'html.parser')
        tul = soup.find('ul', 'nav nav-list')
        li_list = tul.find_all('li')
        for li in li_list:
            a = li.find(['a'])
            link = a['href']
            #   .get('href')
            category_link.append('https://books.toscrape.com/' + link)
        return(category_link)

get_url_category()       

#Ecrire les urls dans un fichier csv
with open('csv/urls_category.csv', 'w') as file:
    for link in category_link:
        file.write(link + '\n')



links = []

#ouverture du fichier csv pour scraper les urls des livres
#dans les différentes catégories 
#récuperer tout les liens de toute les pages des différentes catégories
def get_all_url():
    with open('csv/urls_category.csv', 'r') as file:
        for row in file:
            url = row.strip()               
            links = bscrap.get_Url(url)
        for category in list(links):
            with open(f'{category}.csv', 'w') as file:
                writer = csv.DictWriter('url', fieldnames= links)
                writer.writeheader()
                
                
get_all_url()



          
category_name = set()
#récuperer toute les différentes catégories venant du CSV Url 
def get_all_category_name():
    
    with open('csv/urls_category.csv', 'r') as file:
        for row in file:
            url = row.strip()
            reponses = requests.get(url)
            parsed_url = urlparse(reponses.url)
            category = parsed_url.path.split('/')[-2]
            if category.endswith(('0','1','2','3','4','5','6','7','8','9')):
                category = category[:-2]
            if category.endswith('_'):
                category = category[:-1]
            if category not in category_name:
                category_name.add(category)
    return category_name
    
get_all_category_name()


labels = ['Title', 'UCP', 'Price Excl TAX','Price Includ TAX', 'Nombre available', 
          'Review Rating', 'Category', 'Produc description', 'URL']   


#créée un fichier csv par catégorie avec le titre pour chaque donnée à scrapper
def write_category_csv(category_name):
    for category in list(category_name):
        with open(f'csv/{category}.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=labels)
            writer.writeheader()
            


category_name = get_all_category_name()
write_category_csv(category_name)








#récuperer les autres pages

def get_next_page(reponses):
    if reponses.ok:
        soup = BeautifulSoup(reponses.content, 'html.parser')
        next_page = soup.find('li', 'next')
        if next_page == None :
            return
        else:
            a = next_page.find('a')
            next_page_link = a['href']
            return next_page_link
