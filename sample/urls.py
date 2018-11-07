from django.conf.urls import url
from .views import LoginTest

urlpatterns = [
    url(r'login-test/$', LoginTest.as_view(), name='login-test'),
]