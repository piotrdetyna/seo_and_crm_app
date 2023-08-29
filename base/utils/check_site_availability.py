import requests

def is_site_available(url):
    try:
        response = requests.get(url, headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        })
        print('status code:', response.status_code)
        if response.status_code >= 200 and response.status_code < 300:
            return True
        else:
            return False
    except requests.RequestException:
        return False