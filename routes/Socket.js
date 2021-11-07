const server = require('http').createServer();
const io = require('socket.io')(server);

io.on('connection', client => {
    console.log(client.id);
    client.on('incommingMessage', (data) => {
        console.log(data);
    })
    client.on('disconnect', () => {
        console.log('user disconnected');
    });
});

module.exports = {
    io: io,
    server: server
}