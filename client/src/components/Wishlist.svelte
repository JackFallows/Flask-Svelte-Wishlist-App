<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher } from 'svelte';
    import { Delete, Patch } from '../http';
    import { Views, Api } from '../routes';
    import Modal from './Modal.svelte';

    export let wishlist: IWishlist;
    export let is_third_party: boolean = false; // someone shared it with us

    let delete_modal: Modal;
    let share_modal: Modal;

    let share_email: string;

    const dispatch = createEventDispatcher();

    async function share_wishlist() {
        const confirmed = await share_modal.show();
        if (!confirmed) {
            return;
        }

        await Patch(Api.Wishlists.PatchShare, {
            wishlist_id: wishlist.id,
            email: share_email
        });

        share_email = "";

        dispatch('shared');
    }

    async function delete_wishlist() {
        const confirmed = await delete_modal.show();
        if (!confirmed) {
            return;
        }

        await Delete(Api.Wishlists.Delete.append(wishlist.id), null);

        dispatch('delete');
    }
</script>

<div class="flex flex-nowrap space-x-3" style="width: 100%" id="wishlist-{wishlist.id}">
    <button class="button grow" on:click={() => location.href = Views.Wishlist.View.append(wishlist.id).to_string()}>
        <h2>{wishlist.name}</h2>
    </button>
    {#if !is_third_party}
    <button class="icon-button" aria-label="Share button" on:click={share_wishlist}>
        <span class="fa-solid fa-share-nodes"></span>
    </button>
    <button class="icon-button" aria-label="Delete button" on:click={delete_wishlist}>
        <span class="fa-solid fa-trash" style="pointer-events: none;"></span>
    </button>
    {/if}
</div>


<Modal bind:this={delete_modal} id="delete-{wishlist.id}" is_danger={true}>
    <span slot="header">
        Are you sure?
    </span>
    <span slot="body">
        This action cannot be undone.
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="danger-button" on:click={() => close("true")}>Delete</button>
    </span>
</Modal>

<Modal bind:this={share_modal} id="share-{wishlist.id}">
    <span slot="header">
        Share wishlist '{wishlist.name}'
    </span>
    <span slot="body">
        Enter the email address of the user you want to share this wishlist with:
        <input type="email" class="form-control" bind:value={share_email} />
    </span>
</Modal>

<style lang="less">
    
</style>
