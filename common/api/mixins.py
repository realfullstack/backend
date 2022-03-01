from django.db import transaction

from rest_framework import status
from rest_framework.response import Response


class AtomicMixin(object):
    """
    Ensures we rollback db transactions on exceptions.
    Idea from https://github.com/tomchristie/django-rest-framework/pull/1204
    """

    @transaction.atomic()
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def handle_exception(self, *args, **kwargs):
        response = super().handle_exception(*args, **kwargs)

        if getattr(response, "exception"):
            # We've suppressed the exception but still need to rollback any transaction.
            transaction.set_rollback(True)

        return response


class PostViewMixin(object):
    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if hasattr(self, "execute") and callable(getattr(self, "execute")):
            return self.execute(serializer)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetViewMixin(object):
    def get(self, request, **kwargs):
        if hasattr(self, "execute") and callable(getattr(self, "execute")):
            return self.execute(request)
        else:
            raise Exception("Improperly implemented")
