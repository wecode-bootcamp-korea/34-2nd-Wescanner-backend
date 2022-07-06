from django.urls import path

from .views import EmailLoginView

urlpatterns = [
    path('/email',EmailLoginView.as_view())
]

