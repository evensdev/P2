import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'


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



def get_databooks(book):
    response = requests.get(book)
    soup = BeautifulSoup(response.content, 'html.parser')
    print('lien de livre '+ str(response.status_code))


    if response.ok:


        elements = soup.find_all({'td'})
        image = soup.find('img').attrs['src']
        prefixe = 'http://books.toscrape.com/'
        #  class="star-rating Four" récupérer le review_rating sur la page


        keys = {}

        keys['product_page_url'] = book

        keys['universal_product_code'] = elements[0].text

        keys['title'] = soup.find('h1').text


        price_tax = elements[2].text
        keys['price_including_tax'] = price_tax.replace('Â', '')

        price_exc = elements[3].text
        keys['price_excluding_tax'] = price_exc.replace('Â', '')

        keys['number_available'] = elements[5].text

        keys['product_description'] = soup.find_all('p')[3].text


        categorie = soup.find_all('a')[3]
        keys['category'] = categorie.text


        review = elements[-1]
        keys['review_rating'] = review.text


        keys['image_url'] = prefixe + image


        return keys




def  get_image(url_image, image_name):
    response = requests.get(url_image)

    with open("images/"+image_name+".jpg", "wb") as file:
        file.write(response.content)

    print("coucou")

    return




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





