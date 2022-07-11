from django.urls import path

from .views import EmailLoginView, KakaoLoginView, ReviewView

urlpatterns = [
    path('/email',EmailLoginView.as_view()),
    path('/kakao',KakaoLoginView.as_view()),
    path('/review', ReviewView.as_view())
]
