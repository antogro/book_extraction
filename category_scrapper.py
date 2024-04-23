 #importé les package necessaire pour récuperer les infos des livres
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse




urls = 'https://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html'

reponses = requests.get(urls)
category_link = []

#Récuperer les urls des categories
def get_url_category():
    urls = 'https://books.toscrape.com/index.html'
    reponses = requests.get(urls)
    if reponses.ok: 
        soup = BeautifulSoup(reponses.text, 'html.parser')
        tul = soup.find('ul', 'nav nav-list')
        li_list = tul.find_all('li')
        for li in li_list:
            a = li.find(['a'])
            link = a['href']
            #   .get('href')
            category_link.append('https://books.toscrape.com/' + link)
            return category_link

get_url_category()           
          
#Enregistrer les urls des catégories dans un fichier csv

for url in category_link:
    parsed_url = urlparse(url)
    category_name = parsed_url.path.split('/')[-2]
print(category_name) 


books = [
    {'Title' : '', 'UCP':'', 'Price Excl TAX': '','Price Includ TAX':'', 'Nombre available':'', 
          'Review Rating' :'', 'Category': '', 'Produc description': '', 'URL' :''}]






    
"""

#récuperer les autres pages
def get_next_page(reponses):
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')
        next_page = soup.find('li', 'next')
        if next_page == None :
            return
        else:
            a = next_page.find('a')
            next_page_link = a['href']
            return next_page_link
      




#ouverture du fichier csv pour scraper les urls des livres
#dans les différentes catégories 
def get_all_page_category():
    with open('urls_category.csv', 'r') as file:
        for row in file:
            url = row.strip()
        reponses = requests.get(url)
        if reponses.ok:
            for link in get_next_page(reponses):
                for each with open('urls_category_books.csv', 'w') as file:
get_all_page_category()


with open('urls_category.csv', 'w') as file:
    for link in category_link:
        file.write(link + '\n')
"""


