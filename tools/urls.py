from django.conf.urls import url

from .views import error404, error500

app_name = "tools"

urlpatterns = [
    url(r"error404", error404, name="error404"),
    url(r"error500", error500, name="error500"),
]
