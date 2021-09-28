import requests
import time
import json
from requests.structures import CaseInsensitiveDict
import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "Smarttrader.Ai@gmail.com"  # Enter your address
#receiver_email = "amareshnlr@gmail.com"  # Enter receiver address
password = 'amar@0987'
#Subject: Hi there

#Add Emails to this List
receiver_email_list= ["amareshnlr@gmail.com", "p.amareswar20@dmsiitd.org", "vinaykumar7295@gmail.com"]
#This message is sent from Python."""

def sendEmail(message):
    message = message
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        for email_id in receiver_email_list:
            server.sendmail(sender_email, email_id, message)
            
            
url = "https://swingtraderindia.com/api/notification/notification?pageIdx=1&pageSize=25&orderBy=date&order=DESC"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer HzzeKOqx6SZ4aj2zOXGV8HBjF7KWO26hlXCVkKcBzbE8aB_oQWyrNFiWSAPfQi17QDBI0cUeKPDpKI3wPhtLAYzlP0_dxF1f4IPq9y4khFQfAbH7F2YQbyHoU4Kf8NxKugQNHyHlIjrksJkWZFhxQ-n2vRRbWemP5f33FJtvhj_HTZMIFTMc4xS2h180ps8uSSDNDA5wtiRfmd7B5GMxnexYwUKmNBfVSjDq4ggd5pgTmktLhWTnLVyZtaG8wB013-iidKEqstaPXz5QZq8wKRdEEgQjmVd-xMBjVAx-tlnYVoXkBjeiT85RPDdaT0DOAhJKo59C_J9lRXgohoi0wFkzMEXWaUP8GqQtGFdpdIYKWGBMz6qiWCLd1cgycHME3hJrvU0mvwZo8C_2yMqzIB5n6rqsGVs03ZzwYcN-3KCOAHx9vy5Z2VSNz0XojdmWN_wZ5u8E0T70rzEmYd7wVSu6i9KgiO7NpCKGQGnHReyC36LE6jmy3qhQHihERzER0GFOW9Hw7bxcAG2g22Kwa3R0OBJui06fR1Ns-xKAKUE9qid7qGgtEhmBbe_d26fcEORfBPK7GqFsdWpD62VlHg9jd4GlEZ6biZ-boiCejip7Rn1x9_RH1GhplO-7_iauh7x8SSoBWdaDcEgoP6EFGnqht7Q"


#while(True):
resp = requests.get(url, headers=headers)
#time.sleep(10)
#print(json.loads(resp.content)['alerts'])
company = ""
while (True):
    time.sleep(3)
    resp = requests.get(url, headers=headers)
    for alert in json.loads(resp.content)['alerts']:
        if(alert['state'] == 1):
            if company == "":
                print("Current Symbol is empty.")
                company = alert['symbol']
                break
            elif company == alert['symbol']:
                break;
            elif company != alert['symbol']:
                print("Take the trade")
                sendEmail("Buy "+company)
                company = alert['symbol']
                print(alert['symbol'])
                break
