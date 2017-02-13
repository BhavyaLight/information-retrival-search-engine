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

END
