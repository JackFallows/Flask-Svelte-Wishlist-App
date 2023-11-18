<script lang="ts">
    import { getContext } from "svelte";
    import Badge from "./Badge.svelte";
    import { BadgeColor } from "../enums";

    export let room: string;
    export let hidden: boolean = false;

    const get_is_connected = <() => boolean>getContext('get_is_connected');
    const join = <Join>getContext('join');
    const respond = <Respond>getContext('respond');

    let active_users: number = 0;
    let connected: boolean = get_is_connected();

    join(room);

    respond("user-joined", (data: { clients: number }) => {
        console.log("user joined wishlist");
        active_users = data.clients;
    });
    respond("user-left", (data: { clients: number }) => {
        console.log("user left wishlist");
        active_users = data.clients;
    });
    respond("disconnect", () => {
        connected = false;
    });
    respond("connected", () => {
        connected = true;
    });
</script>

{#if !hidden}

{#if connected}
    <Badge color={BadgeColor.GREEN}>
        <span class="fa-solid fa-users"></span>
        {active_users}
        <!-- {#if active_users === 1}
            You are currently the only person viewing this page
        {:else}
            {#if (active_users - 1) === 1}
                There is currently 1 other person viewing this page
            {:else}
                There are currently {active_users - 1} other people viewing this page
            {/if}
        {/if} -->
    </Badge>
{:else}
    <Badge color={BadgeColor.YELLOW}>
        <span class="fa-solid fa-triangle-exclamation"></span>
    </Badge>
{/if}

{/if}
