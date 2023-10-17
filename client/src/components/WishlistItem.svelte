<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher } from 'svelte';
    import { Get, Patch } from '../http';
    import { makeRoutes } from '../routes';
    import Modal from './Modal.svelte';
    import RadioList from './RadioList.svelte';

    export let wishlist_item: IWishlistItem;
    export let is_edit: boolean = false;
    export let is_owned: boolean = false;
    export let share_guid: string = null;
    export let has_other_wishlists: boolean = false;

    const { Api } = makeRoutes(window.base_path);
    
    const dispatch = createEventDispatcher();

    const html_id = `wishlist-item-${wishlist_item.id ?? "new"}`
    
    let link: string = wishlist_item.link;
    let notes: string = wishlist_item.notes;
    let bought: boolean = wishlist_item.bought;
    let move_item_modal: Modal;
    let target_wishlist: IWishlist = null;

    $: {
        wishlist_item.link = link;
        wishlist_item.notes = notes;
        wishlist_item.bought = bought;
    }

    async function get_all_wishlists(): Promise<IWishlist[]> {
        const payload = await Get<IWishlist[]>(Api.Wishlists.GetAllForUser);

        let wishlists = payload.get_json();

        if (wishlist_item.wishlist_id != null) {
            wishlists = wishlists.filter(w => w.id != wishlist_item.wishlist_id);
        }

        return wishlists;
    }

    async function mark_as_bought() {
        if (share_guid != null) {
            await Patch(Api.WishlistItems.PatchLinkShareMarkBought.append(share_guid).append(wishlist_item.id), null);
        } else {
            await Patch(Api.WishlistItems.PatchMarkAsBought.append(wishlist_item.id), null);
        }

        dispatch('bought');
    }

    async function move_item_to_list() {
        const confirmed = await move_item_modal.show();

        if (!confirmed) {
            return;
        }

        await Patch(Api.WishlistItems.PatchReparent.append(wishlist_item.id).append(target_wishlist.id), {});

        dispatch('moved', wishlist_item);

        // const item_index = wishlist_items.indexOf(item);
        // if (item_index === -1) {
        //     return;
        // }

        // wishlist_items.splice(item_index, 1);
        // wishlist_items = wishlist_items; // trigger reactivity
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
        <div class="">

            <button class="icon-button" on:click={() => dispatch('delete', wishlist_item)}>
                <span class="fa-solid fa-trash pointer-events-none"></span>
            </button>
        </div>
    </div>
    {:else}
    <div class="flex items-center space-x-3">
        <div class="grow">
            <a class="text-lg text-black" href="{link}">{link}</a>
            <div>
                {notes}
            </div>
        </div>
        <div class="text-base text-slate-600">
            {#if has_other_wishlists && is_owned}
            <button class="icon-button" on:click={() => move_item_to_list()}>
                <span class="fa-solid fa-arrow-right-from-bracket"></span>
            </button>
            {/if}
            <button class="icon-button" on:click={mark_as_bought}>
                <span class="fa-solid fa-basket-shopping pointer-events-none"></span>
            </button>
        </div>
    </div>
    {/if}
</div>

<Modal bind:this={move_item_modal} id="move">
    <span slot="header">
        Move item
    </span>
    <span slot="body">
        {#await get_all_wishlists()}
            Loading...
        {:then wishlists} 
            <p>Choose the wishlist to move this item to:</p>
            <RadioList group_id="wishlists_group" items={wishlists} bind:selected_item={target_wishlist}></RadioList>
        {/await}
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="button" on:click={() => close("true")}>Move item</button>
    </span>
</Modal>

<style lang="less">
</style>
