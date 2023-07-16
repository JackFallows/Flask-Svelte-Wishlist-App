<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { Put } from '../http';
    import { Api } from '../routes';

    export let wishlist_item: IWishlistItem;
    export let is_edit: boolean = false;

    const dispatch = createEventDispatcher();

    const html_id = `wishlist-item-${wishlist_item.id ?? "new"}`
    
    let link: string = wishlist_item.link;
    let notes: string = wishlist_item.notes;
    let bought: boolean = wishlist_item.bought;

    $: {
        wishlist_item.link = link;
        wishlist_item.notes = notes;
        wishlist_item.bought = bought;
    }

    async function mark_as_bought() {
        await Put(Api.WishlistItems.MarkAsBought.append(wishlist_item.id), null);

        dispatch('bought');
    }
</script>

<div class="alert alert-secondary" id="{html_id}">
    {#if is_edit}
    <input class="form-control" bind:value={link} id="{html_id + "-link"}" placeholder="Item link or name" />
    <textarea class="form-control" bind:value={notes} id="{html_id + "-notes"}" placeholder="Notes"></textarea>
    {:else}
    <div class="view-container">
        <div class="view-left-column">
            <a href="{link}">{link}</a>
            <div>
                {notes}
            </div>
        </div>
        <div class="view-right-column">
            <button class="btn" on:click={mark_as_bought}>
                <span class="fa-solid fa-bag-shopping" style="pointer-events: none"></span>
            </button>
        </div>
    </div>
{/if}
</div>

<style lang="less">
    .view-container {
        display: flex;
        align-items: center;

        .view-left-column {
            flex-grow: 1;
        }

        .view-right-column {
            flex-grow: 0;
        }
    }
</style>
