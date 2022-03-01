from .client import get_request_ip


class HeadersToRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_ip = get_request_ip(request)
        return self.get_response(request)
