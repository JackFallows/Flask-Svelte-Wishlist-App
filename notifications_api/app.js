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

const workspaces = io.of(/^\/\w+$/);

workspaces.on('connection', (socket) => {
    const workspace = socket.nsp;

    console.log('a user connected');
    socket.emit('connected');

    socket.onAny((event_name, ...args) => {
        if (event_name.startsWith('join:')) {
            const room = event_name.slice(event_name.indexOf(':') + 1);
            socket.join(room);
        } else if (event_name.startsWith('item:')) {
            const action = event_name.slice(event_name.indexOf(':') + 1);
            const data = args[0];
            socket.to(data.room).emit(action, data);
        }
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    workspace.adapter.on('join-room', (room, id) => {
        if (room !== id) {
            workspace.to(room).emit('user-joined', {
                clients: get_room_clients(workspace, room)
            });
        }
    });

    workspace.adapter.on('leave-room', (room, id) => {
        if (room !== id) {
            workspace.to(room).emit('user-left', {
                clients: get_room_clients(workspace, room)
            });
        }
    });
});

server.listen(process.env.PORT);

function get_room_clients(workspace, room) {
    return workspace.adapter.rooms.get(room).size;
}
