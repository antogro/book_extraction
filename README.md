# Book_extraction

## Description
L'application Book_scraper permet d'extraire les informations (titre, code UPC, prix TTC et HT, quantité disponible, note et description sur 5, catégorie) d'un livre, d'une catégorie de livres ou de tous les livres du site web.
"Lien du site Books_to_scrape". "[Lien du site Books_to_scrape](https://books.toscrape.com/index.html)"


## Installation

Pour installer le projet, il faut cloner le repository, soit en utilisant la clé SSH, ou en téléchargeant le dossier zipper du repository. 
[lien du repository :](https://github.com/antogro/book_extraction.git)
**Pour chaque ligne de code coller dans l'invité de commande, veuillez cliquer sur entrée.**

### 1 - Git clone (cloner le repository)

Pour cloner le repository il va vous falloir ouvrir l'inviter de commande (CMD), si cette méthode n'est pas fonctionnel,
veuillez suivre l'étape du téléchargement du repository.
Puis Copier/Coller le bout de code suivant dans l'invité de commande, puis taper sur la touche Entrée 

```bash
git clone git@github.com:antogro/book_extraction.git
```

Après clonage du repository, retournez dans votre invité de commande, puis positionnez-vous dans le dossier contenant l'application
    Pour cela, utilisez la commande suivante, puis Entrée :
```bash
cd book_extraction
```

### 1 bis - Téléchargement du repository compressé (zipper)

[lien du repository :](https://github.com/antogro/book_extraction.git)
Télécharger le code grâce au lien du repository, en cliquant sur le bouton **<> Code** tout en haut de la page, puis sur **Download ZIP** ou **Télécharger le ZIP**
Ensuite vous allez devoir extraire le document, ouvrez le dossier puis glisser le fichier dans le dossier selectionné.



## Usage

### Etape 1: Installer Pyhton et créer son environnement virtuel

Il vous faut installer Python 3.9.10 ou plus pour faire fonctionner le programme.  
[Lien pour télécharger la dernière version de python](https://www.python.org/downloads/)
```
Pour créer votre environnement virtuel, il faut vous placer dans l'inviter de commande (CMD) ouvert précédement.
Pour cela utilisé la commance *cd*
```
```cd C:\Users\anton\Bureau\openclassroom\book_extraction``` 
```
utilisez la commande suivante dans votre invité de commande pour créer votre environnement:
```
```bash
python -m venv env

```

Puis Activer votre environnement virtuelle:
```bash
env/scripts/activate
```


### Etape 2: Installer les packages
Les packages permettent un bon fonctionnement de l'application, ne les oubliez pas.
```bash
pip install -r requirements.txt
```

### Etape 3: Lancer l'application
- Enfin, pour lancer l'application,
lancez le programme avec la commande suivante:

```bash
python main.py
```
                        
Voilà votre programme est maintenant opérationnel, vous n'avez plus qu'à suivre les consignes.


## Exemple d'utilisation

Pour lancer l'application, il vous faut taper la commande suivante:

```bash
python main.py
```

Ensuite le programme vous proposera 4 choix : 
- 1 : Ecrivez 1 si vous souhaitez scraper toutes les données de toutes les catégories
- 2 : Ecrivez 2 si vous souhaitez scraper les données d'une catégorie
- 3 : Ecrivez 3 si vous souhaitez scraper les données d'un livre
- 4 : Ecrivez 4 si vous souhaitez Quittez l'application d'extraction de livre.
```
Pour mon exemple, je vais choisir le numéro '3' l'application vous confirmera votre choix,
puis vous proposera un lien vous permettant de sélectionner l'url du livre voulu **https://books.toscrape.com/**.
Copier et coller l'url dans l'invité de commande, 
```
Dans le fichier book_extraction puis data, vous allez pouvoir récupérer les informations extraites.

## Auteurs

- [@antogro](https://www.github.com/antogro)
