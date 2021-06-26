import json
import requests

class AuctionHouse:
    def __init__(self):
        data = {
            'auctions': [

            ]
        }

    def getauctions(self):
        data = self.data
        url_base = f"https://api.hypixel.net/skyblock/auctions"
        firstpage = json.loads(requests.get(url_base).text) #get the first page and load it as a dictionary
        
        if firstpage['success']:
            data["totalauctions"] = firstpage['totalAuctions']
            for page in range(1, firstpage['pages'] - 1): #for each page - 1 since we checked 0
                page_url = url_base + f'?page={page}'
                pagedata = json.loads(requests.get('page_url').text)#convert to dictionary
                for auc in pagedata:
                    data['auctions'].append(auc)#append it to the dictonary
            return(data)