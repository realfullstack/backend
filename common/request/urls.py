from urllib.parse import parse_qsl, urlparse, urlunparse

from django.utils.http import urlencode


def get_url_domain(url):
    return urlparse(url).netloc


def add_url_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return urlunparse(url_parts)
