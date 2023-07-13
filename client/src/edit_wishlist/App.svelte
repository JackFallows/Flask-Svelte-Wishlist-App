<script lang="ts">
    import { Get, Post } from "../http"
    import { Api, Views } from "../routes";

    interface $$Props {
        wishlist_id: number;
    }

    interface IWishlist {
        id: number;
        name: string;
    }

    export let wishlist_id: number;

    let loading_promise = load_wishlist();

    let wishlist_name: string;

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        const wishlist = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id))
        wishlist_name = wishlist.name;
    }

    async function save_wishlist() {
        if (wishlist_id == null) {
            // create new
            const wishlist = await Post<{ name: string }, IWishlist>(Api.Wishlists.Post, { name: wishlist_name ?? "My wishlist" })
            
            location.href = Views.Edit.append(wishlist.id).to_string();
        } else {
            // update existing
        }
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
