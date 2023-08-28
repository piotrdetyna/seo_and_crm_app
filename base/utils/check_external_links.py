import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from time import sleep

def get_external_links_from_url(url, excluded):
    try:
        print('Sprawdzam: ', url)
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        base_domain = urlparse(url).netloc
        links = []

        for link in soup.find_all('a', href=True):
            
            absolute_url = urljoin(url, link['href'])
            parsed_url = urlparse(absolute_url)
            domain = parsed_url.netloc.replace('www.', '')


            if domain == base_domain.replace('www.', ''):
                continue

            skip = False
            for keyword in excluded:
                if keyword in absolute_url:
                    skip = True
                    break
            if skip:
                continue            

            
            rel_attribute = link.get('rel', [])
            temp_rel_value = ' '.join(rel_attribute) if rel_attribute else 'dofollow'
            if 'nofollow' in temp_rel_value:
                rel_value = 'nofollow'
            else:
                rel_value = 'dofollow'

            link_info = {'href': absolute_url, 'rel': rel_value, 'domain': domain}
            if domain:
                links.append(link_info)

        return links

    except requests.exceptions.RequestException as e:
        print('Wystąpił błąd', e)
        return []
    

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
        if '/sitemap-home.xml' in url:
            links.append(url_element.text + '/')
            break
        if url_element.text[-1] == '/':
            links.append(url_element.text)
    
    return links

def get_external_links(domain, excluded=['mailto:', 'tel:']):

    domain = 'https://' + domain
    sitemaps = ['/sitemap-posts.xml', '/sitemap-pages.xml', '/sitemap-categories.xml', '/wp-sitemap-posts-page-1.xml', '/wp-sitemap-posts-post-1.xml', '/sitemap-home.xml']
    sites = []
    for sitemap in sitemaps:
        sites.extend(get_links_from_xml(domain + sitemap))
    external_links = {}

    

    for site in sites:
        links = get_external_links_from_url(site, excluded)
        if links:
            path = site.split(domain)[-1]
            external_links[path] = []
            

        for link in links:
            external_links[path].append(link)
    return external_links

