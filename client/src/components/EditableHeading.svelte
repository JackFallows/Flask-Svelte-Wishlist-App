<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let tag: string;
    export let value: string;
    export let classes: string = "";

    let dispatch = createEventDispatcher();

    let is_editing: boolean = false;

    function save() {
        dispatch("save");
        is_editing = false;
    }
</script>

{#if !is_editing}
    <svelte:element this={tag} class="flex items-center transition-all rounded hover:shadow-[0_0_10px_rgba(0,0,0,0.3)] {classes}">
        <span class="grow">{value}</span>
        <button class="icon-button" on:click={() => is_editing = true}><span class="fa-solid fa-pencil"></span></button>
    </svelte:element>
{:else}
    <div class="flex items-center">
        <input class="text-input grow" type="text" bind:value={value} />
        <button class="icon-button" on:click={save}><span class="fa-solid fa-floppy-disk"></span></button>
    </div>
{/if}

