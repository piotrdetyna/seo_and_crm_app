from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ..secrets import REGON_API_KEY
from litex.regon import REGONAPI, REGONAPIError 
from lxml import etree
import xmltodict
from time import sleep
import whois

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Opera GX";v="100"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36'
}

def get_domain_from_url(url):
    if not url.startswith('http'):
        url = add_https(url)
    
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = remove_www(url)
        return domain
    return
    

def add_https(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"https://{url}"
    return url

def remove_www(url):
    if url.startswith('www.'):
        return url[4:]
    return url

def is_response_code_ok(code):
    return code >= 200 and code < 300

def is_site_available(url):
    try:
        response = requests.get(url, headers=headers)
        return is_response_code_ok(response.status_code)
    
    except requests.RequestException:
        return False
    
def extract_search_results_from_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    search_results = soup.find_all('div', class_='tF2Cxc')
    return search_results


def check_position(keyword, domain, max_pages=3):
    position = 1
    for page in range(max_pages):

        url = f"https://www.google.com/search?q={keyword}&start={page*10}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
                
        for result in extract_search_results_from_html(response.text):
            link = result.find('a')['href']
            if domain in link:
                return position
            position += 1
        sleep(3)

    return 101


def get_external_links(url, excluded=[]):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('Error while getting external links', e)
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    base_domain = get_domain_from_url(url)
    links = []
    excluded = excluded.copy()
    excluded.extend(['tel:', 'mailto:', 'javascript:'])

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
        response = requests.get(url, headers=headers)
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
    return set(pages)



def get_company_info(nip):
    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
    api.login(REGON_API_KEY)
    try:
        company_info_data = api.search(nip=nip)[0]
    except REGONAPIError:
        return {
            'data': {'error': 'Incorrect nip'},
            'ok': False,
        }

    company_info_xml = etree.tostring(company_info_data, pretty_print=True).decode('utf-8')
    company_info_json = xmltodict.parse(company_info_xml)['dane']
    return {
            'ok': True,
            'data': company_info_json,
        }


def get_domain_expiry_date(domain):
    try:
        w = whois.whois(domain)
        date = w.get('expiration_date', None)
        if date:
            return date.date()
    except Exception as e:
        print(f"An error encountered while checking {domain}'s expiration date: {e}")
    return None