from django import forms
FIELD_CHOICES = [('title','Movie Title'),
                 ('overview', 'Overview'),
                 ('taglines', 'Taglines'),
                 ('genres', 'Genres')]
class SearchForm(forms.Form):
    search_field = forms.ChoiceField(choices=FIELD_CHOICES)
    search_text = forms.CharField(label='Search Movie')

class ClassifyForm(forms.Form):
    classify_plot = forms.CharField(widget=forms.Textarea)
