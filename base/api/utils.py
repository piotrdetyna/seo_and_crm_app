from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ..secrets import REGON_API_KEY
from litex.regon import REGONAPI, REGONAPIError 
from lxml import etree
import xmltodict

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
    

def add_https(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"https://{url}"
    return url


def is_site_available(url):
    try:
        response = requests.get(url, headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Cookie': 'PHPSESSID=6daocdjrk1u39ikn2pp9cn9005; _snrs_sb=ssuid:2b37b9ab-943a-4570-abbe-49ee4dc114c9&leaves:1693384058; _snrs_sa=ssuid:2b37b9ab-943a-4570-abbe-49ee4dc114c9&appear:1693384057&sessionVisits:1; _snrs_p=host:www.mediaexpert.pl&permUuid:e70725a4-b230-47bb-8d42-aabc7d0a96d6&uuid:e70725a4-b230-47bb-8d42-aabc7d0a96d6&identityHash:&user_hash:&init:1693384058&last:1693384058&current:1693384058&uniqueVisits:1&allVisits:1; _snrs_uuid=e70725a4-b230-47bb-8d42-aabc7d0a96d6; _snrs_puuid=e70725a4-b230-47bb-8d42-aabc7d0a96d6; SPARK_TEST=1; _snrs_cid=0; __cf_bm=oNUccz7nSkpqgoAUcrtVsAnLeweVUnXaQmCaqhn_dzI-1693384059-0-AcpraOMO07EPv3Krtkc9yNpRYdfdV4NJipcTyeoAvISjs6ivSiOTMN4hRRAh8HuIiG79/EH4uMiCsR4wZ+qU3eo=; new_csem=; _snrs_dc_views_sd_3bf815ba-9f13-4dc5-90b2-ca57c8289ead=1; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Aug+30+2023+10%3A33%3A44+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=61041d51-9e62-4838-910e-d77ad71fa78f&interactionCount=1&landingPath=https%3A%2F%2Fwww.mediaexpert.pl%2Fdom-i-ogrod%2Fartykuly-dla-zwierzat%2Fkarmy-dla-psow&groups=ME001%3A1%2CME002%3A0%2CME003%3A0%2CME004%3A0',
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
        })
        if response.status_code >= 200 and response.status_code < 300:
            return True
        else:
            return False
    except requests.RequestException:
        return False


def get_external_links(url, excluded=[]):
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
    return set(pages)



def get_company_info(nip):
    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
    api.login(REGON_API_KEY)
    try:
        company_info_data = api.search(nip=nip)[0]
    except REGONAPIError:
        return {
            'data': 'Incorrect nip',
            'ok': False,
        }

    company_info_xml = etree.tostring(company_info_data, pretty_print=True).decode('utf-8')
    company_info_json = xmltodict.parse(company_info_xml)['dane']
    return {
            'ok': True,
            'data': company_info_json,
        }
