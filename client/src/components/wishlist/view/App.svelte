<script lang="ts">
    import { Get, HttpResult } from '../../../http';
    import { Api, Views } from '../../../routes';
    import WishlistItem from '../../WishlistItem.svelte';

    export let wishlist_id: number;

    let loading_promise: Promise<any> = load_wishlist();

    let wishlist: IWishlist;
    let wishlist_as_share: IWishlistShare;

    $: wishlist_as_share = (<IWishlistShare>wishlist)?.owner_name != null ? (<IWishlistShare>wishlist) : null;

    let wishlist_items: IWishlistItem[];

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        wishlist = (await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id))).get_json();
        wishlist_items = wishlist.wishlist_items;
    }
</script>

{#await loading_promise}
    Loading...
{:then}
<h1>{wishlist.name}</h1>
{#if wishlist_as_share != null}
<h3 class="text-body-secondary">{wishlist_as_share.owner_name}</h3>
<h4 class="text-body-secondary">{wishlist_as_share.owner_email}</h4>
{:else}
<a class="btn btn-outline-primary float-end" href="{ Views.Wishlist.Edit.append(wishlist_id).to_string() }">
    Edit
</a>
{/if}
<h2>Items</h2>
{#each wishlist_items as wishlist_item(wishlist_item)}
    <WishlistItem wishlist_item={wishlist_item} on:bought={() => loading_promise = load_wishlist()} />
{/each}
{/await}
