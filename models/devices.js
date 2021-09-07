const mongoose = require('mongoose');

const DevicesSchema = new mongoose.Schema({
    mainDeviceId: {
        type: String,
        required: true
    },
    deviceIp: {
        type: String,
    },
    deviceMac: {
        type: String,
    },
    authorised: {
        type: Boolean,
        required: true
    },
    dataBytesIn: {
        type: Number
    },
    dataBytesOut: {
        type: Number
    },
    customName: {
        type: String,
        default: null
    }
}, {
    timestamps: true
})

module.exports = mongoose.model("device", DevicesSchema);