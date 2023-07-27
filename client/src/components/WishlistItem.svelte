<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher } from 'svelte';
    import { Patch } from '../http';
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
        await Patch(Api.WishlistItems.PatchMarkAsBought.append(wishlist_item.id), null);

        dispatch('bought');
    }
</script>

<div class="rounded-md bg-slate-200 p-2" id="{html_id}">
    {#if is_edit}
    <div class="flex items-center space-x-3">
        <div class="grow">
            <div class="flex items-start space-y-3 flex-col lg:flex-row lg:space-y-0 lg:space-x-3">
                <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Item link or name" />
                <textarea class="text-input grow" bind:value={notes} id="{html_id + "-notes"}" placeholder="Notes"></textarea>
            </div>
        </div>
        <div class="view-right-column">
            <button class="icon-button" on:click={() => dispatch('delete', wishlist_item)}>
                <span class="fa-solid fa-trash pointer-events-none"></span>
            </button>
        </div>
    </div>
{:else}
    <div class="view-container">
        <div class="view-left-column">
            <a href="{link}">{link}</a>
            <div>
                {notes}
            </div>
        </div>
        <div class="view-right-column">
            <button class="icon-button" on:click={mark_as_bought}>
                <span class="fa-solid fa-basket-shopping pointer-events-none"></span>
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
