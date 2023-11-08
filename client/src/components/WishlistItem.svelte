<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher, getContext } from 'svelte';
    import { makeRoutes } from '../routes';
    import Modal from './Modal.svelte';
    import BoughtModal from './modals/BoughtModal.svelte';
    import RadioGroup from './RadioGroup.svelte';
    import Collapse from './Collapse.svelte';
    import BurgerMenu from './BurgerMenu.svelte';
    import IconButton from './IconButton.svelte';
    import RichText from './RichText.svelte';
    import SortControl from './SortControl.svelte';

    export let wishlist_item: IWishlistItem;
    export let is_owned: boolean = false;
    export let is_link_share: boolean = false;
    export let has_other_wishlists: boolean = false;
    export let most_recent_bought_item: IBoughtItem = null;

    const { Get } = <IHttp>getContext("http");

    const { Api } = makeRoutes(window.base_path);
    
    const dispatch = createEventDispatcher();

    const html_id = `wishlist-item-${wishlist_item.id ?? "new"}`
    
    let link: string = wishlist_item.link;
    let notes: string = wishlist_item.notes;
    let is_new: boolean = wishlist_item.id == null;
    let has_notes: boolean = false;

    $: has_notes = notes?.trim().length > 0;

    let is_editing: boolean = is_new;

    let move_item_modal: Modal;
    let target_wishlist: IWishlist = null;
    let bought_confirmation_modal: BoughtModal;
    let confirm_delete_modal: Modal;

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
            item: wishlist_item,
            defer_until: typeof(confirmed) == "string" ? confirmed : null
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

    function move_to_top() {
        dispatch("move_to_top", {
            item: wishlist_item
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

    function move_to_bottom() {
        dispatch("move_to_bottom", {
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

    function cancel_change_text() {
        link = wishlist_item.link;
        notes = wishlist_item.notes;
        is_editing = false;
    }

    async function change_text() {
        if (link == null || link.trim() == "") {
            return;
        }

        wishlist_item.link = link;
        wishlist_item.notes = notes;

        is_editing = false;
        dispatch('change_text', {
            item: wishlist_item
        });
        is_new = false;
    }
</script>

<div class="flex space-x-2 items-center">
    {#if wishlist_item.is_header}
        <div class="grow">
            <div class="flex items-center space-x-3 pr-2 mt-3">
                <div class="grow">
                    {#if is_editing}
                        <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Section name" />
                    {:else}
                        <h2 class="text-xl">{wishlist_item.link}</h2>
                    {/if}
                </div>
                {#if is_owned}
                    {#if !is_editing}
                        <BurgerMenu id="{wishlist_item.id}-menu" label="Heading menu">
                            <IconButton id="{wishlist_item.id}-edit-button" icon="fa-solid fa-pencil" label="Edit" on:click={() => is_editing = true} />
                            <div class="sm:hidden">
                                <IconButton id="{html_id}-move-top-button" icon="fa-solid fa-angles-up" label="Move to top" on:click={move_to_top} />
                                <IconButton id="{html_id}-move-bottom-button" icon="fa-solid fa-angles-down" label="Move to bottom" on:click={move_to_bottom} />
                            </div>
                            <IconButton id="{wishlist_item.id}-delete-button" icon="fa-solid fa-trash" label="Delete" on:click={remove} />
                        </BurgerMenu>
                    {:else}
                        <IconButton id="{wishlist_item.id}-save-button" icon="fa-solid fa-check" label="Save" on:click={change_text} />
                        {#if is_new}
                            <IconButton id="{wishlist_item.id}-delete-button" icon="fa-solid fa-trash" label="Delete" on:click={remove} />
                        {:else}
                            <IconButton id="{wishlist_item.id}-cancel-button" icon="fa-solid fa-rotate-left" label="Cancel" on:click={cancel_change_text} />
                        {/if}
                    {/if}
                    <SortControl id={html_id}
                        on:move_up={move_up}
                        on:move_down={move_down}
                    />
                {/if}
            </div>
            <hr class="mt-2" />
        </div>
        {:else}
        <div class="grow rounded-t-md {is_editing || has_notes ? "" : "rounded-b-md"} bg-slate-200 p-2">
            <div class="flex items-center space-x-3" id="{html_id}">
                {#if is_editing}
                    <div class="grow">
                        <input class="text-input" bind:value={link} id="{html_id + "-link"}" placeholder="Item link or name" />
                    </div>
                {:else}
                    <div class="grow text-lg">
                        <RichText text={link} />
                    </div>
                {/if}
                {#if is_owned && is_editing}
                    <IconButton id="{wishlist_item.id}-save-button" icon="fa-solid fa-check" label="Save" on:click={change_text} />
                    {#if is_new}
                        <IconButton id="{wishlist_item.id}-delete-button" icon="fa-solid fa-trash" label="Delete" on:click={remove} />
                    {:else}
                        <IconButton id="{wishlist_item.id}-cancel-button" icon="fa-solid fa-rotate-left" label="Cancel" on:click={cancel_change_text} />
                    {/if}
                {:else if is_owned}
                    <BurgerMenu id="{wishlist_item.id}-menu" label="Item menu">
                        {#if has_other_wishlists && !is_editing && !is_new}
                            <IconButton id="{wishlist_item.id}-move-out-button" icon="fa-solid fa-arrow-right-from-bracket" label="Move to list" on:click={move_item_to_list} />
                        {/if}
                        {#if !is_new}
                            <IconButton id="{wishlist_item.id}-bought-button" icon="fa-solid fa-basket-shopping" label="Mark as bought" on:click={mark_as_bought} />
                        {/if}
                        {#if !is_editing}
                            <IconButton id="{wishlist_item.id}-edit-button" icon="fa-solid fa-pencil" label="Edit" on:click={() => is_editing = true} />
                            <div class="sm:hidden">
                                <IconButton id="{html_id}-move-top-button" icon="fa-solid fa-angles-up" label="Move to top" on:click={move_to_top} />
                                <IconButton id="{html_id}-move-bottom-button" icon="fa-solid fa-angles-down" label="Move to bottom" on:click={move_to_bottom} />
                            </div>
                        {/if}
                        <IconButton id="{wishlist_item.id}-delete-button" icon="fa-solid fa-trash" label="Delete" on:click={remove} />
                    </BurgerMenu>
                {:else if !is_link_share}
                    <IconButton id="{wishlist_item.id}-bought-button" icon="fa-solid fa-basket-shopping" label="Mark as bought" on:click={mark_as_bought} />
                {/if}
                {#if is_owned}
                    <SortControl id={html_id}
                        on:move_up={move_up}
                        on:move_down={move_down}
                    />
                {/if}
            </div>
        </div>
    {/if}
    {#if is_owned}
        <div class="{wishlist_item.is_header ? "py-3" : "py-2"} hidden sm:block">
            <SortControl id={html_id} move_far has_background={!wishlist_item.is_header}
                on:move_up={move_to_top}
                on:move_down={move_to_bottom}
            />
        </div>
    {/if}
</div>
{#if !wishlist_item.is_header}
    <div class="bg-slate-300 rounded-b-md {is_owned ? "sm:mr-12" : ""}">
        {#if is_editing}
            <Collapse heading="Description" subtle collapsed>
                <textarea class="text-input grow" bind:value={notes} id="{html_id + "-notes"}" placeholder="Enter additional information about this item here..."></textarea>
            </Collapse>
        {:else}
            {#if has_notes}
                <Collapse heading="Description" subtle collapsed>
                    <div class="text-sm">
                        <RichText text={notes} />
                    </div>
                </Collapse>
            {/if}
        {/if}
    </div>
{/if}

<BoughtModal
    is_owner={is_owned}
    defer_bought={most_recent_bought_item?.defer_until != null}
    defer_until={most_recent_bought_item?.defer_until?.toISOString().split('T')[0]}
    bind:this={bought_confirmation_modal}
/>

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
