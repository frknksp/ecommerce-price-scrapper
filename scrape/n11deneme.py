from bs4 import BeautifulSoup
import requests
from mongodb import dbconnect

client = dbconnect()
laptops = client.laptops
n11_collection = laptops.n11

n11_collection.delete_many({})

def n11run(headers,totalnumberofpages):
    numberofpages = 1
    while numberofpages < totalnumberofpages:
        print(numberofpages)
        url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar?ipg=5&pg="+str(numberofpages)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content,"lxml")
        st1 = soup.find("div",attrs={"class":"catalogView"})
        st2 = st1.find("ul",attrs={"class":"list-ul"})
        st3 = st2.find_all("li",attrs={"class":"column"})

        for urun in st3:
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
                "site": "N11",
                "link": ""
            }
            fiyat = ""
            # fotolink = ""

            pric = urun.find("ins")
            fiyat = pric.text


            urunobj["fiyat"] = fiyat

            link = urun.a.get("href")
            urunobj["link"] = link
            # print(link)
            r1 = requests.get(link,headers=headers)
            detay_soup = BeautifulSoup(r1.content,"lxml")

            try:
                imgobj = detay_soup.find("div", attrs={"class": "imgObj"})
                imglink = imgobj.a.get("href")
                fotolink = imglink
                urunobj["fotolink"] = fotolink
            except:
                print("hata")

            marka = ""
            model = ""
            # isletim_sistemi = ""
            # islemci = ""
            # islemci_modeli = ""
            # islemci_hizi = ""
            # ram = ""
            # disk_boyutu = ""
            # disk_turu = ""
            # ekran_boyutu = ""
            # ekran_karti = "None"
            # puan = ""
            # site = "N11"
            # links = link

            try:
                abc = detay_soup.find("div", attrs={"class": "avarageText"})
                puan = abc.text
                urunobj["puan"] = puan
            except:
                puan = "Değerlendirme yok"
                urunobj["puan"] = puan

            teknik_ayrintilar = detay_soup.find_all("div",attrs={"class":"unf-prop-context"})
            for teknik in teknik_ayrintilar:
                detaylar = teknik.find_all("li")
                for i in detaylar:
                    ozellik = i.find("p", attrs={"class": "unf-prop-list-title"}).text
                    deger = i.find("p", attrs={"class": "unf-prop-list-prop"}).text
                    if ozellik == "Marka":
                        urunobj["marka"] = deger
                        marka = deger
                    if ozellik == "Model":
                        urunobj["model"] = deger
                        model = deger
                    if ozellik == "İşlemci":
                        urunobj["islemci"] = deger
                        # islemci = deger
                    if ozellik == "İşlemci Hızı":
                        urunobj["islemci_hizi"] = deger
                        # islemci_hizi = deger
                    if ozellik == "Ekran Boyutu":
                        urunobj["ekran_boyutu"] = deger
                        # ekran_boyutu= deger
                    if ozellik == "İşletim Sistemi":
                        urunobj["isletim_sistemi"] = deger.strip()
                        # isletim_sistemi= deger
                    if ozellik == "İşlemci Modeli":
                        urunobj["islemci_modeli"] = deger
                        # islemci_modeli= deger
                    if ozellik == "Ekran Kartı Modeli":
                        urunobj["ekran_karti"] = deger
                        # ekran_karti= deger
                    if ozellik == "Bellek Kapasitesi":
                        urunobj["ram"] = deger
                        # ram = deger
                    if ozellik == "Disk Türü":
                        urunobj["disk_turu"] = deger
                        # disk_turu = deger
                    if ozellik == "Disk Kapasitesi":
                        urunobj["disk_boyutu"] = deger
                        # disk_boyutu = deger

            # filter = {'marka': marka, 'model': model}
            # count = n11_collection.count_documents(filter=filter)
            # print(count)
            # if count < 1:
            n11_collection.insert_one(urunobj)
            #     print("eklendi")
            # else:
            #     print("zaten var")
            #     count = n11_collection.count_documents(filter=filter)
            #     new_values = {"$set": {'fiyat': fiyat}}
            #     n11_collection.update_one(filter, new_values, upsert=True)


        numberofpages = numberofpages + 1

    print(n11_collection.distinct("isletim_sistemi"))

