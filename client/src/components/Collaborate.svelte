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

    let title: string;

    $: title = !connected ? "Live updates are currently unavailable" :  active_users === 1
        ? "You are currently the only person viewing this page"
        : active_users === 2
            ? "You and 1 other person are currently viewing this page"
            : `You and ${active_users - 1} other people are currently viewing this page`;

    join(room);

    if (!hidden) {
        respond("user-joined", (data: { clients: number }) => {
            active_users = data.clients;
        });
        respond("user-left", (data: { clients: number }) => {
            active_users = data.clients;
        });
        respond("disconnect", () => {
            connected = false;
        });
        respond("connected", () => {
            connected = true;
        });
    }
</script>

{#if !hidden}
<div title={title}>
    {#if connected}
        <Badge color={BadgeColor.GREEN}>
            <span class="fa-solid fa-users"></span>
            {active_users}
        </Badge>
    {:else}
        <Badge color={BadgeColor.YELLOW}>
            <span class="fa-solid fa-triangle-exclamation"></span>
        </Badge>
    {/if}
</div>
{/if}
