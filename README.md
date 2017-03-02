# Information Retrival Search Engine

## Overview

The information retrieval search engine built by our team is based on Movies, the data for which has been obtained by the TMDB api. Our motivation for picking the above in order to build an information retrieval system is influenced by two main factors: 
- **Real world application**  
A typical Movie data consists of title, plot description, poster, genre, date, language, runtime, actors, review etc. that provides realistic paramteres for the construction of a typical search engine in real world. As a result, although set on Movie data, the search engine helps us draw parallels to many other forms of real world data.
- **Opportunity to learn**  
The Movie data consists of numbers, dates, text, images, urls i.e. a great amalgamation of datafor trying different techniques taught in the information retreival course. Thus, we felt the dataset provided enough diversity to learn something new.


### Crawling the data

1. How you crawled the corpus (e.g., source, keywords, API, library) and stored them (e.g., whether a record corresponds to a file or a line, meta information like publication date, author name, record ID)

2. What kind of information users might like to retrieve from your crawled corpus (i.e., applications), with example queries  
Most frequenty users might want to search for a particular movie by its title and find out it's information such as rating, popularity, plot, genre by searching for the main title. The users may also like to recollect the title of some movie by typing in the plot or tagline. Thus, we would like to support both kinds of searches. Furthermore, users might want to search for a list of movies by one or more movie genre and decide to watch the most popular movie in that segment.
 - **Search by title**  
 _Standard Search Query_: Fear of Clowns  (exact title)    
 _Advanced search query (with support for spellcheck):_   
 Clown fear  
 Frea of Clowns  
 Fear the clown  
 _**Expected Result**_: Fear of Clowns  
 - **Search by tagline**  
 _Standard Search Query_: competitive gymnastics   
 _**Expected Result**_: Stick It  
 - **Search by plot**  
 _Standard Search Query_: murderous clowns   
 _**Expected Result**_: Fear of Clowns   
 - **Search by genre**  
 _Standard Search Query_: Crime and thriller movies  
 _**Expected Result**_: Crime and thriller movies, sorted by popularity  
 - **Search by review** (Advanced Feature)  
 _Standard Search Query_:  > 4.7 popularity, < 6.7 rating  
 _**Expected Result**_: Movies who are popular than 4.7 rating, less than 6.7 rating  
 _Advanced search query (with ambiguous popularity ratings):_ e.g. Average popularity movies  

| Query type        | Example of basic Query       | Example of advanced Query    | Expected Result           | Details                                                                             |
|-------------------|------------------------------|------------------------------|---------------------------|-------------------------------------------------------------------------------------|
| Search by title   | Fear of Clowns (exact title) | Frea of Clowns (Spell check) | Movies with similar title | The result should be specific, not more than 3-5 films unless the title is a series |
| Search by tagline |                              |                              |                           |                                                                                     |
| Search by plot    |                              |                              |                           |                                                                                     |

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
