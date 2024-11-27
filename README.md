# IFTS-18-POO-Proyecto-Solucion

Sistema de gestión de obras urbanas con manejo de POO, importación de datasets desde un archivo csv y persistencia de objetos con ORM Peewee en una base de datos SQLite.

## Integrantes

- Brizuela Ludmila
- Flores Diego
- Laguna Martin
- Marighetti Mercedes
- Rodriguez Lola

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

## Funcionalidades del Módulo `interfaztk.py`

El módulo `interfaztk.py` proporciona una interfaz gráfica de usuario (GUI) para gestionar las obras públicas de la Ciudad de Buenos Aires. A continuación se describen las principales funcionalidades a las que puede acceder el cliente:

### Tabla de Obras

**Visualización de Obras:** La interfaz muestra una tabla con las obras extraídas de la base de datos `obras_urbanas.db`. Las columnas visibles en la tabla son:
- id
- nombre
- barrio
- comuna

**Selección de Obras:** El cliente puede seleccionar una obra de la tabla haciendo clic en la fila correspondiente. Esta acción permite acceder a más detalles sobre la obra seleccionada.

### Ver Detalles de una Obra

**Detalles de la Obra:** Al seleccionar una obra y hacer clic en el botón "Ver Detalles", se abre una ventana aparte que muestra información detallada sobre la obra seleccionada. La información presentada incluye:
- Título de la obra
- Descripción
- Barrio
- Comuna
- Área responsable
- Monto del contrato
- Empresa
- Financiación
- Si es destacada

Estas funcionalidades permiten al cliente gestionar y visualizar de manera eficiente la información relacionada con las obras públicas de la Ciudad de Buenos Aires.