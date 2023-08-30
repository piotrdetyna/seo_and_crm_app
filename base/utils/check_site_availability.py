import requests

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
        print('status code:', response.status_code)
        if response.status_code >= 200 and response.status_code < 300:
            return True
        else:
            return False
    except requests.RequestException:
        return False