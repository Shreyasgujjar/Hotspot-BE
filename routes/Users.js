const express = require("express")
const router = express.Router()

const users = require("../models/users");

router.post("/", (req, res) => {
    console.log("Creating user");
    users.create(req.body).then(result => {
        res.status(200).jsom({
            message: "Created successfully",
            status: "SUCCESS"
        })
    }).catch(error => {
        console.log(error);
        res.status(500).json({
            message: "There was an error creating the user",
            status: "FAILURE"
        })
    })
})

router.post("/login", (req, res) => {
    console.log("Authenticating the user");
    users.find(req.body).then(result => {
        if(result.length > 0){
            res.status(200).json({
                message: "Logged in successfully",
                status: "SUCCESS"
            })
        } else {
            res.status(400).json({
                message: "The username or password is in correct",
                status: "FAILURE"
            })
        }
    })
})

module.exports = router;