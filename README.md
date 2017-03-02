# Information Retrival Search Engine

## Overview

The information retrieval search engine built by our team is based on Movies, the data for which has been obtained by the TMDB api. Our motivation for picking the above in order to build an information retrieval system is influenced by two main factors: 
- **Real world application**  
A typical Movie data consists of title, plot description, poster, genre, date, language, runtime, actors, review etc. that provides realistic paramteres for the construction of a typical search engine in real world. As a result, although set on Movie data, the search engine helps us draw parallels to many other forms of real world data.
- **Opportunity to learn**  
The Movie data consists of numbers, dates, text, images, urls i.e. a great amalgamation of datafor trying different techniques taught in the information retreival course. Thus, we felt the dataset provided enough diversity to learn something new.


## Crawling the data

1. How you crawled the corpus (e.g., source, keywords, API, library) and stored them (e.g., whether a record corresponds to a file or a line, meta information like publication date, author name, record ID)  
The Movie Db (TmDB) api was used to extract the corpus and relevant information about the movies. The crawled and extracted corpus was stored in the formed of json-like text files. A single text file consists only of a single movie record with a detailed plot information. Ceratin records lacked plot information. We ignored such records during crawling as they were insignificant to the kind of information retreival system required. Each unique text file is saved with a unique id from 1 to greater than 20,000. The unique identifier for each record is the 'imdb_id' as well as the text file number in our case. We also store the following meta-data for each record:
 - **Title**  
   
 - **Overview**
 - **tagline** 
 - **title**
 - **runtime**
 - **poster_path**
 - **genres**
 - **production_companies**
 - **release_date**
 - **imdb_id**
 - **popularity**
 - **revenue**
 - **vote_average**
 - **adult**

2. What kind of information users might like to retrieve from your crawled corpus (i.e., applications), with example queries  
Most frequenty users might want to search for a particular movie by its title and find out it's information such as rating, popularity, plot, genre by searching for the main title. The users may also like to recollect the title of some movie by typing in the plot or tagline. Thus, we would like to support both kinds of searches. Furthermore, users might want to search for a list of movies by one or more movie genre and decide to watch the most popular movie in that segment.  

We aim to archieve the basic Query functionalities, the implementation of advanced query features is subject to our progress.  

| Query type        | Example of basic Query         | Example of advanced Query                                                                                                  | Expected Result                                                 | Details                                                                                                                                                        |
|-------------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Search by title   | fear of clowns (exact title)   | Frea of Clowns (Spell check)                                                                                               | Movies with similar title                                       | The result should be specific, not more than 3-5 films unless the title is a series                                                                            |
| Search by tagline | competitive gymnastics         | competition of gymnasts (Spell check)                                                                                      | Movie with similar tagline                                      | The result should be specific, not more than 3-5 films unless the title is a series                                                                            |
| Search by plot    | murderous clowns in circus     |                                                                                                                            | Movies with similar plot overview                               | The result can be little less specific and not limited to 3-5 films                                                                                            |
| Search by genre   | crime and thriller movies      | movies with suspense and murder (deciding which genre the user is looking for based on classification from previous data)  | Movies under the crime and thriller genre, sorted by popularity | A good example for boolean indexing by Genre                                                                                                                   |
| Search by review  | > 4.7 popularity, < 6.7 rating | Average popularity movies(with ambiguous popularity ratings)                                                               | Movies who are popular than 4.7 rating, less than 6.7 rating    | Try to convert user text search for a range of ratings, and display results likewise. The simple case could be to use filter, while the advanced would be NLP. |

3. The numbers of records, words, and types (i.e., unique words) in the corpus


### Syntax for MD

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/BhavyaLight/information-retrival-search-engine/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
