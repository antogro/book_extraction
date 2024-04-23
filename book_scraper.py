 #importé les package necessaire pour récuperer les infos des livres
import requests
from bs4 import BeautifulSoup


links = []
#lien de la page d'accueille à scrapper
urls = 'https://books.toscrape.com/index.html'



#récuperer les lien de la 1er page à scrapper 
def get_Url():
    reponses = requests.get(urls)
    if reponses.ok:
    #On cherche tout les liens contenus dans la balise h3
        soup = BeautifulSoup(reponses.text, 'html.parser')
        tdl = soup.findAll('h3')

        #On recuperer les liens de la 1er page
        for td in tdl:
            a = td.find('a')
            link = a['href']
            #   .get('href')
            links.append('https://books.toscrape.com/' + link)
    print(links)

get_Url()


#lien de la page a scrapper
url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'
reponses = requests.get(url)
title_book = []
book_1 = ['Title', 'UCP', 'Price Excl TAX','Price Includ TAX', 'Nombre available', 
          'Review Rating', 'Category', 'Produc description', 'URL']

#récuperer le titre d'un livre 
def get_title ():
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')
        title = soup.find('h1')
        title_book.append(title.get_text())
        print(title_book)

        
#récuperer les informations de chaque livre
#code UPC, price including taxe, price exluding taxe,
# number available,  
def get_info_book():
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')

        for i in soup.findAll('tr'):
            #recuperer le code UPC d'une page
            book = i.find_all('td')

            for td in book:
                if td.get_text() in ['Books', '0', 'Â£0.00']:
                    td.extract()
                else: 
                    print(td.get_text())

# récuperer les category de chaque livre            
def get_category_book():
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')
        category = soup.find('ul', 'breadcrumb')
        li_list = category.find_all('li', limit = 4)
        if len(li_list) >=3:
            print(li_list[2].get_text())


#récuperer le review rating de chaque livre
star_rating = []
def get_star_rating():
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')
        star = soup.findAll('p', 'star-rating')
        if star:
            star_rating = star[0] 
            print(star_rating.get('class')[-1])
 

#récuperer la description de chaque livre
product_description = []
def get_description():
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')
        paragraphe_description = soup.find(id = 'content_inner')
        product_description = paragraphe_description.find_all('p')[3]
        print(product_description.get_text())


#récuperer l'Url de l'image de chaque livre
url_image = []
def get_image_url():
    if reponses.ok:
        soup = BeautifulSoup(reponses.text, 'html.parser')
        image_url = soup.find(class_= 'item active')
        
        image = image_url.find('img')
        link_image = str(image['src'])
        link = link_image[5:]
        print('https://books.toscrape.com/' + link)



get_image_url()

get_Url()


get_info_book()

get_title() 

get_category_book()

get_star_rating()

get_description()




#commencer à créee le fichier csv
# with open('books.csv', 'w', newline='') as csvfile:
#continuer à récuperer les différente page et differente categori