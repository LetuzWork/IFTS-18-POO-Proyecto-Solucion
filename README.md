# IFTS-18-POO-Proyecto-Solucion

Sistema de gestión de obras urbanas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

## Setup

Se añadio pipfile al proyecto para simplificar el inicializado de este, debajo las instrucciones

1. Instalar pipenv: `pip install pipenv`
2. Instalar las Bibliotecas del proyecto `pipenv install`
3. Prender Ambiente Virtual `pipenv shell`

luego de ese setup ya deberia estar funcionando y con las librerias encapsuladas para este proyecto

## Get Started

Para comenzar a interactuar con el sistema de gestion de obras basta con ejecutar`

`python gestionar_obras`

En el cual se va a:

1. Cargar la información proveniente de `observatorio-de-obras-urbanas.csv`
2. Permitirte crear tantas nuevas obras y llevarlas a fin como desees
3. Permitirte obtener indicadores de tu base de obras urbanas
