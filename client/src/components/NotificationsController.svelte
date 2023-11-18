<script lang="ts">
    import io from 'socket.io-client';
    import { setContext } from 'svelte';

    const socket = io(window.notifications_api_url);

    let is_connected: boolean = false;
    let current_room: string = null;

    socket.on('connected', () => {
        console.log('Connected');
        is_connected = true;

        if (current_room) {
            socket.emit(`join:${current_room}`);
        }
    });

    socket.on('disconnect', () => {
        is_connected = false;
    });

    setContext('get_is_connected', () => {
        return is_connected;
    });

    setContext('join', (room: string) => {
        current_room = room;

        socket.emit(`join:${room}`);
    });

    setContext('notify', (event_name: string, data: any) => {
        socket.emit(event_name, { room: current_room, ...data });
    });

    setContext('respond', (to: string, with_callback: (data: any) => void) => {
        socket.on(to, with_callback);
    });
</script>

<slot></slot>
