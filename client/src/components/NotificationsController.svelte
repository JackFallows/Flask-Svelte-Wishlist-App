<script lang="ts">
    import io from 'socket.io-client';
    import { setContext } from 'svelte';

    const socket = io(window.notifications_api_url);

    let current_room: string = null;

    socket.on('connected', () => {
        console.log('Connected');

        if (current_room) {
            socket.emit(`join:${current_room}`);
        }
    });

    setContext('join', (room: string) => {
        current_room = room;

        socket.emit(`join:${room}`);
    });

    setContext('notify', (event_name: string, data: any) => {
        socket.emit(event_name, data);
    });

    setContext('respond', (to: string, with_callback: (data: any) => void) => {
        socket.on(to, with_callback);
    });
</script>

<slot></slot>
