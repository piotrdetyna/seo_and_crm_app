import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from time import sleep
from base.utils.utils import get_domain_from_url
def get_external_links(url, excluded):
    try:
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('Wystąpił błąd', e)
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    base_domain = get_domain_from_url(url)
    links = []
    excluded = excluded.copy()
    excluded.extend(['tel:', 'mailto:', 'javascript:void(0)'])

    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(url, link['href'])
        domain = get_domain_from_url(absolute_url)

        if domain != base_domain and not any(keyword in absolute_url for keyword in excluded):
            rel_attribute = link.get('rel', [])
            rel_value = 'nofollow' if 'nofollow' in ' '.join(rel_attribute) else 'dofollow'

            link_info = {'href': absolute_url, 'rel': rel_value}
            if domain:
                links.append(link_info)

    return links

    

def get_links_from_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return []

    links = []
    soup = BeautifulSoup(response.content, 'xml')
    url_elements = soup.find_all('loc')

    for url_element in url_elements:
        if url_element.text.endswith('/'):
            links.append(url_element.text.replace('www.', ''))

    return links

def get_pages_from_sitemap(domain):
    domain = 'https://' + domain
    sitemaps = ['/sitemap-posts.xml', '/sitemap-pages.xml', '/sitemap-categories.xml', '/wp-sitemap-posts-page-1.xml', '/wp-sitemap-posts-post-1.xml', '/sitemap-home.xml']
    pages = []
    for sitemap in sitemaps:
        pages.extend(get_links_from_xml(domain + sitemap))
    pages.append(domain + '/')
    print(pages)
    return set(pages)
