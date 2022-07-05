from django.urls import path
from hotels.views import SearchView

urlpatterns = [
    path('/search',SearchView.as_view())
]