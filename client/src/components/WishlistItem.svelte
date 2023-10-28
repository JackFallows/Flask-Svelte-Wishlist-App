<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher } from 'svelte';
    import { Get } from '../http';
    import { makeRoutes } from '../routes';
    import Modal from './Modal.svelte';
    import RadioGroup from './RadioGroup.svelte';
    import Collapse from './Collapse.svelte';
    import BurgerMenu from './BurgerMenu.svelte';
    import IconButton from './IconButton.svelte';

    export let wishlist_item: IWishlistItem;
    export let is_owned: boolean = false;
    export let has_other_wishlists: boolean = false;

    const { Api } = makeRoutes(window.base_path);
    
    const dispatch = createEventDispatcher();

    const html_id = `wishlist-item-${wishlist_item.id ?? "new"}`
    
    let link: string = wishlist_item.link;
    let notes: string = wishlist_item.notes;
    let bought: boolean = wishlist_item.bought;
    let is_new: boolean = wishlist_item.id == null;

    let is_editing: boolean = is_new;

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

        dispatch('buy', {
            item: wishlist_item
        });
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
        if (wishlist_item.id != null){
            const confirmed = await confirm_delete_modal.show();

            if (!confirmed) {
                return;
            }
        }

        dispatch('remove', {
            item: wishlist_item
        });
    }

    async function change_text() {
        if (wishlist_item.link == null || wishlist_item.link.trim() == "") {
            return;
        }

        is_editing = false;
        dispatch('change_text', {
            item: wishlist_item
        });
        is_new = false;
    }

    function is_link(link: string): boolean {
        return link.startsWith("http://") || link.startsWith("https://");
    }
</script>

{#if wishlist_item.is_header}
    <div class="flex items-center space-x-3 py-2 border-b-2 border-slate-200">
        <div class="grow">
            {#if is_editing}
                <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Section name" />
            {:else}
                <h2 class="text-xl">{wishlist_item.link}</h2>
            {/if}
        </div>
        {#if is_owned}
            <BurgerMenu id="{wishlist_item.id}-menu" label="Heading menu">
                {#if !is_editing}
                    <IconButton id="{wishlist_item.id}-edit-button" icon="fa-solid fa-pencil" label="Edit" on:click={() => is_editing = true} />
                {:else}
                    <IconButton id="{wishlist_item.id}-save-button" icon="fa-solid fa-floppy-disk" label="Save" on:click={change_text} />
                {/if}
                <IconButton id="{wishlist_item.id}-delete-button" icon="fa-solid fa-trash" label="Delete" on:click={remove} />
            </BurgerMenu>
            <div class="flex flex-col">
                <IconButton id="{wishlist_item.id}-move-up-button" icon="fa-solid fa-arrow-up" label="Move up" on:click={move_up} />
                <IconButton id="{wishlist_item.id}-move-down-button" icon="fa-solid fa-arrow-down" label="Move down" on:click={move_down} />
            </div>
        {/if}
    </div>
{:else}
    <div class="rounded-md bg-slate-200 p-2">
        <div class="flex items-center space-x-3" id="{html_id}">
            {#if is_editing}
                <div class="grow">
                    <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Item link or name" />
                </div>
            {:else}
                <div class="grow">
                    {#if is_link(link)}
                        <span class="text-lg">
                            <a class="text-purple-600 hover:underline" target="_blank" href="{link}">{link}</a>
                            <span class="fa-solid fa-arrow-up-right-from-square"></span>
                        </span>
                    {:else}
                        <span class="text-lg text-black">{link}</span>
                    {/if}
                </div>
            {/if}
            <BurgerMenu id="{wishlist_item.id}-menu" label="Item menu">
                {#if is_owned}
                    {#if has_other_wishlists && !is_editing && !is_new}
                        <IconButton id="{wishlist_item.id}-move-out-button" icon="fa-solid fa-arrow-right-from-bracket" label="Move to list" on:click={move_item_to_list} />
                    {/if}
                {/if}
                {#if !is_new}
                    <IconButton id="{wishlist_item.id}-bought-button" icon="fa-solid fa-basket-shopping" label="Mark as bought" on:click={mark_as_bought} />
                {/if}
                {#if is_owned}
                    {#if !is_editing}
                        <IconButton id="{wishlist_item.id}-edit-button" icon="fa-solid fa-pencil" label="Edit" on:click={() => is_editing = true} />
                    {:else}
                        <IconButton id="{wishlist_item.id}-save-button" icon="fa-solid fa-floppy-disk" label="Save" on:click={change_text} />
                    {/if}
                    <IconButton id="{wishlist_item.id}-delete-button" icon="fa-solid fa-trash" label="Delete" on:click={remove} />
                {/if}
            </BurgerMenu>
            {#if is_owned}
                <div class="flex flex-col">
                    <IconButton id="{wishlist_item.id}-move-up-button" icon="fa-solid fa-arrow-up" label="Move up" on:click={move_up} />
                    <IconButton id="{wishlist_item.id}-move-down-button" icon="fa-solid fa-arrow-down" label="Move down" on:click={move_down} />
                </div>
            {/if}
        </div>
        <div class="mt-2 bg-slate-300 -m-2 rounded-b-md">
            {#if is_editing}
                <Collapse heading="Description" subtle collapsed>
                    <textarea class="text-input grow" bind:value={notes} id="{html_id + "-notes"}" placeholder="Enter additional information about this item here..."></textarea>
                </Collapse>
            {:else}
                {#if notes?.trim().length > 0}
                    <Collapse heading="Description" subtle collapsed>
                        <div class="text-sm">
                            {notes}
                        </div>
                    </Collapse>
                {/if}
            {/if}
        </div>
    </div>
{/if}

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

{#if is_owned}
    <Modal bind:this={move_item_modal} id="move">
        <span slot="header">
            Move item
        </span>
        <span slot="body">
            {#await get_all_wishlists()}
                Loading...
            {:then wishlists} 
                <p>Choose the wishlist to move this item to:</p>
                <RadioGroup group_id="{"wishlists_group_" + wishlist_item.id}" items={wishlists} bind:selected_item={target_wishlist}></RadioGroup>
            {/await}
        </span>
        <span slot="buttons" let:close_modal={close}>
            <button class="button" on:click={() => close()}>Cancel</button>
            <button class="button" on:click={() => close("true")}>Move item</button>
        </span>
    </Modal>

    <Modal bind:this={confirm_delete_modal} is_danger={true} id="delete">
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
{/if}

<style lang="less">
</style>
