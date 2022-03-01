from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("config.urls_api", namespace="api")),
]

if settings.DEBUG:
    from django.views.static import serve

    import debug_toolbar
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework.permissions import AllowAny

    schema_view = get_schema_view(
        openapi.Info(
            title="Authenticator API",
            default_version="v1",
        ),
        public=True,
        permission_classes=(AllowAny,),
    )

    urlpatterns += [path("__debug__", include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
    urlpatterns += [
        url(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        url(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        url(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

handler404 = "tools.views.error404"
handler500 = "tools.views.error500"
