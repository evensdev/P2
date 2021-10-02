
# importation du code html de la page d'accueil du site

import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')



#extraction du titre des livres

for text in soup.find_all('a'):
    print(text.get('title'))




#extraction du prix des livres

for price in soup.find_all('p', class_='price_color'):
    print(price.string)



#Sauvegarde des titres dans une liste

liste_titres = [3]

def titre_livre():
    for text in soup.find_all('a'):
        liste_titres.append(str(text.get('title')))


print(liste_titres)

#Sauvegarde des prix dans une liste
