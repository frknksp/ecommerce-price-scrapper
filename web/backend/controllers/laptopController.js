const {
    n11,
    hepsiburada,
    trendyol,
    vatan
} = require("../models")

const fs = require("fs")

const getAllLaptops = async (req, res) => {
    const hepsiburadalist = await hepsiburada.find()
    const trendyollist = await trendyol.find()
    const n11list = await n11.find()
    const vatanlist = await vatan.find()

    const allLists =
        [
            { "hepsiburada": hepsiburadalist },
            { "trendyol": trendyollist },
            { "n11": n11list },
            { "vatan": vatanlist }
        ]

    const computers = {}

    for (obj of allLists) {
        for (list in obj) {
            for (laptop of obj[list]) {
                if (typeof laptop?.model == "string" && typeof laptop?.marka == "string") {
                    let marka = (laptop?.marka.trim().toLowerCase() || "")
                    let model = (laptop?.model.trim().toLowerCase() || "")
                    if (computers[marka]) {
                        if (computers[marka][model]) {
                            computers[marka][model].amount++
                            computers[marka][model].from.push({ "website": list, "link": laptop?.link || "", "fiyat": laptop?.fiyat.split(",")[0].replaceAll("TL", "").replaceAll(".", "").trim() || "", "fotolink": laptop?.fotolink || "", "puan": laptop?.puan || "", })
                            if (list == "n11") {
                                computers[marka][model].ozellikler =
                                {
                                    "isletim_sistemi": laptop?.isletim_sistemi || "",
                                    "islemci": laptop?.islemci || "",
                                    "islemci_modeli": laptop?.islemci_modeli || "",
                                    "islemci_hizi": laptop?.islemci_hizi || "",
                                    "ram": laptop?.ram || "",
                                    "disk_boyutu": laptop?.disk_boyutu || "",
                                    "disk_turu": laptop?.disk_turu || "",
                                    "ekran_boyutu": laptop?.ekran_boyutu || "",
                                    "ekran_karti": laptop?.ekran_karti || "",
                                }
                            }
                        } else {
                            computers[marka][model] = {}
                            computers[marka][model].amount = 1
                            computers[marka][model].from = [{ "website": list, "link": laptop?.link || "", "fiyat": laptop?.fiyat.split(",")[0].replaceAll("TL", "").replaceAll(".", "").trim() || "", "fotolink": laptop?.fotolink || "", "puan": laptop?.puan || "", }]
                            computers[marka][model].ozellikler =
                            {

                                "isletim_sistemi": laptop?.isletim_sistemi || "",
                                "islemci": laptop?.islemci || "",
                                "islemci_modeli": laptop?.islemci_modeli || "",
                                "islemci_hizi": laptop?.islemci_hizi || "",
                                "ram": laptop?.ram || "",
                                "disk_boyutu": laptop?.disk_boyutu || "",
                                "disk_turu": laptop?.disk_turu || "",
                                "ekran_boyutu": laptop?.ekran_boyutu || "",
                                "ekran_karti": laptop?.ekran_karti || "",
                            }
                        }

                    } else {
                        computers[marka] = {}
                        computers[marka][model] = {}
                        computers[marka][model].amount = 1
                        computers[marka][model].from = [{ "website": list, "link": laptop?.link || "", "fiyat": laptop?.fiyat.split(",")[0].replaceAll("TL", "").replaceAll(".", "").trim() || "", "fotolink": laptop?.fotolink || "", "puan": laptop?.puan || "", }]
                        computers[marka][model].ozellikler =
                        {
                            "isletim_sistemi": laptop?.isletim_sistemi || "",
                            "islemci": laptop?.islemci || "",
                            "islemci_modeli": laptop?.islemci_modeli || "",
                            "islemci_hizi": laptop?.islemci_hizi || "",
                            "ram": laptop?.ram || "",
                            "disk_boyutu": laptop?.disk_boyutu || "",
                            "disk_turu": laptop?.disk_turu || "",
                            "ekran_boyutu": laptop?.ekran_boyutu || "",
                            "ekran_karti": laptop?.ekran_karti || "",
                            "puan": laptop?.puan || "",
                            "site": laptop?.site || "",
                            "link": laptop?.link || "",
                        }

                    }
                }
            }
        }
    }
    for (const marka in computers) {
        for (const model in computers[marka]) {

            if (computers[marka][model].amount == 1) {
                delete computers[marka][model]
            }
            else if (computers[marka][model].amount >= 4) {
                delete computers[marka][model]
            }

        }
        if (Object.keys(computers[marka]).length === 0) {
            delete computers[marka]
        }
    }

    // fs.writeFile('laptops.txt', JSON.stringify(computers, null, "\t"), function (err) {
    //     if (err) return console.log(err);
    // });

    res.json(computers)
}

module.exports = {
    getAllLaptops,
}