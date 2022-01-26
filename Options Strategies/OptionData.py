import requests
import json
def downloaddata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
        "Accept": "*/*"
    }
    url = url
    r = requests.get(url, headers=headers)
    
    if(r.status_code == 200):
        json_data = json.loads(r.content)
        return json_data;
    else:
        return None;

fiidii_data_url = "https://opstra.definedge.com/api/fiidiidata"
fiidii_data = downloaddata(fiidii_data_url)
print(fiidii_data)