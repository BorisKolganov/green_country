from django.conf.urls import url
from core.views import IndexView, RawView, CallBackView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^page/(?P<slug>\w*)', RawView.as_view(), name='raw'),
    url(r'^callback/$', CallBackView.as_view(), name='callback')
]
