<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import IconButton from "./IconButton.svelte";

    export let tag: string;
    export let value: string;
    export let placeholder: string = "";
    export let classes: string = "";
    export let is_editing: boolean = false;

    let dispatch = createEventDispatcher();

    function save() {
        if (value == null || value.trim() == "") {
            return;
        }

        dispatch("save");
        is_editing = false;
    }
</script>

{#if !is_editing}
    <svelte:element this={tag} class="flex items-center transition-all rounded hover:shadow-[0_0_10px_rgba(0,0,0,0.3)] {classes}">
        <span class="grow">{value}</span>
        <IconButton id="edit-heading-button" icon="fa-solid fa-pencil" label="Edit heading" on:click={() => is_editing = true} />
    </svelte:element>
{:else}
    <div class="flex items-center">
        <input class="text-input grow" type="text" bind:value={value} placeholder="{placeholder}" />
        <IconButton id="save-heading-button" icon="fa-solid fa-check" label="Save heading" on:click={save} />
    </div>
{/if}

