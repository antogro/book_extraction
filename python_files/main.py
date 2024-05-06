import book_scraper as bs
import all_category_scraper as all_category_scraper
import time


def time_mode(nb_sec):
     q,s=divmod(nb_sec,60)
     h,m=divmod(q,60)
     return "%d:%d:%d" %(h,m,s)


def main():
    """Fonction principale d\'extraction de livre."""
    print('Bienvenue dans l\'application d\'extraction de livre!')
    start = time.time()
    print('Que souhaitez-vous scraper')
    print('1 : Ecrivez 1 si vous souhaitez scraper toutes les donneés de toutes les catégories')
    print('2 : Ecrivez 2 si vous souhaitez scraper les données d\'une catégorie')
    print('3 : Ecrivez 3 si vous souhaitez scraper les données d\'un livre')
    print('4 : Ecrivez 4 si vous souhaitez Quittezl\'application d\'extraction de livre.')
    choice = input('Votre choix : ')

    if choice == '1':
        print('Vous avez fait le choix 1, vous allez télécharger toutes les données de tout les livres dans un fichier CSV')
        all_category_scraper.all_category_scraper()
        during_time = time.time() - start
        time_code = (time_mode(during_time))
        return time_code

    elif choice == '2':
        print('Vous avez fait le choix 2, patientez quelque instant pour indiquer la catégorie souhaitez.')
        books_data = []
        books_pict = []
        one_category_url = bs.get_all_category_name()
        books_url = bs.get_books_urls(one_category_url)

        while bs.get_next_page(one_category_url) is not None:
            next_page_url = bs.get_next_page(one_category_url)
            next_page_book_url = bs.get_books_urls(next_page_url)
            books_url.extend(next_page_book_url)
            break

        for url in books_url:
            books_data_dict = bs.get_book_data(url)
            books_pict_dict = bs.get_image_url(url)
            
            books_data.append(books_data_dict)
            books_pict.append(books_pict_dict)
            
        bs.write_book_to_csv(books_data)
        bs.save_picture_to_folder(books_pict)
        during_time = time.time() - start

        time_code = (time_mode(during_time))
        return time_code

    elif choice == '3':
        books_pict = []
        books_data = []

        print('Vous avez fait le choix 3, vous allez maintenant télécharger toutes les données d\'un seul livre dans un fichier CSV.')
        one_book_url = input('Veuillez coller l\'url du livre à scraper: ')
        
        books_data_dict = bs.get_book_data(one_book_url)
        books_pict_dict = bs.get_image_url(one_book_url)

        books_data.append(books_data_dict)
        books_pict.append(books_pict_dict)
        
        bs.write_book_to_csv(books_data)
        bs.save_picture_to_folder(books_pict) 
        during_time = time.time() - start

        time_code = (time_mode(during_time))
        return time_code

    elif choice == '4':
        print('Vous avez fait le choix 4, vous allez maintenant quitter l\'application.')
        exit()

    else:
        print('Vous n\'avez pas fait le bon choix! Veuillez écrire un chiffre entre 1 et 4!')
        

if __name__ == '__main__':
    print("Début du programme")
    
    time_code = main()
    
    print(f'Fin du programme en {time_code} min/sec, merci d\'avoir utilisé l\'application books-to-scrap, passez une agréable journée!')