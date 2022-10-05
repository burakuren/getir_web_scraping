from schedule import every, repeat, run_pending
from time import sleep
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from openpyxl import load_workbook

@repeat(every(15).second) #.until("18:30")
def getir_to_excel():

    myFileName=r'./Sheet.xlsx'

    wb = load_workbook(filename=myFileName)
    
    #TODO: gonna create the page for every restaurant and make the changes into those restaurants
    ws = wb['Sheet1']
    
    #TODO: Be sure that all the restaurant are open! And get the links. Then create a if statement to make OPEN/CLOSE diff
    url_list = ["https://getir.com/yemek/restoran/konoha-bagdat-cad-kadikoy-istanbul/",
    "https://getir.com/yemek/restoran/cosa-bi-corba-bi-salata-kozyatagi-mah-kadikoy-istanbul/"
    ]

    for url in url_list:
        '''
        #This is for 'if connection get suspened by getir.com because we are making so much request in a short time'
        try:
            r = requests.get(i)
        except requests.exceptions.ConnectionError:
            sec = 60*3
            sleep(sec)
        '''
        r = requests.get(url)

        #TODO: This is gonna change, because we are not checking the restauant open/close status by status.code normally. # Have the screenshot in the screenshots.
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            #Find the rate
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
            rate = s13.find("span",class_ = "style__Text-sc-__sc-1nwjacj-0 jbOUDC sc-7047f3e2-8 iFDpNz")

            date = datetime.now()
            current_rating = rate.get_text()
            
            #TODO: append the date to the current sheet. But this is gonna change by the restaurant.
            ws.append([url, date, "AÇIK" , current_rating])

            wb.save(filename=myFileName)
    
            wb.close()

            print("Changes saved!")
        
        #TODO: This is gonna be canceled because we are not going to calculate the current OPEN/CLOSE status with this
        else:

            '''
            date = datetime.now()
            
            ws.append([url ,date, "KAPALI" , "Sistem Kapalı"])

            wb.save(filename=myFileName)
    
            wb.close()

            print("Changes saved!")
            '''
            print("URL is not found.")

    return url_list # temp


while True:
    run_pending()
    sleep(1)