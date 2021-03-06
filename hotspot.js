require("dotenv").config();
const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
var cors = require("cors");

const connectDb = require("./database/db");
const notificationService = require('./helpers/notificationService');

const app = express();
const port = process.env.PORT || 3010;

const devices = require("./routes/Devices");
const users = require("./routes/Users");
const { server } = require("./routes/Socket");

connectDb();
app.use(express.static(__dirname, { dotfiles: 'allow' }));
app.use(express.json({ extended: true }));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ limit: "50mb", extended: true }));
app.use(cors({ origin: true, credentials: true }));
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    next();
});

app.use("/hotspotapi/device", devices.router);
app.use("/hotspotapi/users", users);

app.get("/hotspotapi/", (req, res) => {
    res.status(200).json({
        message: "Yayyy ! I am working"
    })
})


app.listen(port, () => console.log("app running at - " + port))
server.listen(3020 + 1, () => console.log("socket running at - " + (3010 + 1)))