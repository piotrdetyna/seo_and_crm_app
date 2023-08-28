from urllib.parse import urlparse


def get_domain_from_url(url):
    if 'https://' not in url:
        url = 'https://' + url
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    return domain