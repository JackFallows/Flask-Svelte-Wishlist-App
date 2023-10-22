<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher } from 'svelte';
    import { Get, Patch } from '../http';
    import { makeRoutes } from '../routes';
    import Modal from './Modal.svelte';
    import RadioList from './RadioList.svelte';
    import Collapse from './Collapse.svelte';

    export let wishlist_item: IWishlistItem;
    export let is_owned: boolean = false;
    export let share_guid: string = null;
    export let has_other_wishlists: boolean = false;

    const { Api } = makeRoutes(window.base_path);
    
    const dispatch = createEventDispatcher();

    const html_id = `wishlist-item-${wishlist_item.id ?? "new"}`
    
    let link: string = wishlist_item.link;
    let notes: string = wishlist_item.notes;
    let bought: boolean = wishlist_item.bought;

    let is_editing: boolean = false;

    let move_item_modal: Modal;
    let target_wishlist: IWishlist = null;
    let bought_confirmation_modal: Modal;
    let confirm_delete_modal: Modal;

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
        const confirmed = await bought_confirmation_modal.show();

        if (!confirmed) {
            return;
        }

        if (share_guid != null) {
            await Patch(Api.WishlistItems.PatchLinkShareMarkBought.append(share_guid).append(wishlist_item.id), null);
        } else {
            await Patch(Api.WishlistItems.PatchMarkAsBought.append(wishlist_item.id), null);
        }

        dispatch('bought', wishlist_item);
    }

    async function move_item_to_list() {
        const confirmed = await move_item_modal.show();

        if (!confirmed) {
            return;
        }

        dispatch('move_out', {
            item: wishlist_item,
            target_wishlist_id: target_wishlist.id
        });
    }

    function move_up() {
        dispatch('move_up', {
            item: wishlist_item
        });
    }

    function move_down() {
        dispatch('move_down', {
            item: wishlist_item
        });
    }

    async function remove() {
        const confirmed = await confirm_delete_modal.show();

        if (!confirmed) {
            return;
        }

        dispatch('remove', {
            item: wishlist_item
        });
    }

    function is_link(link: string): boolean {
        return link.startsWith("http://") || link.startsWith("https://");
    }
</script>

{#if wishlist_item.is_header}
    <div class="flex items-center space-x-3 p-2 border-b-2 border-slate-200">
        <div class="grow">
            {#if is_editing}
                <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Section name" />
            {:else}
                <h2 class="text-xl">{wishlist_item.link}</h2>
            {/if}
        </div>
        <div class="flex items-center">
            {#if is_owned}
                {#if !is_editing}
                    <button class="icon-button" on:click={() => is_editing = true}>
                        <span class="fa-solid fa-pencil"></span>
                    </button>
                {:else}
                    <button class="icon-button" on:click={() => is_editing = false}>
                        <span class="fa-solid fa-floppy-disk"></span>
                    </button>
                {/if}
                <div class="flex flex-col">
                    <button class="icon-button" on:click={move_up}><span class="fa-solid fa-arrow-up"></span></button>
                    <button class="icon-button" on:click={move_down}><span class="fa-solid fa-arrow-down"></span></button>
                </div>
                <button class="icon-button" on:click={remove}>
                    <span class="fa-solid fa-trash pointer-events-none"></span>
                </button>
            {/if}
        </div>
    </div>
{:else}
    <div class="rounded-md bg-slate-200 p-2" id="{html_id}">
        {#if is_editing}
        <div class="flex items-center space-x-3">
            <div class="grow">
                <div class="flex items-start space-y-3 flex-col">
                    <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Item link or name" />
                    <Collapse heading="Description" subtle collapsed>
                        <textarea class="text-input grow" bind:value={notes} id="{html_id + "-notes"}" placeholder="Enter additional information about this item here..."></textarea>
                    </Collapse>
                </div>
            </div>
            <div class="flex items-center">
                <div class="flex flex-col">
                    <button class="icon-button" on:click={move_up}><span class="fa-solid fa-arrow-up"></span></button>
                    <button class="icon-button" on:click={move_down}><span class="fa-solid fa-arrow-down"></span></button>
                </div>
                <button class="icon-button" on:click={() => dispatch('delete', wishlist_item)}>
                    <span class="fa-solid fa-trash pointer-events-none"></span>
                </button>
            </div>
        </div>
        {:else}
        <div class="flex items-center space-x-3">
            <div class="grow">
                {#if is_link(link)}
                <span class="text-lg">
                    <a class="text-purple-600 hover:underline" target="_blank" href="{link}">{link}</a>
                    <span class="fa-solid fa-arrow-up-right-from-square"></span>
                </span>
                {:else}
                <span class="text-lg text-black">{link}</span>
                {/if}
                {#if notes?.trim().length > 0}
                <div class="mt-2">
                    <Collapse heading="Description" subtle collapsed>
                        <div class="text-sm">
                            {notes}
                        </div>
                    </Collapse>
                </div>
                {/if}
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
{/if}

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

<Modal bind:this={bought_confirmation_modal} id="bought-modal">
    <span slot="header">
        Have you bought this item?
    </span>
    <span slot="body">
        If you have bought this item, click Yes below and it will be removed from the list.
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="button" on:click={() => close("true")}>Yes</button>
    </span>
</Modal>

<Modal bind:this={confirm_delete_modal} is_danger={true} id="delete">
    <span slot="header">
        Are you sure?
    </span>
    <span slot="body">
        Once the wishlist is saved, this action cannot be undone.
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="danger-button" on:click={() => close("true")}>Delete</button>
    </span>
</Modal>

<style lang="less">
</style>
