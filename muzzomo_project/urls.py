from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

import service.urls as service_urls
import user.urls as user_urls
import job.urls as job_urls

from muzzomo_project import settings


urlpatterns = [
    path('service/', include(service_urls)),
    path('user/', include(user_urls)),
    path('job/', include(job_urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
