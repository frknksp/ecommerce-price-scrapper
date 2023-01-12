from bs4 import BeautifulSoup
import requests
from mongodb import dbconnect

client = dbconnect()
laptops = client.laptops
vatan_collection = laptops.vatans

vatan_collection.delete_many({})

def vatanrun(headers,totalnumberofpages):
    numberofpages = 1
    while numberofpages < totalnumberofpages:
        print(numberofpages)
        url = "https://www.vatanbilgisayar.com/notebook/?page="+str(numberofpages)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find("div",attrs={"id":"productsLoad"})
        urunler = table.find_all("div",attrs={"class":"product-list product-list--list-page"})
        for urun in urunler:
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
                "site": "Vatan Bilgisayar",
                "link": ""
            }

            urun_linkleri = urun.a.get("href")
            link_basi = "https://www.vatanbilgisayar.com/"
            tamlink = link_basi + urun_linkleri
            # print(tamlink)
            r1 = requests.get(tamlink, headers=headers)
            detay_soup = BeautifulSoup(r1.content, "lxml")

            fiyat = ""
            fotolink = ""
            marka = ""
            model = ""
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
            site = "Vatan Bilgisayar"
            links = tamlink
            urunobj["link"]= links

            pricebox = detay_soup.find("div", attrs={"class": "product-list__content product-detail-big-price"})
            price = pricebox.find("span",attrs={"class":"product-list__price"})
            fiyat = price.text
            urunobj["fiyat"] = fiyat

            fotolinkbox = detay_soup.find("div", attrs={"class": "swiper-wrapper"})
            fotolink = fotolinkbox.a.get("href")
            urunobj["fotolink"] = fotolink

            try:
                st1 = detay_soup.find("div", attrs={"class": "wrapper-score clearfix"})
                puant = st1.find("strong", attrs={"id": "averageRankNum"})
                puan = puant.text
                urunobj["puan"] = puan
            except:
                puan = "Değerlendirme yok"
                urunobj["puan"] = puan


            valuetable = detay_soup.find("div", attrs={"id": "urun-ozellikleri"})
            tr = valuetable.find_all("tr", attrs={"data-count": "0"})
            for i in tr:
                ozellik = i.find("td")
                deger = i.find("p")
                # print(tmp.text)
                if ozellik.text == "Ram (Sistem Belleği)":
                    ram = deger.text
                    urunobj["ram"] = ram
                if ozellik.text == "Ekran Boyutu":
                    ekran_boyutu = deger.text
                    urunobj["ekran_boyutu"] = ekran_boyutu
                if ozellik.text == "İşlemci Markası":
                    islemci = deger.text
                    urunobj["islemci"] = islemci
                if ozellik.text == "İşlemci Nesli":
                    islemci_modeli = deger.text
                    urunobj["islemci_modeli"] = islemci_modeli
                if ozellik.text == "İşlemci Hızı":
                    islemci_hizi = deger.text
                    urunobj["islemci_hizi"] = islemci_hizi
                if ozellik.text == "Ekran Kartı Chipseti":
                    ekran_karti = deger.text
                    urunobj["ekran_karti"] = ekran_karti
                if ozellik.text == "İşletim Sistemi":
                    isletim_sistemi = deger.text.strip()
                    if isletim_sistemi == "FreeDOS" or isletim_sistemi == "Free Dos":
                        isletim_sistemi = "Freedos"
                    urunobj["isletim_sistemi"] = isletim_sistemi
                if ozellik.text == "Disk Türü":
                    disk_turu = deger.text
                    urunobj["disk_turu"] = disk_turu
                if ozellik.text == "Disk Kapasitesi":
                    disk_boyutu = deger.text
                    urunobj["disk_boyutu"] = disk_boyutu

            try:
                markabox = detay_soup.find("span",attrs={"style": ["font-size:20px;", "font-size:22px;", "font-size:26px;","font-size:20px"]})
                markanote = markabox.text
                # print(markanote)
                if "NOTEBOOK" in markanote:
                    markanote = markanote.replace('NOTEBOOK', '')
                # print(markanote)
                marka = markanote.split()[0]
                urunobj["marka"] = marka
                model = ' '.join(markanote.split()[1:])
                urunobj["model"] = model
            except:
                print(tamlink)

            # filter = {'marka': marka, 'model': model}
            # # filterprice = {"fiyat": {}}
            # count = vatan_collection.count_documents(filter=filter)
            # print(count)
            # if count < 1:
            vatan_collection.insert_one(urunobj)
            #     print("eklendi")
            # else:
            #     print("zaten var")
            #     count = vatan_collection.count_documents(filter=filter)
            #     new_values = {"$set": {'fiyat': fiyat}}
            #     vatan_collection.update_one(filter, new_values, upsert=True)


        numberofpages = numberofpages + 1

    print(vatan_collection.distinct("isletim_sistemi"))
