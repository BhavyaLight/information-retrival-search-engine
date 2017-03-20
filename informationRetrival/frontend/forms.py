from django import forms
FIELD_CHOICES = [('title','Movie Title'),
                 ('overview', 'Overview'),
                 ('taglines', 'Taglines'),
                 ('genres', 'Genres'),
                 ('review', 'Review')]
class SearchForm(forms.Form):
    search_field = forms.ChoiceField(choices=FIELD_CHOICES)
    search_text = forms.CharField(label = 'Search Movie')
