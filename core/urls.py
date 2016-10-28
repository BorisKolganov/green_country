from django.conf.urls import url
from core.views import IndexView, PageView, CallBackView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^page/(?P<slug>[\w\-]+)', PageView.as_view(), name='page'),
    url(r'^callback/$', CallBackView.as_view(), name='callback')
]
