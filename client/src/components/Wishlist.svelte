<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { Delete } from '../http';
    import { Views, Api } from '../routes';
    import ConfirmModal from './ConfirmModal.svelte';

    export let wishlist: IWishlist;

    let confirm_modal: ConfirmModal;

    const dispatch = createEventDispatcher();

    async function delete_wishlist() {
        const confirmed = await confirm_modal.show();

        if (!confirmed) {
            return;
        }

        await Delete(Api.Wishlists.Delete.append(wishlist.id), null);

        dispatch('delete');
    }
</script>

<div class="mb-3 btn-group" role="group" style="width: 100%" id="wishlist-{wishlist.id}">
    <button class="btn btn-outline-primary wishlist-button" on:click={() => location.href = Views.Wishlist.View.append(wishlist.id).to_string()}>
        <h2>{wishlist.name}</h2>
    </button>
    <button class="btn btn-outline-danger" on:click={delete_wishlist}>
        <span class="fa-solid fa-trash" style="pointer-events: none;"></span>
    </button>
</div>

<ConfirmModal bind:this={confirm_modal} />

<style lang="less">
    .wishlist-button {
        width: 100%;
    }
</style>
