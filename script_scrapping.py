import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'


# Je crée un fonction qui récupère tous les liens de la partie catégorie
def get_links(url):
    response = requests.get(url)
    link_categories = []
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find_all('a')[3:53]

    for a in categories:
        link = a.attrs['href']
        link_categories.append(url + link)

    return (link_categories)


# je crée une fonction qui récupère tous les livres des pages de catégories + gestion de la pagination
def get_books(url):

    list_books = []
    for i in range(1):
        new_url = url.replace('index.html', 'page-' + str(i) + '.html')
        response = requests.get(new_url)
        print(response)
        if response.ok:
            print('Page: ' + str(i))
            soup = BeautifulSoup(response.text, 'html.parser')
            list_h3 = soup.find_all('h3')

            for h3 in list_h3:
                list_books.append(url + h3.find('a').attrs['href'])

    return(list_books)





def get_databooks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # je définis deux listes que je vais concatener par la suite pour créer un dictionnaire
    # Je crée premièrement la liste [key] pour définir toutes les clés correspondantes aux données de la consigne
    if response.ok:
        keys = ['product_page_url',
                'universal_product_code',
                'title',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url']

        # Je crée la liste vide temporaire destinée à recevoir toutes les données scrappée sur la page
        v_temp = []

        # J'ajoute l'url de la page en 1ère valeur dans la liste temporaire
        v_temp.append(url)

        # j'ajoute les autres valeurs dans la liste temporaire grâce à une boucle qui passe sur tout les 'td' de la page
        elements = soup.find_all({'td'})

        for element in elements:
            v_temp.append(element.text)

        # je crée ma vrai liste "values" destinée à recevoir les valeurs de la liste temporaire qui est nettoyée
        values = []

        for value in v_temp:
            new_value = value.replace('Â', '')
            values.append(new_value)

        # Scrapper le titre du livre
        list_h1 = soup.find('h1')
        values.insert(3, list_h1.text)

        # scrapper la description du livre
        description = soup.find_all('p')[3]
        values.insert(8, description.text)

        # Scrapper Categorie du livre
        categorie = soup.find_all('a')[3]
        values.insert(9, categorie.text)

        # Scrapper image de la page
        image = soup.find('img').attrs['src']
        prefixe = 'http://books.toscrape.com/'
        values.append(prefixe + image)

        # effacer les valeurs non-désirées
        values.pop(2)
        values.pop(5)

        return (values)


    # Contatener les listes : valeurs et clées, pour faire un dictionnaire
    #dict_book = dict(zip(keys, values))



"""# Exporter les données en fichier CSV
    with open('test.csv', 'w') as test:
        for key in keys:
            test.write(key +';')
        test.write('\n')
        for value in values:
            test.write(value + ';')

"""



#print(get_databooks('http://books.toscrape.com/catalogue/the-mysterious-affair-at-styles-hercule-poirot-1_452/index.html'))

# dict to Dataframe




def create_csv(liste):
    with open('graal.csv', 'w') as test:
        for contenu in liste:
            test.write(contenu + ';')
        test.write('\n')




#print(get_books(url))


lien_book = get_books(url)
for lien in lien_book:
    infos_livre = get_databooks(lien)




"""
with open('graal.csv', 'w') as test:
    for info in infos_livres:
        test.write(info + ';')
    test.write('\n')

"""



"""
ma_liste = {'http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html', 'a22124811bfa8350',
            "It's Only the Himalayas",
            '£45.17', '£45.17', 'In stock (19 available)', 'â\x80\x9cWherever you go, whatever you do, just . . . donâ\x80\x99t do anything stupid.â\x80\x9d â\x80\x94My MotherDuring her yearlong adventure backpacking from South Africa to Singapore, S. Bedford definitely did a few things her mother might classify as "stupid." She swam with great white sharks in South Africa, ran from lions in Zimbabwe, climbed a Himalayan mountain without training in Nepal, and wa â\x80\x9cWherever you go, whatever you do, just . . . donâ\x80\x99t do anything stupid.â\x80\x9d â\x80\x94My MotherDuring her yearlong adventure backpacking from South Africa to Singapore, S. Bedford definitely did a few things her mother might classify as "stupid." She swam with great white sharks in South Africa, ran from lions in Zimbabwe, climbed a Himalayan mountain without training in Nepal, and watched as her friend was attacked by a monkey in Indonesia.But interspersed in those slightly more crazy moments, Sue Bedfored and her friend "Sara the Stoic" experienced the sights, sounds, life, and culture of fifteen countries. Joined along the way by a few friends and their aging fathers here and there, Sue and Sara experience the trip of a lifetime. They fall in love with the world, cultivate an appreciation for home, and discover who, or what, they want to become.It\'s Only the Himalayas is the incredibly funny, sometimes outlandish, always entertaining confession of a young backpacker that will inspire you to take your own adventure. ...more',
            'Travel', '0', 'http://books.toscrape.com/../../media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg'}

print(create_csv(ma_liste))

"""






#print(create_csv('http://books.toscrape.com/catalogue/the-mysterious-affair-at-styles-hercule-poirot-1_452/index.html'))








# Ceci est mon main script : avant de l'activer je dois créer toutes mes fonctions quand elles seront prêtes, je pourrai m'en servir






"""
categories = get_links(url)

for categorie in categories:
    books = get_books(categorie)
    file = create_csv(categorie)
    
"""













