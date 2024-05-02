import book_scraper as bs

def main():
    """Fonction principale d'extraction/sauvegarde du site Books.toscrap"""
# Récupérer la liste des urls des catégories Pour chaque url de la liste des urls des catégories 
    PRIMARI_URL = 'https://books.toscrape.com/'
    book_data = []
    book_image = []
    
    category_url = bs.get_url_category(PRIMARI_URL)
    print(category_url)
   
    for categories in category_url:
     # Récupérer la liste des urls des livres de la catégorie (Gérer le multi page)
        book_url = bs.get_Url(categories) 
        print(book_url)
         
        # Pour chaque url des livres Récupérer les données du livre 
        while bs.get_next_page(categories) is not  None:
            next_page = bs.get_next_page(categories)
            next_page_url  = bs.get_Url(next_page)
            print(next_page_url)
            book_url.extend(next_page_url)
            break
            
       # Pour chaque url des livres Récupérer les données du livre
        for url in book_url:
            try :
                book_data_dict = bs.get_book_data(url)
                print(book_data_dict)
                book_image_dict = bs.get_image_url(url)
                print(book_image_dict)
                # Sauvegarder le résultat (les données des livres) dans un fichier csv                
                book_data.append(book_data_dict)
                book_image.append(book_image_dict)
        
            except Exception as e:
                        print(f"Erreur lors de la récupération des données pour: {e}")
        bs.write_book_to_csv(book_data)
        #write_book_to_csv(book_image)

if __name__ == '__main__':
    print("Début du programme")
    try:
        #main()
        bs.get_image_url('https://books.toscrape.com/catalogue/the-mysterious-affair-at-styles-hercule-poirot-1_452/index.html')
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour: {e}")

    finally:
        print("Fin du programme")