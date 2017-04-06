from django.shortcuts import render
from .forms import SearchForm, ClassifyForm
from django.http import HttpResponseRedirect
from indexing.MovieDataSearch import Search
from whoosh.qparser import QueryParser
from whoosh import index as i
from whoosh import scoring
from whoosh import highlight
from paginate_whoosh import WhooshPage
import json
import time

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['search_field']
            query = form.cleaned_data['search_text']
            query = query.replace('+', ' AND ').replace('-', ' NOT ')
            # TODO: Change Directory here
            ix = i.open_dir('/Users/noopurjain/Desktop/index')
            start_time = time.time()
            if query is not None and query != u"":
                parser = QueryParser(search_field, schema=ix.schema)
                try:
                    qry = parser.parse(query)
                except:
                    qry = None
                if qry is not None:
                    searcher = ix.searcher(weighting=scoring.TF_IDF())
                    corrected = searcher.correct_query(qry, query)
                    if corrected.query != qry:
                        return render(request, 'frontend/index.html', {'field': search_field, 'correction': True, 'suggested': corrected.string, 'form': form})
                    pages = WhooshPage(searcher.search(qry, limit=None), page=1, items_per_page=5)
                    print pages
                    for page in pages:
                        print page
                    hits = searcher.search(qry)
                    elapsed_time = time.time() - start_time
                    elapsed_time = "{0:.3f}".format(elapsed_time)
                    return render(request, 'frontend/index.html', { 'error': False, 'hits': hits, 'form':form, 'elapsed': elapsed_time, 'number': len(hits)})
                else:
                    return render(request, 'frontend/index.html', {'error': True, 'message':"Sorry couldn't parse", 'form':form})
            else:
                return render(request, 'frontend/index.html', {'error': True, 'message':'oops', 'form':form})
    else:
        form = SearchForm()
        return render(request, 'frontend/index.html', {'form': form})

def classify(request):
    form = ClassifyForm()
    return render(request, 'frontend/classify.html', {'form': form})
