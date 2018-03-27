# manage url in application level folder instead or project level folder.
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateView, DetailsView

urlpatterns = {
    url('^$', CreateView.as_view()),                   # request http://127.0.0.1:8000/
    url('^(?P<pk>[0-9]+)/$', DetailsView.as_view()),  # request http://127.0.0.1:8000/1/
}

urlpatterns = format_suffix_patterns(urlpatterns)
