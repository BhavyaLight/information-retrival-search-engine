# Information-retrival-search-engine  

[![Stories in Ready](https://badge.waffle.io/BhavyaLight/information-retrival-search-engine.png?label=ready&title=Ready)](https://waffle.io/BhavyaLight/information-retrival-search-engine) [![Stories in Backlog](https://badge.waffle.io/BhavyaLight/information-retrival-search-engine.png?label=backlog&title=Backlog)](https://waffle.io/BhavyaLight/information-retrival-search-engine)

## Project Development Set-Up

### Requirements
- Install docker
- Git clone this repository into your local disk

Run the following commands:  
```bash
docker build -t bhavya/information_retrival:version1 .
```
```bash
docker run --publish=8001:8000 bhavya/information_retrival:version1
```
Note: The django website will now be available on port 8001 instead of 8000

## To run locally without Docker (Sorry Bhavya) 
- Change information-retrival-search-engine/informationRetrival/frontend/views.py to point to correct directory for local index folder
- Change information-retrival-search-engine/informationRetrival/classification/classify.py to point to local 'model_files' diretory   
- Inside information-retrival-search-engine/informationRetrival directory do  
```bash
$ python manage.py runserver
```
- Open http://localhost:8000 knock yourself out searching and classifying (only, for now :( ) movies


END
