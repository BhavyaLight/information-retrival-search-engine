from django.shortcuts import render
from .forms import SearchForm
from django.http import HttpResponseRedirect
from indexing.MovieDataSearch import Search
from whoosh.qparser import QueryParser
from whoosh import index as i
from whoosh import scoring
from whoosh import highlight
import json

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['search_field']
            query = form.cleaned_data['search_text']
            # TODO: Change Directory here
            ix = i.open_dir('/Users/noopurjain/Desktop/index')
            # TODO: Suggest corrected spelling
            if query is not None and query != u"":
                parser = QueryParser(search_field, schema=ix.schema)
                try:
                    qry = parser.parse(query)
                except:
                    qry = None
                if qry is not None:
                    searcher = ix.searcher()
                    hits = searcher.search(qry)
                    return render(request, 'frontend/index.html', { 'error':False, 'hits': hits, 'form':form})
                # TODO: Display error messages on the page
                else:
                    return render(request, 'frontend/index.html', {'error': True, 'message':"Sorry couldn't parse", 'form':form})
            else:
                return render(request, 'frontend/index.html', {'error': True, 'message':'oops', 'form':form})
    else:
        form = SearchForm()
        return render(request, 'frontend/index.html', {'form': form})

# TODO: Use this function to get more spelling suggestions
def get_more_suggestions(query_string, field_key, corrected_string, s):
    # Stores list of words with spelling error detected
    mistyped_words = []
    # for each word from original query
    for word in query_string.split(" "):
        # if the word id mis-spelt, store it
        if word not in corrected_string:
            mistyped_words.append(word)
    # initialize the corrector
    corrector = s.corrector(field_key)
    # stores mapping of incorrect->list of correct words
    list_of_corrections = dict()
    # Retrieves top 3 closest word based on existing index
    for mistyped_word in mistyped_words:
        list_of_corrections[mistyped_word] = corrector.suggest(mistyped_word, limit=3)
    return list_of_corrections
