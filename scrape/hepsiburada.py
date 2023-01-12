from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from mongodb import dbconnect

client = dbconnect()
laptops = client.laptops
hepsiburada_collection = laptops.hepsiburadas

hepsiburada_collection.delete_many({})

def hbrun(headers,totalnumberofpages):
    numberofpages = 1
    while numberofpages < totalnumberofpages:
        print(numberofpages)
        url = "https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa="+str(numberofpages)
        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        st1 = soup.find("div", attrs={"class": "productListContent-pXUkO4iHa51o_17CBibU"})
        st2 = st1.find_all("li", attrs={"class":"productListContent-zAP0Y5msy8OHn5z7T_K_"})
        for urun in st2:
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
                "site": "Hepsiburada",
                "link": ""
            }
            fiyat = ""
            pric = urun.find("div", attrs={"data-test-id": "price-current-price"})
            fiyat = pric.text
            urunobj["fiyat"] = fiyat
            # print(fiyat)

            link =urun.a.get("href")
            link_basi = "https://www.hepsiburada.com/"
            tamlink = link_basi + link
            # print(tamlink)
            r1 = requests.get(tamlink,headers=headers)
            detay_soup = BeautifulSoup(r1.content, "lxml")
            if "adservice" in link:
                continue

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

            titlebox = detay_soup.find("h2", attrs={"class": "product-features-text"})
            try:
                title=titlebox.text

                if "Apple" in title:
                    titlsplit = re.split('M1|M2|13"|16"|14"|Intel', title, maxsplit=1)

                else:
                    titlsplit = re.split('AMD|Amd|Intel|Ryzen|INTEL|intel|amd|İntel|i5-|i3-|i7-|I7-|I7|I5-|I3-|I9-|I5|Pentium|R7-',title, maxsplit=1)

                # print(title)
                # print(titlsplit[0])
                markamodel = titlsplit[0]
                marka = markamodel.split()[0]
                urunobj["marka"] = marka
                model = ' '.join(markamodel.split()[1:])
                urunobj["model"] = model
            except:
                print(links)
            # print(marka)
            # print(model)
            try:
                puanbox = detay_soup.find("span", attrs={"class": "rating-star"})
                puan = puanbox.text.strip()
                urunobj["puan"] = puan
            except:
                puan = "Değerlendirme yok"
                urunobj["puan"] = puan

            imgbox = detay_soup.find("picture", attrs={"itemprop": "image"})
            imglnk = imgbox.img.get("src")
            fotolink = imglnk
            urunobj["fotolink"] = fotolink
            # print(fotolink)

            try:
                valuetablebox = detay_soup.find("div", attrs={"class": "list-item-detail product-detail box-container"})
                valuetable = valuetablebox.find("table", attrs={"class": "data-list tech-spec"})
                tr = valuetable.find_all("tr")
            except:
                print("ozellik tablosu bulunamadi")
            for i in tr:
                ozellik = i.find("th")
                deger = i.find("td")

                if ozellik.text == "Ram (Sistem Belleği)":
                    ram = deger.text.strip()
                    urunobj["ram"] = ram
                if ozellik.text == "Ekran Boyutu":
                    ekran_boyutu = deger.text.strip()
                    urunobj["ekran_boyutu"] = ekran_boyutu
                if ozellik.text == "İşlemci Tipi":
                    islemci = deger.text.strip()
                    urunobj["islemci"] = islemci
                if ozellik.text == "İşlemci":
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
                    if isletim_sistemi == "Yok (Free Dos)":
                        isletim_sistemi = "Freedos"
                    urunobj["isletim_sistemi"] = isletim_sistemi
                disk_turu = "SSD"
                urunobj["disk_turu"] = disk_turu
                if ozellik.text == "SSD Kapasitesi":
                        disk_boyutu = deger.text.strip()
                        urunobj["disk_boyutu"] = disk_boyutu

            # filter = {'marka': marka, 'model': model}
            # count = hepsiburada_collection.count_documents(filter=filter)
            # print(count)
            # if count < 1:
            hepsiburada_collection.insert_one(urunobj)
            #     print("eklendi")
            # else:
            #     print("zaten var")
            #     count = hepsiburada_collection.count_documents(filter=filter)
            #     new_values = {"$set": {'fiyat': fiyat}}
            #     hepsiburada_collection.update_one(filter, new_values, upsert=True)


        numberofpages = numberofpages + 1

    print(hepsiburada_collection.distinct("isletim_sistemi"))

