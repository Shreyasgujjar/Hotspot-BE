const express = require("express");
const { sendNotificationWithData } = require("../helpers/notificationService");
const router = express.Router()

const devices = require("../models/devices");
const deviceTokens = require("../models/deviceTokens");

const { io } = require('./Socket');

router.post("/checkandcreate", (req, res) => {
    devices.find({ mainDeviceId: req.body.mainDeviceId, deviceMac: req.body.deviceMac }).then(result => {
        if (result.length == 0) {
            devices.create({
                mainDeviceId: req.body.mainDeviceId,
                deviceIp: req.body.deviceIp,
                deviceMac: req.body.deviceMac,
                authorised: false,
                dataBytesIn: 0,
                dataBytesOut: 0
            }).then(creationResult => {
                res.status(200).json({
                    message: "Device created successully",
                    status: "SUCCESS"
                })
            }).catch(error => {
                console.log(error);
                res.status(500).json({
                    message: "There was an error creating the device",
                    status: "FAILURE"
                })
            })
            return;
        } else {
            devices.findOneAndUpdate({ mainDeviceId: req.body.mainDeviceId, deviceMac: req.body.deviceMac }, {deviceIp: req.body.deviceIp}).then(result => {
                res.status(200).json({
                    message: "Device added successfully",
                    status: "SUCCESS"
                })
            }).catch(error => {
                console.log(error);
                res.status(500).json({
                    message: "There was an error creating the device",
                    status: "FAILURE"
                })
            })
        }
        checkAndAuthoriseTheNewDevices(req);
        res.status(200).json({
            message: "This device already exists",
            status: "SUCCESS"
        })
    })
})

router.get("/getall/:mainDeviceId/:deviceIp", (req, res) => {
    devices.find({ mainDeviceId: req.params.mainDeviceId, deviceIp: req.params.deviceIp }).then(result => {
        res.status(200).json({
            message: "Data retrived successfully",
            status: "SUCCESS",
            data: result
        })
    }).catch(error => {
        console.log(error);
        res.status(500).json({
            message: "There was an error retriving the data",
            status: "FAILURE"
        })
    })
})

router.get("/getalldetails", (req, res) => {
    var mainDeviceId = []
    var replyList = []
    devices.find().then(result => {
        result.forEach(item => {
            mainDeviceId.push(item.mainDeviceId)
        })
        mainDeviceId = Array.from(new Set(mainDeviceId));
        for (var item of mainDeviceId) {
            var subList = []
            var customName = null;
            result.forEach(data => {
                if (data.mainDeviceId == item) {
                    if (data.customName != null || data.customName != undefined) {
                        if (customName == null) {
                            customName = data.customName
                        }
                    }
                    subList.push({
                        deviceIp: data.deviceIp,
                        authorised: data.authorised,
                        dataBytesIn: data.dataBytesIn,
                        dataBytesOut: data.dataBytesOut
                    })
                }
            })
            replyList.push({
                customName: customName,
                mainDeviceId: item,
                count: subList.length,
                deviceData: subList
            })
        }
        res.status(200).json({
            message: "Data retrived successfully",
            staus: "SUCCESS",
            data: replyList
        })
    }).catch(error => {
        console.log(error);
        res.status(500).json({
            message: "There was a problem retriving the data",
            status: "FAILURE"
        })
    })
})

router.put("/updateAuthStatus", (req, res) => {
    devices.findOne({ mainDeviceId: req.body.mainDeviceId, deviceIp: req.body.deviceIp }).then(result => {
        var authStatus = !result.authorised;
        devices.findOneAndUpdate({ mainDeviceId: req.body.mainDeviceId, deviceIp: req.body.deviceIp }, { authorised: authStatus }).then(data => {
            io.emit(req.body.mainDeviceId, {
                type: 'checkMac'
            })
            deviceTokens.findOne({mainDeviceId: req.body.mainDeviceId}).then(result => {
                sendNotificationWithData(result.pushToken, 'New message', 'Authorised devices changes', 'checkMac');
            })
            res.status(200).json({
                message: "Auth status updated successfully",
                status: "SUCCESS"
            })
        }).catch(error => {
            console.log(error);
            res.status(500).json({
                message: "There was an error updating the status",
                status: "FAILURE"
            })
        })
    }).catch(error => {
        console.log(error);
        res.status(500).json({
            message: "There was an error updating the status",
            status: "FAILURE"
        })
    })
})

router.post("/updateData", (req, res) => {
    devices.findOneAndUpdate({ mainDeviceId: req.body.mainDeviceId, deviceIp: req.body.ip }, { dataBytesIn: req.body.dataIn, dataBytesOut: req.body.dataOut }).then(result => {
        res.status(200).json({
            message: "Updated details successfully",
            status: "SUCCESS"
        })
    }).catch(error => {
        console.log(error)
        res.status(500).json({
            message: "There was an error updating the data",
            status: "FAILURE"
        })
    })
})

router.get("/sendrestarthotspot/:mainDeviceId", (req, res) => {
    io.emit(req.params.mainDeviceId, {
        userName: "Shreyas",
        type: "restartHotspot"
    })
    res.status(200).json({
        message: "RestartedHotspot",
        status: "SUCCESS"
    })
})

router.get('/sendcheckmac/:mainDeviceId', (req, res) => {
    io.emit(req.params.mainDeviceId, {type: "checkMac"})
    res.status(200).json({
        message: "Checking mac",
        status: "SUCCESS"
    })
})

router.post("/addnewmac", (req, res) => {
    devices.find({ mainDeviceId: req.body.mainDeviceId, deviceMac: req.body.deviceMac }).then(data => {
        if(data.length == 0){
            devices.create({
                mainDeviceId: req.body.mainDeviceId,
                deviceMac: req.body.deviceMac,
                authorised: true,
                dataBytesIn: 0,
                dataBytesOut: 0
            }).then(result => {
                res.status(200).json({
                    message: "Added Mac successfully ",
                    status: "SUCCESS"
                })
            })
        } else {
            devices.findOneAndUpdate({ mainDeviceId: req.body.mainDeviceId, deviceMac: req.body.deviceMac }, { authorised: true }).then(devicesData => {
                res.status(200).json({
                    message: "Added Mac successfully ",
                    status: "SUCCESS"
                })
            }).catch(error => {
                console.log(error)
                res.status(500).json({
                    message: "There was an error updating the data",
                    status: "FAILURE"
                })
            })
        }
    })
})

router.post("/sendpushtoken", (req, res) => {
    console.log(req.body);
    deviceTokens.find(req.body).then(result => {
        if (result.length == 0) {
            deviceTokens.create(req.body).then(result => {
                console.log(result);
                console.log("Updated the name successfully");
                res.status(200).json({
                    message: "Updated the name successfully",
                    status: "SUCCESS"
                })
            }).catch(error => {
                console.log(error);
                res.status(500).json({
                    message: "There was an error updating the name",
                    status: "FAILURE"
                })
            })
        } else {
            res.status(200).json({
                message: "Updated the name successfully",
                status: "SUCCESS"
            })
        }
    })
})

router.put("/updatecustomname", (req, res) => {
    console.log("Trying to update the name");
    devices.findOneAndUpdate({ mainDeviceId: req.body.mainDeviceId }, { customName: req.body.customName }).then(result => {
        console.log(result);
        console.log("Updated the name successfully");
        res.status(200).json({
            message: "Updated the name successfully",
            status: "SUCCESS"
        })
    }).catch(error => {
        console.log(error);
        res.status(500).json({
            message: "There was an error updating the name",
            status: "FAILURE"
        })
    })
})

function checkAndAuthoriseTheNewDevices(req) {
    devices.find({ mainDeviceId: req.body.mainDeviceId, deviceMac: req.body.deviceMac }).then(async result => {
        for (var data of result) {
            await authoriseDevice(data._id, data.authorised);
        }
    })
}

async function authoriseDevice(_id, authState) {
    return new Promise((resolve, reject) => {
        devices.findOneAndUpdate({ _id: _id }, { authorised: authState }).then(result => {
            console.log(_id, authState)
            resolve(result);
        })
    })
}

module.exports = {
    router: router
};