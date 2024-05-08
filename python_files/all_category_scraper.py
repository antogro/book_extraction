import python_files.book_scraper as bs
import requests
from urllib.parse import urlparse


def get_category_name():
    """Fonction qui permet de récupérer le nom des catégories"""
    category_url = bs.get_category_urls('https://books.toscrape.com/catalogue/category/books_1/index.html')
    category_name = set()
    for row in category_url:
        url = row.strip()
        try:
            reponses = requests.get(url)
            parsed_url = urlparse(reponses.url)
            category = parsed_url.path.split('/')[-2]
            category = category.rstrip('_0123456789').rstrip('_')
            category_name.add(category)
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {url}: {e}")
        return category_name


def all_category_scraper():
    """Fonction principale d'extraction/sauvegarde du site Books.toscrap"""
    PRIMARI_URL = 'https://books.toscrape.com/'
    
# Récupérer la liste des urls des catégories Pour chaque des catégories 
    category_url = bs.get_category_urls(PRIMARI_URL)
   
    for categories in category_url:
        book_data = []
        book_image = []
        books_url = []
        picture_book_url = []

     # Récupérer la liste des urls des livres de la catégorie (Gérer le multi page)
        books_url = bs.get_books_urls(categories) 

        # Pour chaque url des livres Récupérer les données du livre 
        while True:
            next_page_url = bs.get_next_page(categories)
            if next_page_url is None:
                break

            categories = next_page_url
            books_url.extend(bs.get_books_urls(categories))
            
       # Pour chaque url des livres Récupérer les données du livre
        for url in books_url:
            book_data_dict = bs.get_book_data(url)
            book_image_dict = bs.get_image_url(url)
            # Sauvegarder le résultat (les données des livres) dans un fichier csv
            book_data.append(book_data_dict)
            book_image.append(book_image_dict)
        category_name = get_category_name()

        for category in category_name:
            bs.write_book_to_csv(book_data)
            bs.save_picture_to_folder(book_image)


def one_category_scraper():
    """Scraper pour une catégorie donnée"""
    books_data = []
    book_picture = []

    one_category_url = bs.get_one_category_data()
    books_url = bs.get_books_urls(one_category_url)

    while True:
        next_page_url = bs.get_next_page(one_category_url)
        if next_page_url is None:
            break
        one_category_url = next_page_url
        books_url.extend(bs.books_data(one_category_url))
    
    for url in books_url:
        
        books_data.append(bs.get_book_data(url))
        book_picture.append(bs.get_image_url(url))

    bs.write_book_to_csv(books_data)
    bs.save_picture_to_folder(book_picture)

def one_book_scraper(one_book_url):
    book_data = []
    book_picture = []

    book_data.append(bs.get_book_data(one_book_url))
    book_picture.append(bs.get_image_url(one_book_url))

    bs.write_book_to_csv(book_data)
    bs.save_picture_to_folder(book_picture)
    