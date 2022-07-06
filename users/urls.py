from django.urls import path

from .views import EmailLoginView, KakaoLoginView

urlpatterns = [
    path('/email',EmailLoginView.as_view()),
    path('/kakao',KakaoLoginView.as_view())
]
