from schedule import every, repeat, run_pending
from time import sleep
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from openpyxl import load_workbook

def get_rating(soup):
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

        current_rating = rate.get_text()

        return current_rating

def get_close(soup):

    s11 = soup.find("div", id= "__next")
    s10 = s11.find("div", class_= "sc-212542e0-2 ckZpLq")
    s9 = s10.find("main", class_= "sc-212542e0-0 iiapCb")
    s8 = s9.find("div", class_="sc-e85e5299-0 sc-4e0754cc-0 hkaVQN klYfLJ")
    s7 = s8.find("div", class_ = "sc-4e0754cc-1 YPsgm")
    s6 = s7.find("div", class_="sc-4e0754cc-3 bwTzrw")
    s5 = s6.find("div", class_= "sc-7047f3e2-6 iFptQI")
    s4 = s5.find("div", class_ = "style__Wrapper-sc-__sc-sbxwka-15 jPuQcd")
    s3 = s4.find("div", class_="style__CardWrapper-sc-__sc-sbxwka-12 ccsSiU") 
    s2 = s3.find("div", class_="style__ContentWrapper-sc-__sc-sbxwka-7 emAjmS")
    close = s2.find("div", class_= "sc-e27f3f42-0 hPdSRl")

    return close

def get_name(url):

    return url.split("/")[-2]


@repeat(every(2).second) #.until("18:30")
def getir_to_excel():

    myFileName=r'./Sheet.xlsx'

    wb = load_workbook(filename=myFileName)
    
    #TODO: gonna create the page for every restaurant and make the changes into those restaurants
    ws = wb['Sheet1']
    
    #TODO: Be sure that all the restaurant are open! And get the links. Then create a if statement to make OPEN/CLOSE diff. Belove statement is not quite right, gotta change it with the real time case.
    url_dict = {
        "Alle Bowls":"https://getir.com/yemek/restoran/alle-bowls-acibadem-mah-kadikoy-istanbul/",
        "Arianas Cheesecake":"https://getir.com/yemek/restoran/ariana-s-cheesecake-acibadem-mah-kadikoy-istanbul/",
        "Big Bold Quick":"https://getir.com/yemek/restoran/bbq-big-bold-quick-acibadem-mah-kadikoy-istanbul",
        "Caesar Salad By":"https://getir.com/yemek/restoran/caesar-salad-by-chef-amadeo-acibadem-mah-kadikoy-istanbul",
        "Çosa":"https://getir.com/yemek/restoran/cosa-bi-corba-bi-salata-acibadem-mah-kadikoy-istanbul/",
        "Detroit Bad Boys Pizza":"https://getir.com/yemek/restoran/detroit-bad-boys-pizza-acibadem-mah-kadikoy-istanbul",
        "Dlycious Dyssert": "https://getir.com/yemek/restoran/dydy-dylicious-dyssert-acibadem-mah-kadikoy-istanbul",
        "Doyuyo":"https://getir.com/yemek/restoran/doyuyo-sarayardi-cad-kadikoy-istanbul/",
        "El Pollo Lasso": "https://getir.com/yemek/restoran/el-pollo-lasso-acibadem-mah-kadikoy-istanbul/",
        "Etişler Köfte" : "https://getir.com/yemek/restoran/et-isleri-kofte-burger-durum-acibadem-mah-kadikoy-istanbul/",
        "Fadelini" : "https://getir.com/yemek/restoran/fadelini-acibadem-mah-kadikoy-istanbul/",
        "Fun For Fit": "https://getir.com/yemek/restoran/fun-for-fit-acibadem-mah-kadikoy-istanbul",
        "G&G Burger": "https://getir.com/yemek/restoran/g-g-burger-acibadem-mah-kadikoy-istanbul-2/",
        "Gurra Tavuk": "https://getir.com/yemek/restoran/gurra-tavuk-doner-acibadem-mah-kadikoy-istanbul",
        "Jay Jay Fries": "https://getir.com/yemek/restoran/jay-jay-fries-acibadem-mah-kadikoy-istanbul",
        "Kale Arkası Mutfak": "https://getir.com/yemek/restoran/kale-arkasi-mutfak-acibadem-mah-kadikoy-istanbul",
        "Kengeres Çiğ Köfte" : "https://getir.com/yemek/restoran/kengeres-gurme-cig-kofte-acibadem-mah-kadikoy-istanbul",
        "Madritas": "https://getir.com/yemek/restoran/madritas-acibadem-mah-kadikoy-istanbul",
        "Mztps Meze" : "https://getir.com/yemek/restoran/mztps-meze-tapas-acibadem-mah-kadikoy-istanbul",
        "Nane Mantı" : "https://getir.com/yemek/restoran/nane-manti-acibadem-mah-kadikoy-istanbul/",
        "Noody" : "https://getir.com/yemek/restoran/noody-acibadem-mah-kadikoy-istanbul/",
        "Red Haag" : "https://getir.com/yemek/restoran/red-haag-cafe-brasserie-acibadem-mah-kadikoy-istanbul",
        "Rylee's Ranch Salad": "https://getir.com/yemek/restoran/rylee-s-ranch-salad-acibadem-mah-kadikoy-istanbul/",
        "Seez Beez": "https://getir.com/yemek/restoran/seez-beez-falafel-wraps-burgers-acibadem-mah-kadikoy-istanbul",
        "Senor Torreon":"https://getir.com/yemek/restoran/senor-torreon-red-hot-spicy-food-acibadem-mah-kadikoy-istanbul/",
        "Tabur Köfte":"https://getir.com/yemek/restoran/tabur-kofte-acibadem-mah-kadikoy-istanbul",
        "The Bowl":"https://getir.com/yemek/restoran/the-bowl-best-of-we-love-acibadem-mah-kadikoy-istanbul",
        "Veganista" : "https://getir.com/yemek/restoran/veganista-acibadem-mah-kadikoy-istanbul"

    }

    for url_key in url_dict.keys():

        '''
        #This is for 'if connection get suspened by getir.com because we are making so much request in a short time'
        try:
            r = requests.get(i)
        except requests.exceptions.ConnectionError:
            sec = 60*3
            sleep(sec)
        '''
        url = url_dict[url_key]

        r = requests.get(url)

        #normal status code checks
        if r.status_code == 404:
            print(f"The url is not valid {url}.")

        if r.status_code != 200:
            print("An error occured while creating a connection between app and the getir server ")

        #TODO: This is gonna change, because we are not checking the restauant open/close status by status.code normally. # Have the screenshot in the screenshots.

        soup = BeautifulSoup(r.content, 'html.parser')

        close = get_close(soup=soup)

        date = datetime.now()

        name = get_name(url=url)

        try:
            current_rating = get_rating(soup=soup)

        except Exception as e:

            current_rating = "NO RATING"
            print(e)
        
        # Check that if close state is exsist in the html.
        if close == None:            
            #TODO: append the date to the current sheet. But this is gonna change by the restaurant.
            ws.append([name, date, "AÇIK" , current_rating])

            wb.save(filename=myFileName)

            wb.close()

            print("Changes saved!")
        
        #TODO: This is gonna be canceled because we are not going to calculate the current OPEN/CLOSE status with this
        else:

            ws.append([name ,date, "KAPALI" , current_rating])

            wb.save(filename=myFileName)
    
            wb.close()

            print("Changes saved!")
    
            print("URL is not found.")

    return url_dict # temp


while True:
    run_pending()
    sleep(1)

'''
def get_name(soup):

    s11 = soup.find("div", id = "__next")
    s10 = s11.find("div", class_ = "sc-212542e0-2 gfYNGG")
    s9 = s10.find("main", class_ = "sc-212542e0-0 kYcfkH")
    s8 = s9.find("div", class_ = "sc-e85e5299-0 sc-4e0754cc-0 jClnfO jePsfF")
    s7 = s8.find("div", class_ = "sc-4e0754cc-1 dOyrVi")
    s6 = s7.find("div", class_ = "sc-4e0754cc-3 gwxSQr")
    s5 = s6.find("div", class_ = "sc-7047f3e2-6 dxWpfi") 
    s4 = s5.find("div", class_ = "style__Wrapper-sc-__sc-sbxwka-15 hZQrGs")
    s3 = s4.find("div", class_ = "style__CardWrapper-sc-__sc-sbxwka-12 iBBNFu")
    s2 = s3.find("div", class_ = "style__ContentWrapper-sc-__sc-sbxwka-7 fIhlvO")
    s1 = s2.find("div", class_ = "sc-7047f3e2-0 ggYwVs")
    name = s1.find("h1", class_="style__Title1-sc-__sc-1nwjacj-2 hIkhWh sc-7047f3e2-2 hAeUHj")

    return name
'''