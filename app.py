from schedule import every, repeat, run_pending
from time import sleep
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from openpyxl import load_workbook
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
)

engine = create_engine("sqlite:///logs.db", echo=True)
meta = MetaData()

logs = Table(
    "logs",
    meta,
    Column("id", Integer, primary_key=True),
    Column("branch", String(80)),
    Column("brand", String(80)),
    Column("date", String(80)),
    Column("hour", String(80)),
    Column("status", String(80)),
    Column("current_rating", Float),
)
meta.create_all(engine)


def save_to_db(branch, brand, date, hour, status, current_rating):

    sql = logs.insert().values(
        branch=branch,
        brand=brand,
        date=date,
        hour=hour,
        status=status,
        current_rating=current_rating,
    )
    engine.execute(sql)


def save_to_db_log(branch, brand, date, hour, log):

    sql = logs.insert().values(
        branch=branch, brand=brand, date=date, hour=hour, status=log, current_rating=log
    )


def save_to_excel(
    ws, wb, myFileName, branch, brand, date, hour, status, current_rating
):
    ws.append([branch, brand, date, hour, status, current_rating])

    wb.save(filename=myFileName)

    wb.close()


def save_to_excel_log(ws, wb, myFileName, branch, brand, date, hour, log):
    ws.append([branch, brand, date, hour, log, log])

    wb.save(filename=myFileName)

    wb.close()


def getir_to_excel_first():

    myFileName = r"./logs.xlsx"

    wb = load_workbook(filename=myFileName)

    # TODO: gonna create the page for every restaurant and make the changes into those restaurants
    ws = wb["Sheet1"]

    # TODO: Be sure that all the restaurant are open! And get the links. Then create a if statement to make OPEN/CLOSE diff. Belove statement is not quite right, gotta change it with the real time case.
    url_dict = {
    }

    num = str(len(list(url_dict.keys())))
    print(f"{num} restaurant's data are gonna be collected.")

    for url_key in url_dict.keys():
        url = url_dict[url_key]
        url_key_list = url_key.split(" ")
        branch = url_key_list[0]
        url_key_list.pop(0)
        brand = " ".join(url_key_list)
        now = datetime.now()
        format_date = "%d/%m/%Y"
        format_hour = "%H:%M:%S"
        # format datetime using strftime()
        date = now.strftime(format_date)
        hour = now.strftime(format_hour)
        r = None

        index = str(list(url_dict.keys()).index(url_key))

        # This is for 'if connection get suspened by getir.com because we are making so much request in a short time'
        try:
            r = requests.get(url)
        except Exception as e:
            log = str(e)

            save_to_excel_log(
                ws=ws,
                wb=wb,
                myFileName=myFileName,
                branch=branch,
                brand=brand,
                date=date,
                hour=hour,
                log=log,
            )

            save_to_db_log(branch=branch, brand=brand, date=date,hour=hour, log=log)

            print(index + log)

            continue

        if r == None:
            print(index + "URL is None")
            continue

        # TODO: This is gonna change, because we are not checking the restauant open/close status by status.code normally. # Have the screenshot in the screenshots.

        soup = BeautifulSoup(r.content, "html.parser")

        try:
            close = get_close(soup=soup)

        except Exception as e:
            log = str(e)

            save_to_excel_log(
                ws=ws,
                wb=wb,
                myFileName=myFileName,
                branch=branch,
                brand=brand,
                date=date,
                hour=hour,
                log=log,
            )

            save_to_db_log(branch=branch, brand=brand, date=date, hour=hour, log=log)

            print(index + log)
            continue

        try:
            current_rating = get_rating(soup=soup)

        except Exception as e:
            current_rating = None

        # Check that if close state is exsist in the html.
        if close == None:
            # TODO: append the date to the current sheet. But this is gonna change by the restaurant.
            status = "AÇIK"

            try:

                save_to_excel(
                    ws=ws,
                    wb=wb,
                    myFileName=myFileName,
                    branch=branch,
                    brand=brand,
                    date=date,
                    hour=hour,
                    status=status,
                    current_rating=current_rating,
                )

                print(index + "Changes saved to excel!")

            except Exception as e:
                print(index + str(e))
                print(index + "Couldn't write to excel! Keep looping")
                continue

            try:
                save_to_db(
                    branch=branch,
                    brand=brand,
                    date=date,
                    hour=hour,
                    status=status,
                    current_rating=current_rating,
                )

            except Exception as e:
                print(index + str(e))
                print("Couldn't write to db!")
                continue

        # TODO: This is gonna be canceled because we are not going to calculate the current OPEN/CLOSE status with this
        else:
            status = "KAPALI"

            try:

                save_to_excel(
                    ws=ws,
                    wb=wb,
                    myFileName=myFileName,
                    branch=branch,
                    brand=brand,
                    date=date,
                    hour=hour,
                    status=status,
                    current_rating=current_rating,
                )

                print(index + "Changes saved to excel!")

            except Exception as e:

                print(index + str(e))
                print(index + "Couldn't write to excel! Keep looping")
                continue

            try:
                save_to_db(
                    branch=branch,
                    brand=brand,
                    date=date,
                    hour=hour,
                    status=status,
                    current_rating=current_rating,
                )

            except Exception as e:
                print(index + str(e))
                print("Couldn't write to db!")
                continue

        sleep(5)

    return url_dict  # temp


def get_rating(soup):
    # Find the rate
    body = soup.body
    s = body.find("div", id="__next")
    s2 = s.find("div", class_="sc-212542e0-2 ckZpLq")
    s4 = s2.find("main", class_="sc-212542e0-0 iiapCb")
    s5 = s4.find("div", class_="sc-e85e5299-0 sc-4e0754cc-0 hkaVQN klYfLJ")
    s6 = s5.find("div", class_="sc-4e0754cc-1 YPsgm")
    s7 = s6.find("div", class_="sc-4e0754cc-3 bwTzrw")
    s8 = s7.find("div", class_="sc-7047f3e2-6 iFptQI")
    s9 = s8.find("div", class_="style__Wrapper-sc-__sc-sbxwka-15 jPuQcd")
    s10 = s9.find("div", class_="style__CardWrapper-sc-__sc-sbxwka-12 ccsSiU")
    s11 = s10.find("div", class_="style__ContentWrapper-sc-__sc-sbxwka-7 emAjmS")
    s12 = s11.find("div", class_="sc-7047f3e2-0 iJHJBI")
    s13 = s12.find("div", class_="sc-7047f3e2-3 hbiBbV")
    rate = s13.find(
        "span", class_="style__Text-sc-__sc-1nwjacj-0 jbOUDC sc-7047f3e2-8 iFDpNz"
    )

    current_rating = rate.get_text()

    return current_rating


def get_close(soup):
    body = soup.body
    s11 = body.find("div", id="__next")
    s10 = s11.find("div", class_="sc-212542e0-2 ckZpLq")
    s9 = s10.find("main", class_="sc-212542e0-0 iiapCb")
    s8 = s9.find("div", class_="sc-e85e5299-0 sc-4e0754cc-0 hkaVQN klYfLJ")
    s7 = s8.find("div", class_="sc-4e0754cc-1 YPsgm")
    s6 = s7.find("div", class_="sc-4e0754cc-3 bwTzrw")
    s5 = s6.find("div", class_="sc-7047f3e2-6 iFptQI")
    s4 = s5.find("div", class_="style__Wrapper-sc-__sc-sbxwka-15 jPuQcd")
    s3 = s4.find("div", class_="style__CardWrapper-sc-__sc-sbxwka-12 ccsSiU")
    s2 = s3.find("div", class_="style__ContentWrapper-sc-__sc-sbxwka-7 emAjmS")
    close = s2.find("div", class_="sc-e27f3f42-0 hPdSRl")

    return close


@repeat(every(1).hour)  # .until("18:30")
def getir_to_excel():

    getir_to_excel_first()


# for the first time and then let the schdule does it's job
getir_to_excel_first()

while True:
    run_pending()
    sleep(1)
