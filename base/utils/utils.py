from urllib.parse import urlparse


def get_domain_from_url(url):
    if not url.startswith('http'):
        url = 'https://' + url
    
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    else:
        return None
