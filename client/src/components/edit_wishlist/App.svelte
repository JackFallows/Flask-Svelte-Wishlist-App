<script lang="ts">
    import { Get, Post, Put } from "../../http"
    import { Api, Views } from "../../routes";
    import WishlistItem from "../WishlistItem.svelte";

    interface $$Props {
        wishlist_id: number;
    }

    export let wishlist_id: number;

    let loading_promise = load_wishlist();

    let wishlist_name: string;
    let wishlist_items: IWishlistItem[] = [];

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        const wishlist = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id))
        wishlist_name = wishlist.name;
        wishlist_items = wishlist.wishlist_items;
    }

    async function save_wishlist() {
        if (wishlist_id == null) {
            // create new
            const wishlist = await Post<{ name: string, wishlist_items: IWishlistItem[] }, IWishlist>(
                Api.Wishlists.Post, {
                    name: wishlist_name ?? "My wishlist", wishlist_items
                });
            
            location.href = Views.Edit.append(wishlist.id).to_string();
        } else {
            // update existing
            await Put<IWishlist, any>(Api.Wishlists.Put, {
                id: wishlist_id,
                user_id: null,
                name: wishlist_name,
                shared: false,
                deleted: false,
                wishlist_items: wishlist_items
            });

            location.reload();
        }
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
</script>

{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="form-container">
    <div class="form-section-left">
        <div class="mb-3">
            <label class="form-label" for="wishlist-name">Wishlist name</label>
            <input class="form-control" id="wishlist-name" placeholder="My wishlist" bind:value={wishlist_name} />
        </div>
        <h2>Items</h2>
        <button class="btn btn-primary mb-3" id="add-item-button" on:click={() => add_item()}>Add item</button>
        {#each wishlist_items as wishlist_item(wishlist_item)}
            <WishlistItem wishlist_item={wishlist_item} />
        {/each}
    </div>
    <div class="form-section-right">
        <button class="btn btn-outline-success" style="margin-bottom: 0" on:click={() => loading_promise = save_wishlist()}>Save wishlist</button>
    </div>
</div>
{/await}

<style lang="less">
    .form-container {
        display: flex;

        padding-top: 20px;

        .form-section-left {
            flex-grow: 1;
            padding-right: 120px;
        }

        .form-section-right {
            flex-grow: 0;
            right: 8px;
            position: fixed;
        }
    }
</style>
