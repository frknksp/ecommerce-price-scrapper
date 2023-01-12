const mongoose = require("mongoose")

const schema = {
    _id: mongoose.Schema.Types.ObjectId,
    marka: {
        type: String,
        required: true,
    },
    model: {
        type: String,
        required: true,
    },
    fiyat: {
        type: String,
        required: true,
    },
    fotolink: {
        type: String,
        required: true,
    },
    isletim_sistemi: {
        type: String,
        required: true,
    },
    islemci: {
        type: String,
        required: true,
    },
    islemci_modeli: {
        type: String,
        required: true,
    },
    islemci_hizi: {
        type: String,
        required: true,
    },
    ram: {
        type: String,
        required: true,
    },
    disk_boyutu: {
        type: String,
        required: true,
    },
    disk_turu: {
        type: String,
        required: true,
    },
    ekran_boyutu: {
        type: String,
        required: true,
    },
    ekran_karti: {
        type: String,
        required: true,
    },
    puan: {
        type: String,
        required: true,
    },
    site: {
        type: String,
        required: true,
    },
    link: {
        type: String,
        required: true,
    },
}

const mongooseSchema = mongoose.Schema(schema)

module.exports = {
    hepsiburada: mongoose.model("hepsiburada", mongooseSchema),
    n11: mongoose.model("n11", mongooseSchema),
    trendyol: mongoose.model("trendyol", mongooseSchema),
    vatan: mongoose.model("vatan", mongooseSchema),
}