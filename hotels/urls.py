from django.urls import path
from hotels.views import SearchView, HotelListView

urlpatterns = [
    path('/search',SearchView.as_view()),
    path('',HotelListView.as_view()),
]