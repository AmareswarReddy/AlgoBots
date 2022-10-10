#%%
#%%
import requests as req
from datetime import datetime, timedelta
from dateutil import parser, tz
import pendulum
from dateutil.relativedelta import relativedelta
import mysql.connector
import time



headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)",
    "Accept": "*/*"
}

#Set cookies to access the website
cookiesUrl = 'https://www.nseindia.com/companies-listing/corporate-filings-financial-results'
def setcookies():
    print("Setting cokkies")
    global r
    r = req.get(cookiesUrl, headers=headers)
    global cookies 
    cookies = {}
    for c in r.cookies:
        print(c.name, c.value)
        if (c.name == 'nseappid'):
            cookies['nseappid'] = c.value        
        if(c.name == 'nsit'):
            cookies['nsit'] = c.value
        
setcookies()


boardMeetingUrl = "https://www.nseindia.com/api/corporate-board-meetings?index=equities"
corporateActionsUrl = "https://www.nseindia.com/api/corporates-corporateActions?index=equities"
upcomingEventsUrl = "https://www.nseindia.com/api/event-calendar?index=equities"
financialResultsUrl = "https://www.nseindia.com/api/corporates-financial-results?index=equities&period=Quarterly"
announcmentsUrl ="https://www.nseindia.com/api/corporate-announcements?index=equities"

timeelapsed = 24
while True:    
    # Following code runs in loop
    for c in r.cookies:
            if (c.is_expired() ==  True):
                setcookies()
            else:
                break  

    ist = pendulum.timezone('Asia/Calcutta')
    currentDate = datetime.date(datetime.now(ist)).strftime("%d-%m-%Y")
    threeMonthDate = datetime.date(datetime.now(ist)+relativedelta(months=+2)).strftime("%d-%m-%Y")
    print(currentDate)
    print(threeMonthDate)
    payload = {'from_date':currentDate,'to_date':threeMonthDate}


    while timeelapsed == 24:
        print("Inside the second loop")
        corporateActionsresp = req.get(corporateActionsUrl,params=payload, headers=headers, cookies= cookies)
        print("")
        print("")
        print(corporateActionsresp.url)
        corporateActionsTuple = []
        for dictElement in corporateActionsresp.json():
            temptuple = (dictElement['symbol'], dictElement['comp'],dictElement['series'], dictElement['faceVal'], dictElement['subject'], parser.parse(dictElement['exDate']), dictElement['recDate'], dictElement['bcStartDate'], dictElement['bcEndDate'], dictElement['ndStartDate'], dictElement['ndEndDate'])
            corporateActionsTuple.append(temptuple)
        print(corporateActionsTuple)


        upcomingEventsresp = req.get(upcomingEventsUrl,params=payload, headers=headers, cookies= cookies)
        print("")
        print("")
        print(upcomingEventsresp.url)
        upcomingEventsTuple = []
        for dictElement in upcomingEventsresp.json():
            temptuple = (dictElement['symbol'], dictElement['company'],dictElement['purpose'], dictElement['bm_desc'], parser.parse(dictElement['date']))
            upcomingEventsTuple.append(temptuple)
        print(upcomingEventsTuple)
        #timeelapsed = 0

   

    announcmentsresp = req.get(announcmentsUrl, headers=headers, cookies= cookies)
    print(announcmentsresp.url)
    announcmentsTuple = []
    for dictElement in announcmentsresp.json():
        temptuple = (dictElement['symbol'], dictElement['sm_name'], dictElement['desc'],dictElement['attchmntText'], dictElement['attchmntFile'], parser.parse(dictElement['an_dt']))
        announcmentsTuple.append(temptuple)
    print(announcmentsresp)
    timeelapsed = timeelapsed+1
    time.sleep(150)

# %%
