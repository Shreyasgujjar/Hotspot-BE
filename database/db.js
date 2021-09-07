const mongoose = require('mongoose');
const metaData = require('../metadata/config');
const db = metaData.dbUrl;


const connectDB = async() => {
    try {
        await mongoose.connect(db, { useNewUrlParser: true, useFindAndModify: false, useUnifiedTopology: true });
        console.log("MongoDB is Connected...");
    } catch (err) {
        console.error(err.message);
        process.exit(1);
    }
};

module.exports = connectDB;