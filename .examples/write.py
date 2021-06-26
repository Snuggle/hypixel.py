import grequests
import json
#TODO add commentss

base_url = f"https://api.hypixel.net/skyblock/auctions"
resp = grequests.get(base_url)

res = json.loads(resp.content)
pages = res['totalPages']
if res['success']:
    data = {}
    data['auctions'] = []
    for auction in res['auctions']:
        data['auctions'].append(auction)
    pageurls = []
    for page in range(1, (pages - 1)):
        purl = base_url + f'?page={page}'
        pageurls.append(purl)
    resps = (grequests.get(url) for url in pageurls)
    for r in resps:
        respd = json.loads(r.content)
        if data['success']:
            for auction in respd['auctions']:
                data['auctions'].append(auction)
        else:
            raise RuntimeError(f'GET Request failed')
else:
    raise RuntimeError(f'Page 0 GET Request failed')