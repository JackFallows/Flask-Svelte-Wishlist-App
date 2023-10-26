<script lang="ts">
    import { getContext } from "svelte";
    import MenuButton from "./MenuButton.svelte";

    export let id: string;
    export let icon: string;
    export let label: string;
    export let expand_in_burger_menu: boolean = !!getContext('burger');
    export let button: HTMLButtonElement = null;
</script>

{#if expand_in_burger_menu}
    <div class="inline sm:hidden">
        <MenuButton id={id} label={label} icon={icon} on:click />
    </div>
    <div class="hidden sm:inline">
        <button class="icon-button" id={id} title="{label}" bind:this={button} on:click>
            <span class="fa-fw {icon} pointer-events-none"></span>
        </button>
        <label for={id} class="sr-only">
            {label}
        </label>
    </div>
{:else}
    <button class="icon-button" id={id} title="{label}" bind:this={button} on:click>
        <span class="fa-fw {icon} pointer-events-none"></span>
    </button>
    <label for={id} class="sr-only">
        {label}
    </label>
{/if}
