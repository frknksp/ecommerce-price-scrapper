from bs4 import BeautifulSoup
import requests
import re
from mongodb import dbconnect

client = dbconnect()
laptops = client.laptops
trendyoldb_collection = laptops.trendyols

trendyoldb_collection.delete_many({})

def trendrun(headers,totalnumberofpages):
    numberofpages = 1
    while numberofpages < totalnumberofpages:
        print(numberofpages)
        # url = "https://www.trendyol.com/sr?wc=103108&mb=kurumsal_satici&pi="+str(numberofpages)
        url = "https://www.trendyol.com/sr/laptop-x-c103108?sst=BEST_SELLER&pi=" + str(numberofpages)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")

        table = soup.find("div",attrs={"class":"prdct-cntnr-wrppr"})
        alltables = table.find_all("div",attrs={"class":"p-card-wrppr with-campaign-view"})
        for urun in alltables:
            urunobj = {
                "marka": "",
                "model": "",
                "fiyat": "",
                "fotolink": "",
                "isletim_sistemi": "",
                "islemci": "",
                "islemci_modeli": "",
                "islemci_hizi": "",
                "ram": "",
                "disk_boyutu": "",
                "disk_turu": "",
                "ekran_boyutu": "",
                "ekran_karti": "None",
                "puan": "",
                "site": "Trendyol",
                "link": ""
            }
            urun_linkleri = urun.a.get("href")
            link_basi = "https://www.trendyol.com"
            tamlink = link_basi + urun_linkleri
            # print(tamlink)
            r1 = requests.get(tamlink)
            detay_soup = BeautifulSoup(r1.content, "lxml")

            fiyat = ""
            fotolink = ""
            marka = ""
            model = ""
            title = ""
            isletim_sistemi = ""
            islemci = ""
            islemci_modeli = ""
            islemci_hizi = ""
            ram = ""
            disk_boyutu = ""
            disk_turu = ""
            ekran_boyutu = ""
            ekran_karti = ""
            puan = ""
            site = "Hepsiburada"
            links = tamlink
            urunobj["link"] = links

            pricebox = detay_soup.find("div",attrs={"class":"pr-in-cn"})
            title = pricebox.find("div",attrs={"class":"pr-in-cn"})
            markas = pricebox.find("a")
            marka = markas.text
            urunobj["marka"] = marka
            modelwtitle = pricebox.find("span")
            # marka = mark[0].text
            # utitle = title[0].text
            # print(marka)
            # print(marka)
            title = modelwtitle.text
            if "Macbook" in title:
                titlsplit = re.split('M1|M2|13"|16"|14"|Intel', title, maxsplit=1)

            else:
                titlsplit = re.split('AMD|Amd|Intel|Ryzen|INTEL|intel|amd|İntel|i5-|i3-|i7-|I7-|I7|I5-|I3-|I9-|I5|Pentium|R7-|Celeron',title, maxsplit=1)

            # print(title)
            model = titlsplit[0]
            urunobj["model"] = model
            # print(model)
            price = pricebox.find("span",attrs={"class":"prc-dsc"})
            fiyat = price.text
            urunobj["fiyat"] = fiyat

            fotobox = detay_soup.find("div", attrs={"class": "gallery-container"})
            fotoboxn = fotobox.find("img", attrs={"loading": "lazy"})
            fotolink = fotoboxn.get("src")
            urunobj["fotolink"] = fotolink
            # print(fotolink)

            tumozellikler = detay_soup.find_all("li",attrs={"class":"detail-attr-item"})
            for i in tumozellikler:
                ozellik = i.find("span")
                deger = i.find("b")
                if ozellik.text == "Ram (Sistem Belleği)":
                    ram = deger.text.strip()
                    urunobj["ram"] = ram
                if ozellik.text == "Ekran Boyutu":
                    ekran_boyutu = deger.text.strip()
                    urunobj["ekran_boyutu"] = ekran_boyutu
                if ozellik.text == "İşlemci Tipi":
                    islemci = deger.text.strip()
                    urunobj["islemci"] = islemci
                if ozellik.text == "İşlemci Modeli":
                    islemci_modeli = deger.text.strip()
                    urunobj["islemci_modeli"] = islemci_modeli
                if ozellik.text == "Temel İşlemci Hızı":
                    islemci_hizi = deger.text.strip()
                    urunobj["islemci_hizi"] = islemci_hizi
                if ozellik.text == "Ekran Kartı":
                    ekran_karti = deger.text.strip()
                    urunobj["ekran_karti"] = ekran_karti
                if ozellik.text == "İşletim Sistemi":
                    isletim_sistemi = deger.text.strip()
                    if isletim_sistemi == "Free Dos":
                        isletim_sistemi = "Freedos"
                    urunobj["isletim_sistemi"] = isletim_sistemi
                disk_turu = "SSD"
                urunobj["disk_turu"] = disk_turu
                if ozellik.text == "SSD Kapasitesi":
                    disk_boyutu = deger.text.strip()
                    urunobj["disk_boyutu"] = disk_boyutu

            # filter = {'marka': marka, 'model': model}
            # count = trendyoldb_collection.count_documents(filter=filter)
            # print(count)
            # if count < 1:
            trendyoldb_collection.insert_one(urunobj)
            #     print("eklendi")
            # else:
            #     print("zaten var")
            #     count = trendyoldb_collection.count_documents(filter=filter)
            #     new_values = {"$set": {'fiyat': fiyat}}
            #     trendyoldb_collection.update_one(filter, new_values, upsert=True)

        numberofpages = numberofpages + 1

    print(trendyoldb_collection.distinct("isletim_sistemi"))
