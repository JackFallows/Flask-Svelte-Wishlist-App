const express = require("express");
const { createServer } = require('node:http');
const { Server } = require("socket.io");

const app = express();

const cors_origin = process.env.CORS_ORIGIN
    ? [...process.env.CORS_ORIGIN.split(",")]
    : "https://127.0.0.1:5000";

const server = createServer(app);
const io = new Server(server, {
    cors: {
        origin: cors_origin
    }
});

app.get('/', (req, res) => {
    res.send('<h1>Hello world</h1>');
});

io.on('connection', (socket) => {
    console.log('a user connected');
    socket.emit('connected');

    socket.onAny((event_name, ...args) => {
        if (event_name.startsWith('join:')) {
            const room = event_name.slice(event_name.indexOf(':') + 1);
            socket.join(room);
        }
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

io.of("/").adapter.on('join-room', (room, id) => {
    if (room !== id) {
        io.to(room).emit('user-joined');
    }
});

io.of("/").adapter.on('leave-room', (room, id) => {
    if (room !== id) {
        io.to(room).emit('user-left');
    }
});

server.listen(process.env.PORT);