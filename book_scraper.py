#importé les package necessaire pour récuperer les infos des livres
import requests
from bs4 import BeautifulSoup
import pep8
from urllib.parse import urlparse
import slugify
import os

#lien de la page d'accueille à scrapper
#
url = 'https://books.toscrape.com/'
SESSION = requests.session()

labels = ['Title', 'UCP', 'Price Excl TAX','Price Includ TAX', 'Nombre available', 
          'Review Rating', 'Category', 'Produc description', 'URL']



def get_soup(url):
    """récupérer les informations du site web"""
    reponses = SESSION.get(url)
    if reponses.ok:
        soup = BeautifulSoup(reponses.content, 'html.parser')
        if soup is None:
            print('Une erreur est survenue lors de l\'extraction de donnée')
        return soup
    

def get_url_category(url):
    """récupérer les liens des catégories"""
    category_link = []
    soup = get_soup(url)
    tul = soup.find('ul', 'nav nav-list')
    li_list = tul.find_all('li')
    for li in li_list:
        a = li.find(['a'])
        link = a['href']
        link = link.replace('../', '')
        category_link.append('https://books.toscrape.com/' + link)
        category_links = category_link[1:]
    return(category_links)


def get_Url(url):
    """récuperer les lien de la page à scrapper"""
    links = []
    soup = get_soup(url)
    tdl = soup.findAll('h3')
    #On recuperer les liens de la 1er page
    for td in tdl:
        a = td.find('a')
        link = a['href']
        link = link.replace('../', '')
        links.append('https://books.toscrape.com/catalogue/' + link)
    return(links)


def get_next_page(url):
    #récuperer les autres pages
    soup = get_soup(url)
    next_page = soup.find('li', 'next')
    if next_page == None :
        return None
    else:
        a = next_page.find('a')
        next_page_link = a['href']
        link = url[:-10] + next_page_link
    
    return link


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
        if key == 'UPC' :
            book_data[key]= ''.join(c for c in value if c.isdigit() or c =='.')
        if key == 'Price (excl. tax)' :
            book_data[key]= ''.join(c for c in value if c.isdigit() or c =='.')
        if key == 'Price (incl. tax)':
            book_data[key]=''.join(c for c in value if c.isdigit() or c =='.')
        if key == 'Availability' :
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
        book_data['Star rating'] = star_rating

    #récuperer la catégorie du livre    
    category = soup.find('ul', 'breadcrumb')
    li_list = category.find_all('li', limit = 4)
    if len(li_list) >=3:
        book_category = li_list[2].get_text()
        book_data['Book category'] = book_category

    book_data['title'] = soup.find('h1').get_text()
    #print(book_data['Book category'])

    for urls in url:
        book_data['URL'] = url
    
    return(book_data)   


def get_category_book(url):
    """récuperer les category de chaque livre"""   
    book_category = [] 
    soup = get_soup(url)
    category = soup.find('ul', 'breadcrumb')
    #récuperer la catégorie se trouvant à la 3éme place de la liste    
    li_list = category.find_all('li', limit = 4)
    if len(li_list) >=3:
        book_category = li_list[2].get_text()
    return(book_category)




def get_image_url(url):
    """récuperer l'Url de l'image de chaque livre"""
    url_image = []
    soup = get_soup(url)
    image_url = soup.find(class_= 'item active')
    image = image_url.find('img')
    link_image = str(image['src'])
    link = link_image[5:]
    url_image.append('https://books.toscrape.com/' + link)
    return url_image



def write_book_to_csv(book_data):   
    csv = 'C:/Users/anton/OneDrive/Bureau/openclassroom/book_extraction_scraper/book_extraction/csv'
    if not os.path.exists(csv):
        os.makedirs(csv)
        for category, book in book_data.items():
            category = slugify(category)
            file_name = os.path.join(csv, f'{category}.csv')
            if not os.path.exists(file_name):
                with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=books[0].keys)
                    writer.writeheader()
                with open(file_name, 'a', encoding='utf-8-sig', newline=''):
                    writer = csv.DictWriter(file, fieldnames=books[0].keys)
                    writer.writerows(books)


def main():
# Récupérer la liste des urls des catégories Pour chaque url de la liste des urls des catégories 
    PRIMARI_URL = 'https://books.toscrape.com/'
    book_data = []
    book_image = []  
    
    category = get_url_category(PRIMARI_URL)
   
    for categories in category:
     # Récupérer la liste des urls des livres de la catégorie (Gérer le multi page)    
        book_url = get_Url(categories) 
         
        # Pour chaque url des livres Récupérer les données du livre 
        while get_next_page(categories) is not  None: 
            next_page = get_next_page(categories)
            next_page_url  = get_Url(next_page)
            book_url.extend(next_page_url)
       # Pour chaque url des livres Récupérer les données du livre      
        for url in book_url:
            try :
                book_data_dict = get_book_data(url)
                book_image_dict = get_image_url(url)
                book_data.append(book_data_dict)
                book_image.append(book_image_dict)
        
            except Exception as e:
                        print(f"Erreur lors de la récupération des données pour {url}: {e}")
        write_book_to_csv(book_data)
        write_book_to_csv(book_image)





# (sous forme de dictionnaire et stocker le tout dans une liste)
# Sauvegarder le résultat (les données des livres) dans un fichier csv
# Sauvegarder les images des livres de la catégories (comprend la requête pour récupérer le contenu)

    
   
    
   
    
   #get_next_page(url)

if __name__=='__main__':
    #get_description(url)
    #
    #get_Url(url)
    main()
    #get_url_category(url)
    #get_next_page(url)
    #get_category_book(url)
    #get_all_category_name()