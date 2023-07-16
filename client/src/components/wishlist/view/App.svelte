<script lang="ts">
    import { Get } from '../../../http';
    import { Api, Views } from '../../../routes';
    import WishlistItem from '../../WishlistItem.svelte';

    export let wishlist_id: number;

    let loading_promise: Promise<void> = load_wishlist();

    let wishlist_name: string;
    let wishlist_items: IWishlistItem[];

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        const wishlist = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id))
        wishlist_name = wishlist.name;
        wishlist_items = wishlist.wishlist_items;
    }
</script>

{#await loading_promise}
    Loading...
{:then}
<h1>{wishlist_name}</h1>
<button class="btn btn-outline-primary float-end" on:click={() => location.href = Views.Wishlist.Edit.append(wishlist_id).to_string()}>
    Edit
</button>
<h2>Items</h2>
{#each wishlist_items as wishlist_item(wishlist_item)}
    <WishlistItem wishlist_item={wishlist_item} />
{/each}
{/await}
