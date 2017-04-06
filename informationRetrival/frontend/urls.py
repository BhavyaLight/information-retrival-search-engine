from django.conf.urls import url
from . import views

app_name = 'frontend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^/page=', views.paginate),
    url(r'^classify$', views.classify, name='classify')
]
