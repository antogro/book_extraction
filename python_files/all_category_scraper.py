import python_files.book_scraper as bs


def all_category_scraper():
    """Scraping of all the website 'Book-to-scrap'"""
    PRIMARI_URL = 'https://books.toscrape.com/'
    
# Récupérer la liste des urls des catégories Pour chaque des catégories 
    category_url = bs.get_category_urls(PRIMARI_URL)
   
    for categories in category_url:
        books_data = [] 
        books_url = []

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
            # Sauvegarder le résultat (les données des livres) dans un fichier csv
            books_data.append(book_data_dict)
    
        for book in books_data:
            book_data_url = bs.save_picture_to_folder(book)
            bs.write_book_to_csv(book_data_url)


def one_category_scraper():
    """Scraping of one category book"""
    books_data = []

    one_category_url = bs.get_one_category_data()
    books_url = bs.get_books_urls(one_category_url)

    while True:
        next_page_url = bs.get_next_page(one_category_url)
        if next_page_url is None:
            break

        one_category_url = next_page_url
        books_url.extend(bs.get_books_urls(one_category_url))
    
    for url in books_url:
        books_data.append(bs.get_book_data(url))

    for book in books_data:
        book_data_url = bs.save_picture_to_folder(book)
        bs.write_book_to_csv(book_data_url)
    

def one_book_scraper(one_book_url):
    """Sraping of one book"""
    books_data = []

    books_data.append(bs.get_book_data(one_book_url))

    book_data_url = bs.save_picture_to_folder(books_data)
    bs.write_book_to_csv(book_data_url)
    
    