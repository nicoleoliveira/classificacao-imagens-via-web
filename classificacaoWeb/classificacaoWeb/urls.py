from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from interfaceWeb.views import ImagemUploadViewSet, AmostrasViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^imagemUpload/', ImagemUploadViewSet.as_view()),   
    url(r'^amostras/', AmostrasViewSet.as_view()),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)