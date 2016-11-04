from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from green_country import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls', namespace='core'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
