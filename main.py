import time

from python_files import all_category_scraper 

def time_mode(nb_sec):
     q,s=divmod(nb_sec,60)
     h,m=divmod(q,60)
     return "%d:%d:%d" %(h,m,s)


def main():
    """Fonction principale d\'extraction de livre."""
    start = time.time()
    duration = []
    end_phrase = [f'Fin du programme en {duration} min/sec, merci d\'avoir utilisé l\'application books-to-scrap, passez une agréable journée!']
    print('Bienvenue dans l\'application d\'extraction de livre!')
    
    print('Que souhaitez-vous scraper')
    print('1 : Ecrivez 1 si vous souhaitez scraper toutes les données de toutes les catégories')
    print('2 : Ecrivez 2 si vous souhaitez scraper les données d\'une catégorie')
    print('3 : Ecrivez 3 si vous souhaitez scraper les données d\'un livre')
    print('4 : Ecrivez 4 si vous souhaitez Quittez l\'application d\'extraction de livre.')
    
    while True:
        choice = input('Votre choix : ')
        try:
            choice = int(choice)
        except ValueError:
            print('Vous devez entrer un nombre entre 1 et 4')
            continue
        if choice == 1:
            print('Vous avez fait le choix 1, vous allez télécharger toutes les données de tout les livres dans un fichier CSV.')
            
            all_category_scraper.all_category_scraper()
           
            duration = (time_mode(time.time() - start))
            break

        elif choice == 2:
            print('Vous avez fait le choix 2, patientez quelque instant pour indiquer la catégorie souhaitez.')

            all_category_scraper.one_category_scraper()
            
            duration = (time_mode(time.time() - start))
            break
        elif choice == 3:
            PRIMARI_URL = 'https://books.toscrape.com/'
            print('Vous avez fait le choix 3, vous allez maintenant télécharger toutes les données d\'un seul livre dans un fichier CSV.')
            
            one_book_url = input(f'Veuillez coller l\'url du livre à scraper en allant sur le site web {PRIMARI_URL}: ')
            all_category_scraper.one_book_scraper(one_book_url)

            duration = (time_mode(time.time() - start))
            break
        elif choice == 4:
            print('Vous avez fait le choix 4, vous allez maintenant quitter l\'application.')
            break
        else:
            print('Vous n\'avez pas fait le bon choix! Veuillez écrire un chiffre entre 1 et 4!')
            continue

    return duration
        
        
        

if __name__ == '__main__':
    print("Début du programme")
    
    duration = main()
    
    print(f'Fin du programme en {duration} min/sec, merci d\'avoir utilisé l\'application books-to-scrap, passez une agréable journée!')
    

      
    