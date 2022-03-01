from ipware import get_client_ip


def get_request_ip(request):
    remote_addr, _ = get_client_ip(
        request,
        request_header_order=[
            "X_FORWARDED_FOR",
            "HTTP_X_FORWARDED_FOR",
            "HTTP_X_REAL_IP",
        ],
    )
    return remote_addr
