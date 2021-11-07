const fcm_server_key = "AAAAe45dE0A:APA91bGORvFMrpr7nt9tiB5lh34zbFvaGtOB7JsRi5R8YnRtmg-fKmuZRoOaTPUAaVFsV0CgHSokT4TUG8-0CSm5IY8IpyViOAi5avH-I4f-krt4fb1M6XfxUR4bLhaTaATLfeWMT73E";
const FCM = require('fcm-node');
var fcm = new FCM(fcm_server_key);
sendNotification()

function sendNotification() {
    var message = { //this may vary according to the message type (single recipient, multicast, topic, et cetera)
        to: 'f0cZmO4YRyStF_oJFgDhZK:APA91bGrhwKYn07S1D4xc_lDdM_A2Y2q3cWIZGRQcizsH4aIkf6oG_1kmw9aFblu5kgPhqJuaSTjoHJRKZqWlyVZnyPmeMOzA5vpNUxbZto88A281QJoEgTsnqMU1oeADJQLj_Pgr6ZZ',

        data: { //you can send only notification or only data(or include both)
            title: "New Message",
            text: "Please wait while we turn on the hotspot",
            postId: "postId",
            type: "checkMac",
            redirectPage: "FARMGATE"
        }
    };

    fcm.send(message, function(err, response) {
        console.log("sending it now");
        if (err) {
            console.log(err)
            console.log("Something has gone wrong!");
        } else {
            console.log("Successfully sent with response: ", response);
        }
    });
}

async function sendNotificationWithData(token, title, text, postId) {
    return new Promise(async(resolve, reject) => {
        console.log("called");
        var type = await getType(postId);
        var message = {
            to: token,
            data: {
                title: title,
                text: text,
                postId: postId,
                type: type,
                redirectPage: "FARMGATE"
            }
        };
        console.log(message)

        fcm.send(message, function(err, response) {
            console.log("sending it now");
            if (err) {
                console.log(err)
                console.log("Something has gone wrong!");
                resolve(false)
            } else {
                createNotification({
                    uid: userData.userId,
                    title: "New message",
                    text: message,
                    type: type,
                    data: {}
                }).then(data => {
                    console.log("Added to notification")
                    resolve(true);
                })
                console.log("Successfully sent with response: ", response);
            }
        });
    })
}

async function getType(postId) {
    return new Promise((resolve, reject) => {
        mandi.find({ postId: postId }).then(mandiResult => {
            if (mandiResult.length != 0) {
                resolve("mandi")
            } else {
                crops.find({ cropId: postId }).then(cropResult => {
                    if (cropResult.length != 0) {
                        resolve("crop")
                    } else {
                        traderPosts.find({ postId: postId }).then(traderResult => {
                            if (traderResult.length != 0) {
                                resolve("trader")
                            } else {
                                resolve("none")
                            }
                        })
                    }
                })
            }
        })
    })
}

module.exports = {
    sendNotification: sendNotification,
    sendNotificationWithData: sendNotificationWithData,
};