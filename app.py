from schedule import every, repeat, run_pending
from time import sleep
from bs4 import BeautifulSoup
import requests
from datetime import datetime

@repeat(every(1).minute) #.until("18:30")
def getir_to_excel():

    url_list = ["https://getir.com/yemek/restoran/konoha-bagdat-cad-kadikoy-istanbul/"]
    k = 0

    for i in url_list:

        try:
            r = requests.get(i)
        except requests.exceptions.ConnectionError:
            sec = 60*3
            sleep(sec)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            s = soup.find("div", id = "__next")
            s2 = s.find("div", class_ = 'sc-212542e0-2 ckZpLq')
            s4 = s2.find("main", class_="sc-212542e0-0 iiapCb")
            s5 = s4.find("div", class_ = "sc-e85e5299-0 sc-4e0754cc-0 hkaVQN klYfLJ")
            s6 = s5.find("div", class_ = "sc-4e0754cc-1 YPsgm")
            s7 = s6.find("div", class_ = "sc-4e0754cc-3 bwTzrw")
            s8 = s7.find("div", class_ = "sc-7047f3e2-6 iFptQI")
            s9 = s8.find("div", class_ = "style__Wrapper-sc-__sc-sbxwka-15 jPuQcd")
            s10 = s9.find("div", class_= "style__CardWrapper-sc-__sc-sbxwka-12 ccsSiU")
            s11 = s10.find("div",class_="style__ContentWrapper-sc-__sc-sbxwka-7 emAjmS")
            s12 = s11.find("div", class_ = "sc-7047f3e2-0 iJHJBI")
            s13 = s12.find("div", class_ = "sc-7047f3e2-3 hbiBbV")
            s14 = s13.find("span",class_ = "style__Text-sc-__sc-1nwjacj-0 jbOUDC sc-7047f3e2-8 iFDpNz")

            print(s14.get_text())
            print(r.status_code) # this means is open
            print(datetime.now())
            k+=1
            print(k)
        
        else:
            print(r.status_code) # this means is close
    return url_list

while True:
    run_pending()
    sleep(1)
