from django.conf.urls import url
from core.views import IndexView, RawView, CallBackView, EcoView, EcoFormView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^page/(?P<slug>\w*)', RawView.as_view(), name='raw'),
    url(r'^callback/$', CallBackView.as_view(), name='callback'),
    url(r'^eco/$', EcoView.as_view(), name='eco'),
    url(r'^ecoform', EcoFormView.as_view(), name='eco-form')
]
