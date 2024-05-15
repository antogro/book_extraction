#importé les package necessaire pour récuperer les infos des livres
import requests
from bs4 import BeautifulSoup
from slugify import slugify 
from pathlib import Path
import pathlib
import pandas as pd
from urllib.parse import urlparse, urljoin
import urllib.parse
import re

############################# Extraction / Transformation ###########################
def get_soup(url):
    """retrieve all the information of the url"""
    SESSION = requests.session()
    reponses = SESSION.get(url)
    if reponses.ok:
        soup = BeautifulSoup(reponses.content, 'html.parser')
        if soup is None:
            print('Une erreur est survenue lors de l\'extraction de donnée')
        return soup
    

def get_category_urls(url):
    """retrieve category link"""
    category_link = []
    soup = get_soup(url)
    tul = soup.find('ul', 'nav nav-list')
    li_list = tul.find_all('li')
    for li in li_list:
        a = li.find(['a'])
        link = a['href']
        link.replace('../', '')
        category_link.append('https://books.toscrape.com/' + link)
        category_links = category_link[1:]

    return category_links


def get_books_urls(url):
    """retrieve all the url of the book on the curent page"""
    links = []
    soup = get_soup(url)
    tdl = soup.findAll('h3')
    for td in tdl:
        a = td.find('a')
        link = a['href']
        link = link.replace('../', '')
        links.append('https://books.toscrape.com/catalogue/' + link)

    return links


def get_next_page(url):
    """retrieve the link of the next page if there is"""
    soup = get_soup(url)
    next_page = soup.find('li', 'next')
    if not next_page:
        return None
    else:
        next_page_link = next_page.find('a')['href']
        parse_url = urllib.parse.urlparse(url)
        base_url = f'{parse_url.scheme}://{parse_url.netloc}{parse_url.path.rsplit('/', 1)[0]}/' 
        next_page_url = urljoin(base_url, next_page_link)

    return next_page_url


def get_one_category_data():
    """retrieve category name, and category url after a input"""
    category_url = get_category_urls('https://books.toscrape.com/catalogue/category/books_1/index.html')
    category_data = []
    for row in category_url:
        url = row.strip()
        urls_category = url.replace('https://books.toscrape.com/../', 'https://books.toscrape.com/catalogue/category/')
        try:
            reponses = requests.get(url)
            parsed_url = urlparse(reponses.url)
            category = parsed_url.path.split('/')[-2]
            category = category.rstrip('_0123456789').rstrip('_')
            category_data.append({'category_name': category, 'category_url': urls_category})
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {url}: {e}")
    for i, category_dict in enumerate(category_data, start=1):
        print(f"{i}. {category_dict['category_name']}")
    try:
        category_index = int(input("Entrer le numéro de la catégorie choisie: "))
        
        if 1 <= category_index <= len(category_data):
            print(f'Vous avez choisie la catégorie : {category_data[category_index -1]['category_name']}')
            category_url = category_data[category_index -1]['category_url']
            print(category_url)    
        else:
            print("Le numéro de la catégorie choisie n'est pas valide")
           
    except:
        print("L'entrée saisie de la catégorie n'est pas valide")

    return category_url


def reviews_rating(soup):
    """retrieve review rating"""
    star = soup.findAll('p', 'star-rating')
    if star:
        star_rating = star[0].get('class')[-1]
        if star_rating == 'One':
            star_rating = 1
        elif star_rating == 'Two':
            star_rating = 2
        elif star_rating == 'Three':
            star_rating = 3
        elif star_rating == 'Four':
            star_rating = 4
        elif star_rating == 'Five':
            star_rating = 5

    return star_rating


#extract book informartion: UPC, price including taxe, price exluding taxe, number available, star rating, category 
def get_book_data(url):
    """retrieve information from each book"""
    book_data = {}
    th_list=[]
    td_list = []
    soup = get_soup(url)

    #extrcat book information (UPC, price taxe, price without taxe, stocks)
    tds = soup.findAll('th')

    th_list = [th.get_text() for th in tds if th.get_text()]
    tds = soup.findAll('td')
    td_list = [td.get_text() for td in tds if td.get_text()]
    product_informations = {th_list[i]: td_list[i] for i in range(len(th_list))}
   
    del product_informations['Product Type'], product_informations['Tax'],  product_informations['Number of reviews']

    paragraphe_description = soup.find(id = 'content_inner')

    #extrcat category book
    category = soup.find('ul', 'breadcrumb')
    li_list = category.find_all('li', limit = 4)
    if len(li_list) >=3:
        book_category = li_list[2].a.get_text()

    #book data dictionnary
    book_data = {
        'title': soup.find('h1').get_text(),
        'category': book_category,
        'star_rating': reviews_rating(soup),
        'url': url,
        'picture_url': get_image_url(soup),
        'description': paragraphe_description.findAll('p')[3].get_text()
    }
    book_data.update(product_informations)

    
    book_data['Availability'] = int(re.search(r'\((\d+) available\)', book_data['Availability']).group(1))

    return book_data

def get_image_url(soup):
    """retrieve books url"""
    books_pict = {}
    image_url = soup.find(class_= 'item active')
    image = image_url.find('img')
    link_image = str(image['src'])
    link = link_image[5:]
    books_pict = 'https://books.toscrape.com/' + link

    return books_pict

get_book_data('https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html')

def save_picture_to_folder(book_data: dict):
    """Save book image to folder"""
    if not isinstance(book_data, list):
        book_data = [book_data]

    picture_url = book_data[0]['picture_url']
    cat_folder_path = pathlib.Path('data') / slugify(book_data[0]['category'])
    image_full_path = cat_folder_path / (slugify(book_data[0]['title']) + '.jpg')
    
    if not cat_folder_path.exists():
        cat_folder_path.mkdir(parents = True, exist_ok = True)
    if image_full_path.exists():
        image_full_path = image_full_path.with_name(f"{image_full_path.stem}-{book_data[0]['UPC']}.jpg")
    book_data[0]['image_path'] = image_full_path.as_posix()
    try:
        res = requests.get(picture_url)
        res.raise_for_status()
        with open(image_full_path, 'wb') as file:
            file.write(res.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
    else:
        pass

    return book_data


def write_book_to_csv(book_data: dict | list[dict]):
    """Write book data to a csv files"""
    if not isinstance(book_data, list):
        book_data = [book_data]

    category = slugify(book_data[0].get('category'))
    cat_folder_path = pathlib.Path('data')

    if not cat_folder_path.exists():
        cat_folder_path.mkdir(parents = True, exist_ok = True)
    
    csv_file_name = cat_folder_path / f'{category}.csv'
    fieldnames = book_data[0].keys()

    if not Path(csv_file_name).exists():
        df = pd.DataFrame(columns=fieldnames)
        df.to_csv(csv_file_name, index=False)

    df = pd.DataFrame(book_data)
    df.to_csv(csv_file_name, mode='a', index=False, header=False)