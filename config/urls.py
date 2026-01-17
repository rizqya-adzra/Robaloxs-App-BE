from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('apps.users.urls', 'users-api'))),
    path('api/', include(('apps.roblox_cores.urls', 'roblox-cores-api'))),
    path('api/', include(('apps.catalogues.urls', 'catalogues-api'))),
    path('api/', include(('apps.transactions.urls', 'transactions-api'))),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
