<script lang="ts">
    import io from 'socket.io-client';

    const socket = io(window.notifications_api_url);

    socket.on('my response', msg => {
        console.log('Received: ', msg);
    });
</script>

<slot></slot>
