const express = require("express")
const app = express()
const cors = require('cors')
const PORT = process.env.PORT || 3001

const connectDb = require("./config/db")
require("dotenv").config()

connectDb()

app.use(express.json())
app.use(express.urlencoded({ extended: false }))
app.use(cors({ origin: '*' }))

app.get("/", (req, res) => {
    res.status(200)
        .send("<h1>Succesfully connected. List of endpoints => </h1>\n",)
})

app.use("/api/laptop", require("./routes/laptop"))


app.listen(PORT, () => { console.log("App start and listen on " + PORT) })