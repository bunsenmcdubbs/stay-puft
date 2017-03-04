from requests import request
import json

HACKALIST_API_URL = 'http://www.hackalist.org/api/1.0/%d/%02d.json'

def fetch_month(year, month):
    res = request('GET', HACKALIST_API_URL%(year, month)).content
    data = json.loads(res).values()[0]
    return data

if __name__=="__main__":
    print fetch_month(2014, 8)
    
