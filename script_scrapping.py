import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


"""
Pour effectuer le scrapping des données sur le site books.toscrape.com, 
Nous créerons 4 fonctions : get_links, get_book, get_databooks, get_image.
Elles permettront de créer un script qui récupérera par itérations les données des livres.
et les exporter dans un fichier .csv par catégories.
"""



url = 'https://books.toscrape.com/'



#Fonction permettant de récupérer l'url de toutes les catégories
def get_links(url):
    response = requests.get(url)
    link_categories = []
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = soup.find_all('a')[3:53]


    for a in categories:
        link = a.attrs['href']
        link_categories.append(url + link)

        print('OK: ' + url + link)

    return (link_categories)



#Fonction permettant de récupérer les liens de pages de chaque livres en gérant la pagination
def get_books(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_h3 = soup.find_all('h3')
    list_books = []

    for h3 in list_h3:
        new_url = h3.find('a').attrs['href']
        separated = new_url.split('/')
        prefixe = 'https://books.toscrape.com/catalogue/'

        list_books.append(prefixe + separated[-2] + '/' + separated[-1])


    for i in range(1,20):

        extension = 'page-' + str(i) + '.html'
        url_page = url.replace('index.html', extension)
        response = requests.get(url_page)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            list_h3 = soup.find_all('h3')
            prefixe = 'https://books.toscrape.com/catalogue/'

            for h3 in list_h3:
                new_url = h3.find('a').attrs['href']
                separated = new_url.split('/')

                list_books.append(prefixe + separated[-2] + '/' + separated[-1])
        else:
            return list_books



#Fonction permettant de récupérer les données d'un livre
def get_databooks(book):
    response = requests.get(book)
    soup = BeautifulSoup(response.content, 'html.parser')
    print('OK '+ str(response.status_code))


    if response.ok:


        elements = soup.find_all({'td'})
        image = soup.find('img').attrs['src']
        prefixe = 'http://books.toscrape.com/'


        keys = {}

        keys['product_page_url'] = book

        keys['universal_product_code'] = elements[0].text

        title = soup.find('h1').text
        keys['title'] = title.replace('/', ' ')


        price_tax = elements[2].text
        keys['price_including_tax'] = price_tax.replace('Â', '')

        price_exc = elements[3].text
        keys['price_excluding_tax'] = price_exc.replace('Â', '')

        keys['number_available'] = elements[5].text

        description = soup.find_all('p')[3].text
        keys['product_description'] = description.replace(';', '')


        categorie = soup.find_all('a')[3]
        keys['category'] = categorie.text


        review = str(soup.find_all('p')[2])
        separated = review.split('"')
        keys['review_rating'] = separated[1]


        keys['image_url'] = prefixe + image



        return keys



#fonction permettant de télécharger et nommer l'image d'un livre
def  get_image(url_image, image_name):
    response = requests.get(url_image)

    with open("images/"+image_name+".jpg", "wb") as file:
        file.write(response.content)

    return




"""
Le script ci-dessous utilisera les fonctions et les boucles permettant de récupérer toutes les
données des livres sur le site. Elles seront ensuite exportées en fichier .csv par catégorie,
et les image seront téléchargées dans le dossier 'images'
"""



categories = get_links(url)


for categorie in categories:
    books = get_books(categorie)
    print(books)
    separated = categorie.split('/')
    category_name = str(separated[-2])+'.csv'



    with open(category_name, 'a', encoding='utf_8-sig') as file:
        file.write('product_page_url;' +
                   'universal_product_code;' +
                   'title;' +
                   'price_including_tax;' +
                   'price_excluding_tax;' +
                   'number_available;' +
                   'product_description;' +
                   'category;' +
                   'review_rating;' +
                   'image_url'+ "\n")
        for book in books:
            databook = get_databooks(book)
            get_image(databook['image_url'], databook['title'])
            file.write(databook['product_page_url'] + ";" +
                       databook['universal_product_code'] + ";" +
                       databook['title'] + ";" +
                       databook['price_including_tax'] + ";" +
                       databook['price_excluding_tax'] + ";" +
                       databook['number_available'] + ";" +
                       databook['product_description'] + ";" +
                       databook['category'] + ";" +
                       databook['review_rating'] + ";" +
                       databook['image_url'] + "\n")
    file.close()
