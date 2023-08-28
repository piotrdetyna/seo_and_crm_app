from urllib.parse import urlparse


def get_domain_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]  # Usuń ewentualny prefiks 'www.'
        return domain
    else:
        return "Nieprawidłowy link"