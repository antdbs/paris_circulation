# Bienvenue dans le TP des villes connectées 🤙

## Prérequis

- Python
- Docker
- SQL


## Installation

Pour installer les différents TP je vous invite à executer une des commandes adéquate dans un de vos répertoires en fonction du TP que vous souhaitez executer :  

- TP 1 : ```git clone -b importer https://github.com/antdbs/paris_circulation.git```
    - [x] BDD postgresql
    - [x] SGBD pgadmin
    - [x] IMPORTER python main.py



## Ensuite vous pouvez suivre les étapes suivantes

### 1. Créer et completer un fichier .env à la racine du projet

Alimenté le avec les variables suivante et vos valeurs personnelles

```
POSTGRES_USER=votre_nom_utilisateur
POSTGRES_PASSWORD=votre_mdp_utilisateur
POSTGRES_DB=le_nom_de_votre_bdd


PGADMIN_DEFAULT_EMAIL=votre@mail.com
PGADMIN_DEFAULT_PASSWORD=votre_mdp_utilisateur
PGADMIN_LISTEN_PORT=80

# Garder les suivantes par défaut
DATABASE_DIALECT=postgresql
DATABASE_HOST=database
DATABASE_PORT=5432
```

### 2. Lancer la commande suivante dans un terminal

``` docker-compose up -d --build ```