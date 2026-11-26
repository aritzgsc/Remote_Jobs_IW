from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from App_Remote_Jobs.views.media import servir_avatar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("App_Remote_Jobs.urls")),
]

# En desarrollo se usa la ruta habitual de Django; en Render solo se sirven avatares.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.RENDER:
    urlpatterns += [
        re_path(
            r"^media/(?P<ruta>avatares/[0-9]{4}/[0-9]{2}/[^/\\]+\.(?i:jpg|jpeg|png|webp))$",
            servir_avatar,
            name="avatar_media",
        ),
    ]
