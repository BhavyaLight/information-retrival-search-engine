import os
import ast
from MovieData import MovieData
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME, NUMERIC, BOOLEAN
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from whoosh import index, query
from whoosh import scoring
import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")

BASE_PATH="/Users/bhavyachandra/Desktop/trial/"
FILEPATH="/Users/bhavyachandra/Desktop/Index_notstemmed"
# Schema for Movie data
# Stored= True corresponds to all items that require to be returned with the search result
# schema = Schema(overview=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
#                 tagline=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
#                 title=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
#                 production_companies=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
#                 genres=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
#                 runtime=STORED,
#                 poster_path=STORED,
#                 imdb_id=ID(stored=True),
#                 popularity=NUMERIC(float,bits=64, stored=True),
#                 revenue=NUMERIC(float,bits=64, stored=True),
#                 vote_average=NUMERIC(float,bits=64, stored=True),
#                 adult=BOOLEAN(stored=True),
#                 release_date=DATETIME(stored=True)
#                 )

# # instantiate index
# if not os.path.exists(FILEPATH):
#     os.mkdir(FILEPATH)
# ix = index.create_in(FILEPATH, schema)
#
# #open index writer
ix = index.open_dir(FILEPATH)
# writer = ix.writer()
#
# count1=10
# for i in range(1, count1):
#     f21=MovieData(BASE_PATH+str(i)+'.txt')
#     print (i)
#     prod=[]
#     # print (f2.get("production_companies"))
#     for x in f21.get("production_companies"):
#         prod.append(x['name'])
#     genres=[]
#     for x in f21.get("genres"):
#         genres.append(x['name'])
#
#     prodstring=''
#     for x in prod:
#         prodstring=prodstring+x+' '
#     print (prodstring)
#     genrestring=''
#     for x in genres:
#         genrestring=genrestring+x+' '
#     print (genrestring)
#     rdate=f21.get("release_date")
#     print (rdate)
#     if rdate=='':
#         rdate=u'2100-10-10'
#     f2=dict()
#     f2['overview']=f21.get('overview')
#     f2['tagline']=f21.get('tagline')
#     f2['title']=f21.get('title')
#     f2['runtime']=f21.get('runtime')
#     f2['poster_path']=f21.get('poster_path')
#     f2['imdb_id']=f21.get('imdb_id')
#     f2['popularity']=f21.get('popularity')
#     f2['revenue']=f21.get('revenue')
#     f2['vote_average']=f21.get('vote_average')
#     f2['adult']=f21.get('adult')
#
#
#
#     print ("##################################################################################")
#     writer.add_document(overview=unicode(f2['overview']), tagline=unicode(f2['tagline']),title=unicode(f2['title']), production_company=unicode(prodstring), \
#                     genre=unicode(genrestring),runtime=unicode(f2['runtime']), poster=unicode(f2['poster_path']),IMDB_id=unicode(f2['imdb_id']),Popularity=unicode(f2['popularity']),\
#                     Revenue=unicode(f2['revenue']), Vote_Avg=unicode(f2['vote_average']), Adult=unicode(f2['adult']), Release_Date=unicode(rdate))
#
# #commit writer
# writer.commit()
# print("done ##################################################################################")

qstring="crime"
qp = QueryParser("genres", schema=ix.schema, termclass=query.Variations)
q = qp.parse(qstring)
mistyped_words = []

start = time.time()
with ix.searcher(weighting=scoring.TF_IDF()) as s:
    corrected = s.correct_query(q, qstring)
    if corrected.query != q:
        print("Did you mean:", corrected.string)
    for word in qstring.split(" "):
        if word not in corrected.string:
            mistyped_words.append(word)
    print (mistyped_words)
    corrector = s.corrector("genres")
    for mistyped_word in mistyped_words:
        lis=corrector.suggest(mistyped_word, limit=3)
        print lis
        q = qp.parse(corrected.string)
    results = s.search(q)
    print (len(results))
    print (list(results))
    counter = 0
    for hit in results:
        print hit['title']
        counter += 1
        if counter == 10:
            break
    # print ((list(s.lexicon("overview"))))
    # print (len(list(s.lexicon("title"))))
    # print (len(list(s.lexicon("tagline"))))
    # print (len(list(s.lexicon("production_companies"))))
    # print (len(list(s.lexicon("genres"))))
end = time.time()
print ("Total time:"+str((end-start)*1000))

