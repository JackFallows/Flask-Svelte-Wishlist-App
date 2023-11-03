<script lang="ts">
    import Modal from "../Modal.svelte";

    export let is_owner: boolean;

    let modal: Modal;

    let defer_bought: boolean;
    let defer_until: string;

    const min_date: string = (new Date()).toISOString().split('T')[0];

    export async function show(): Promise<string | boolean> {
        const result = await modal.show();

        console.log(defer_until);

        if (!result) {
            return false;
        }

        if (defer_bought) {
            return defer_until;
        }

        return true;
    }
</script>

<Modal bind:this={modal} id="bought-modal">
    <span slot="header">
        Have you bought this item?
    </span>
    <span slot="body">
        <p>If you have bought this item, click Yes below and it will be removed from the list.</p>
        {#if !is_owner}
            <div class="mt-3">
                <label>
                    <input type="checkbox" id="defer-bought-checkbox" name="defer_bought_checkbox" bind:checked={defer_bought} />
                    Don't let the wishlist owner know until...
                </label>
                {#if defer_bought}
                    <input type="date" min={min_date} bind:value={defer_until} />
                {/if}
            </div>
        {/if}
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="button" on:click={() => close("true")}>Yes</button>
    </span>
</Modal>
