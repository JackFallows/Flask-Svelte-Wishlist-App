import express from "express";
import { createServer } from 'node:http';
import { Server } from "socket.io";

const app = express();

const server = createServer(app);
const io = new Server(server, {
    cors: {
        origin: process.env.CORS_ORIGIN ?? "https://127.0.0.1:5000"
    }
});

app.get('/', (req, res) => {
    res.send('<h1>Hello world</h1>');
});

io.on('connection', (socket) => {
    console.log('a user connected');
    io.emit('my response');
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

server.listen(process.env.PORT, () => {
    console.log(`server running at http://localhost:${process.env.PORT}`);
});
