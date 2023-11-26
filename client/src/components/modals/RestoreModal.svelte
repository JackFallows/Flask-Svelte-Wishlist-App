<script lang="ts">
    import Modal from "../Modal.svelte";
    import RichText from "../RichText.svelte";

    let modal: Modal;

    let item_to_restore: string;

    export function show(item_name: string): Promise<string> {
        item_to_restore = item_name;
        return modal.show();
    }

</script>

<Modal bind:this={modal} id="retore-modal">
    <span slot="header">
        Restore item?
    </span>
    <span slot="body">
        <p>
            Are you sure you want to restore the following item?
        </p>
        
        {#if item_to_restore}
            <RichText text={item_to_restore} />
        {/if}
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="button" on:click={() => close("true")}>Yes</button>
    </span>
</Modal>
