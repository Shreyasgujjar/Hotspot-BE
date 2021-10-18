const mongoose = require('mongoose');

const DevicesSchema = new mongoose.Schema({
    mainDeviceId: {
        type: String,
        required: true
    },
    pushToken: {
        type: String
    }
}, {
    timestamps: true
})

module.exports = mongoose.model("deviceToken", DevicesSchema);