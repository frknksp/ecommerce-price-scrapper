const router = require("express").Router()
const { getAllLaptops } = require("../controllers/laptopController")

router.get("/", getAllLaptops)

module.exports = router