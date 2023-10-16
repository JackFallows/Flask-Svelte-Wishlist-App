<script lang="ts">
    import '../../../tailwind.css';

    import { Get, Post, Put } from "../../../http"
    import { makeRoutes } from "../../../routes";
    import WishlistItem from "../../WishlistItem.svelte";
    import Modal from "../../Modal.svelte";

    export let wishlist_id: number;

    const { Api, Views } = makeRoutes(window.base_path);

    let loading_promise = load_wishlist();
    let get_all_wishlists_promise: Promise<IWishlist[]>;

    let confirm_delete_modal: Modal;
    let move_item_modal: Modal;

    let wishlist_name: string;
    let wishlist_items: IWishlistItem[] = [];
    let total_wishlists: number;
    let has_other_wishlists: boolean;

    $: has_other_wishlists = wishlist_id == null ? total_wishlists > 0 : total_wishlists > 1;

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        const wishlistPayload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));
        const countPayload = await Get<{ total_wishlists: number }>(Api.Wishlists.GetCountForUser);

        const wishlist = wishlistPayload.get_json();
        wishlist_name = wishlist.name;
        wishlist_items = wishlist.wishlist_items;
        total_wishlists = countPayload.get_json().total_wishlists;
    }

    async function get_all_wishlists(): Promise<IWishlist[]> {
        const payload = await Get<IWishlist[]>(Api.Wishlists.GetAllForUser);

        let wishlists = payload.get_json();

        if (wishlist_id != null) {
            wishlists = wishlists.filter(w => w.id != wishlist_id);
        }

        return wishlists;
    }

    async function save_wishlist() {
        if (wishlist_id == null) {
            // create new
            const wishlist_response = await Post<{ name: string, wishlist_items: IWishlistItem[] }, IWishlist>(
                Api.Wishlists.Post, {
                    name: wishlist_name ?? "My wishlist", wishlist_items
                });
            
            const wishlist = wishlist_response.get_json();

            wishlist_id = wishlist.id;
        } else {
            // update existing
            await Put<IWishlist, any>(Api.Wishlists.Put, {
                id: wishlist_id,
                user_id: null,
                name: wishlist_name,
                shared: false,
                deleted: false,
                share_guid: null,
                wishlist_items: wishlist_items
            });
        }

        await new Promise(() => {
            location.href = Views.Wishlist.View.append(wishlist_id).to_string();
        });
    }

    function add_item() {
        const new_item: IWishlistItem = {
            id: null,
            wishlist_id: wishlist_id,
            link: "",
            notes: "",
            bought: false,
            order_number: 0
        };

        wishlist_items = [new_item, ...wishlist_items.map((wi, i) => {
            wi.order_number = i + 1;
            return wi;
        })];
    }

    async function move_item_to_list(event: CustomEvent<IWishlistItem>) {
        get_all_wishlists_promise = get_all_wishlists();
        const confirmed = await move_item_modal.show();
    }

    async function remove_item(event: CustomEvent<IWishlistItem>) {
        const confirmed = await confirm_delete_modal.show();
        
        if (!confirmed) {
            return;
        }

        const item = event.detail;

        const item_index = wishlist_items.indexOf(item);
        if (item_index === -1) {
            return;
        }

        wishlist_items.splice(item_index, 1);
        wishlist_items = wishlist_items; // trigger reactivity
    }
</script>

{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="flex space-x-3">
    <div class="grow">
        <div class="">
            <label class="" for="wishlist-name">Wishlist name</label><br />
            <input class="text-input" id="wishlist-name" placeholder="My wishlist" bind:value={wishlist_name} />
        </div>
        <h2 class="mt-2.5 text-lg">Items</h2>
        <button class="button my-2.5" id="add-item-button" on:click={() => add_item()}>Add item</button>
        <div class="flex flex-col space-y-3">
            {#each wishlist_items as wishlist_item(wishlist_item)}
                <WishlistItem wishlist_item={wishlist_item} is_edit={true}  has_other_wishlists={has_other_wishlists} on:delete={remove_item} on:move={move_item_to_list} />
            {/each}
        </div>
    </div>
    <aside class="">
        <button class="success-button" on:click={() => loading_promise = save_wishlist()}>Save wishlist</button>
    </aside>
</div>
{/await}

<Modal bind:this={move_item_modal} id="move">
    <span slot="header">
        Move item
    </span>
    <span slot="body">
        {#if get_all_wishlists_promise}
            {#await get_all_wishlists_promise}
                Loading...
            {:then wishlists} 
                <p>Choose the wishlist to move this item to:</p>
                {#each wishlists as wishlist}
                    <p>{wishlist.name}</p>
                {/each}
            {/await}
        {/if}
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
        Once the wishlist is saved, this action cannot be undone.
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="danger-button" on:click={() => close("true")}>Delete</button>
    </span>
</Modal>

<style lang="less">
</style>
