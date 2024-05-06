#importé les package necessaire pour récuperer les infos des livres
import requests
from bs4 import BeautifulSoup
from slugify import slugify 
import csv
import os
from urllib.parse import urlparse
import datetime


#lien de la page d'accueille à scrapper
#
url = 'https://books.toscrape.com/'
SESSION = requests.session()


def get_soup(url):
    """récupérer les informations du site web"""
    reponses = SESSION.get(url)
    if reponses.ok:
        soup = BeautifulSoup(reponses.content, 'html.parser')
        if soup is None:
            print('Une erreur est survenue lors de l\'extraction de donnée')
        return soup
    

def get_category_urls(url):
    """récupérer les liens des catégories"""
    category_link = []
    soup = get_soup(url)
    tul = soup.find('ul', 'nav nav-list')
    li_list = tul.find_all('li')
    for li in li_list:
        a = li.find(['a'])
        link = a['href']
        urls_category = link.replace('../', '')
        category_link.append('https://books.toscrape.com/' + link)
        category_links = category_link[1:]

    return category_links


def get_books_urls(url):
    """récuperer les lien des livres la page à scrapper"""
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
    """récuperer le lien de la page suivante"""
    soup = get_soup(url)
    next_page = soup.find('li', 'next')
    if not next_page:
        return None
    else:
        a = next_page.find('a')
        next_page_link = a['href']
        link = url[:-10] + next_page_link
    
    return link


def get_all_category_name():
    """Fonction qui permet de récupérer le nom des catégories"""
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

#récuperer les informations de chaque livre
#code UPC, price including taxe, price exluding taxe,
# number available,  
def get_book_data(url):
    """récuperer les informations de chaque livre"""
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
    for key, value in product_informations.items():
        if key == 'UPC':
            book_data[key]= ''.join(c for c in value if c.isdigit() or c =='.')
        if key == 'Price (excl. tax)':
            book_data[key]= ''.join(c for c in value if c.isdigit() or c =='.')
        if key == 'Price (incl. tax)':
            book_data[key]=''.join(c for c in value if c.isdigit() or c =='.')
        if key == 'Availability':
            book_data[key]=''.join(c for c in value if c.isdigit())
            
    #récuperer la description du livre
    paragraphe_description = soup.find(id = 'content_inner')
    if paragraphe_description:
        description = paragraphe_description.findAll('p')[3].get_text()
        book_data['description'] = description

    #récuperer la note du livre
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
        book_data['Star rating'] = star_rating


    #récuperer la catégorie du livre
    category = soup.find('ul', 'breadcrumb')
    li_list = category.find_all('li', limit = 4)
    if len(li_list) >=3:
        book_category = li_list[2].a.get_text()
        book_data['category'] = book_category

    book_data['title'] = soup.find('h1').get_text()

    for urls in url:
        book_data['URL'] = url
    
    return book_data


def get_image_url(url):
    """récuperer l'Url de l'image de chaque livre"""
    books_pict = {}
    soup = get_soup(url)
    image_url = soup.find(class_= 'item active')
    image = image_url.find('img')
    link_image = str(image['src'])
    link = link_image[5:]
    books_pict['title'] = image['alt']
    books_pict['image_url'] = 'https://books.toscrape.com/' + link
    return books_pict

   
#rajouter date et heure au nom du fichier
def write_book_to_csv(book_data):
    """Ecrire les données des livres dans un fichier CSV"""
    category = slugify(book_data[0].get('category'))
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join('../data_picture_file', 'data_book_csv')
    file_name = os.path.join(folder_path, f'{category}.csv')
    fieldnames = book_data[0].keys()

    #créer un dossier csv si il n'existe pas
    if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(book_data)


def save_picture_to_folder(books_pict):
    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join('../data_picture_file', 'book_images')

    for books in books_pict:
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        date_folder_path = os.path.join(folder_path, date_str)
        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)
        file_name = slugify(books.get('title')) + '.jpg'
        image_url = books['image_url']
        full_path = os.path.join(date_folder_path, file_name)
        if file_name not in date_folder_path:
            try:
                res = requests.get(image_url)
                res.raise_for_status()  # Raise an exception for unsuccessful requests (status codes not 2xx)
                with open(full_path, 'wb') as file:
                    file.write(res.content)
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")  # Log or handle download errors
        else:
            pass