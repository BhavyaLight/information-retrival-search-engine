from django.shortcuts import render
from .forms import SearchForm, ClassifyForm
from whoosh.qparser import QueryParser
from whoosh import index as i
from whoosh import scoring
import whoosh.query as QRY
import time
from datetime import datetime
from classification.classify import Classification

CLASSIFICATION_PATH = '/Users/bhavyachandra/Desktop/model_files_new_with_voting_with_weights/'

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['search_field']
            query = form.cleaned_data['search_text']
            rating = request.POST.get("rating")
            year = request.POST.get("year")
            query = query.replace('+', ' AND ').replace('-', ' NOT ')
            filter_q = None
            print (rating)
            print (year)
            # TODO: Change Directory here
            ix = i.open_dir('/Users/bhavyachandra/Desktop/Index')
            start_time = time.time()
            if query is not None and query != u"":
                parser = QueryParser(search_field, schema=ix.schema)
                if year!=None and rating!=None:
                    date_q = QRY.DateRange("release_date", datetime.strptime(year.split(",")[0], "%Y"),\
                                            datetime.strptime(year.split(",")[1], "%Y"))
                    rating_q = QRY.NumericRange("vote_average",0, int(rating))
                    filter_q = QRY.Require(date_q, rating_q)
                else:
                    year = "1970,2017"
                    rating = 5
                try:
                    qry = parser.parse(query)
                except:
                    qry = None
                    return render(request, 'frontend/index.html', {'error': True, 'message':"Query is null!", 'form':form})
                if qry is not None:
                    searcher = ix.searcher(weighting=scoring.TF_IDF())
                    corrected = searcher.correct_query(qry, query)
                    if corrected.query != qry:
                        return render(request, 'frontend/index.html', {'field': search_field, 'correction': True, 'suggested': corrected.string, 'form': form})
                    hits = searcher.search(qry,filter=filter_q,limit=None)
                    elapsed_time = time.time() - start_time
                    elapsed_time = "{0:.3f}".format(elapsed_time)
                    return render(request, 'frontend/index.html', {'error': False, 'hits': hits, 'form':form, 'elapsed': elapsed_time, 'number': len(hits), 'year': year, 'rating': rating})
                else:
                    return render(request, 'frontend/index.html', {'error': True, 'message':"Sorry couldn't parse", 'form':form})
            else:
                return render(request, 'frontend/index.html', {'error': True, 'message':'oops', 'form':form})
    else:
        form = SearchForm()
        return render(request, 'frontend/index.html', {'form': form})

def classification(request):
    if request.method == "POST":
        form = ClassifyForm(request.POST)
        if form.is_valid():
            plot = form.cleaned_data['classify_plot']
            genre, time = Classification(CLASSIFICATION_PATH).Classify_Text(plot)
            return render(request, 'frontend/classify.html', {'form': form, 'genre': genre[0], 'time': time})
        else:
            return render(request, 'frontend/classify.html', {'form': form})
    else:
        form = ClassifyForm()
        return render(request, 'frontend/classify.html', {'form': form})
