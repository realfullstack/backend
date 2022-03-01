from http import HTTPStatus

from django.shortcuts import render


def error404(request, *args, **argv):
    return render(
        request,
        "tools/error404.html",
        status=HTTPStatus.NOT_FOUND,
    )


def error500(request, *args, **argv):
    return render(
        request,
        "tools/error500.html",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
