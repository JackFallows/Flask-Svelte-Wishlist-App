<script lang="ts">
    import '../../../tailwind.css';
    import { flip } from 'svelte/animate';

    import { Get, Post, Put } from "../../../http"
    import { makeRoutes } from "../../../routes";
    import WishlistItem from "../../WishlistItem.svelte";
    import Modal from "../../Modal.svelte";

    export let wishlist_id: number;

    const { Api, Views } = makeRoutes(window.base_path);

    let loading_promise = load_wishlist();

    let confirm_delete_modal: Modal;

    let wishlist_name: string;
    let wishlist_items: IWishlistItem[] = [];

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        const wishlistPayload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));

        const wishlist = wishlistPayload.get_json();
        wishlist_name = wishlist.name;
        wishlist_items = wishlist.wishlist_items;
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

    function add_item(is_header: boolean = false) {
        const new_item: IWishlistItem = {
            id: null,
            wishlist_id,
            link: "",
            notes: "",
            bought: false,
            order_number: 0,
            is_header
        };

        wishlist_items = [new_item, ...wishlist_items.map((wi, i) => {
            wi.order_number = i + 1;
            return wi;
        })];
    }

    async function delete_item(event: CustomEvent<IWishlistItem>) {
        const confirmed = await confirm_delete_modal.show();
        
        if (!confirmed) {
            return;
        }

        const item = event.detail;

        remove_item(item);
    }

    function remove_item(item: IWishlistItem) {
        const item_index = wishlist_items.indexOf(item);
        if (item_index === -1) {
            return;
        }

        wishlist_items.splice(item_index, 1);
        wishlist_items = wishlist_items; // trigger reactivity
    }

    function sort_up(event: CustomEvent<{ item: IWishlistItem }>) {
        const current_index = wishlist_items.indexOf(event.detail.item);
        if (current_index <= 0) {
            return;
        }

        const target_index = current_index - 1;

        sort(event.detail.item, current_index, target_index);
    }

    function sort_down(event: CustomEvent<{ item: IWishlistItem }>) {
        const current_index = wishlist_items.indexOf(event.detail.item);
        if (current_index === (wishlist_items.length - 1)) {
            return;
        }

        const target_index = current_index + 1;

        sort(event.detail.item, current_index, target_index);
    }

    function sort(item: IWishlistItem, current_index: number, target_index: number) {
        wishlist_items.splice(current_index, 1);

        wishlist_items.splice(target_index, 0, item);

        wishlist_items = wishlist_items.map((wi, i) => {
            wi.order_number = i;
            return wi;
        });
    }
</script>

{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="flex space-x-3">
    <div class="grow">
        <div class="">
            <label class="" for="wishlist-name">Wishlist name</label><br />
            <input class="text-input md:w-96" id="wishlist-name" placeholder="My wishlist" bind:value={wishlist_name} />
        </div>
        <h2 class="mt-2.5 text-lg">Items</h2>
        <button class="button my-2.5" id="add-item-button" on:click={() => add_item()}>Add item</button>
        <button class="button my-2.5" id="add-header-button" on:click={() => add_item(true)}>Add heading</button>
        <div class="flex flex-col space-y-3">
            {#each wishlist_items as item(item)}
                <div animate:flip={{ duration: 200 }}>
                    <WishlistItem
                        wishlist_item={item}
                        is_edit={true}
                        on:delete={delete_item}
                        on:move_up={sort_up}
                        on:move_down={sort_down}
                    />
                </div>
            {/each}
        </div>
    </div>
    <aside class="">
        <button class="success-button" on:click={() => loading_promise = save_wishlist()}>Save wishlist</button>
    </aside>
</div>
{/await}

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
