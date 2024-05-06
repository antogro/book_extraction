import book_scraper as bs
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
    
# Récupérer la liste des urls des catégories Pour chaque url de la liste des urls des catégories 
    category_url = bs.get_category_urls(PRIMARI_URL)
   
    for categories in category_url:
        book_data = []
        book_image = []
        picture_book_url = []

     # Récupérer la liste des urls des livres de la catégorie (Gérer le multi page)
        book_url = bs.get_books_urls(categories) 
         
        # Pour chaque url des livres Récupérer les données du livre 
        while bs.get_next_page(categories) is not  None:
            next_page = bs.get_next_page(categories)
            next_page_url  = bs.get_books_urls(next_page)
            book_url.extend(next_page_url)
            break
            
       # Pour chaque url des livres Récupérer les données du livre
        for url in book_url:
            book_data_dict = bs.get_book_data(url)
            book_image_dict = bs.get_image_url(url)
            # Sauvegarder le résultat (les données des livres) dans un fichier csv                
            book_data.append(book_data_dict)
            book_image.append(book_image_dict)
        category_name = get_category_name()

        for category in category_name:
            bs.write_book_to_csv(book_data)
            bs.save_picture_to_folder(book_image)
       


