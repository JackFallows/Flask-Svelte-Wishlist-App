<script lang="ts">
    import io from 'socket.io-client';

    const socket = io();

    socket.on('my response', msg => {
        console.log('Received: ', msg);
    });
</script>

<slot></slot>
