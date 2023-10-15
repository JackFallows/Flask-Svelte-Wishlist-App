<script lang="ts">
    import '../../tailwind.css';

    import { Get } from '../../http';
    import { makeRoutes } from '../../routes';
    import WishlistItem from '../WishlistItem.svelte';

    let share_guid: string = location.href.substring(location.href.lastIndexOf('/') + 1);

    const { Api } = makeRoutes(window.base_path);

    let loading_promise: Promise<any> = load_wishlist();

    let wishlist: IWishlistLinkShare;
    let wishlist_items: IWishlistItem[];

    async function load_wishlist() {
        if (share_guid?.length != 8) {
            return;
        }
        
        const wishlistPayload = await Get<IWishlistLinkShare>(Api.Wishlists.GetLinkShare.append(share_guid));

        wishlist = wishlistPayload.get_json();
        wishlist_items = wishlist.wishlist_items;
    }
</script>

{#await loading_promise}
    Loading...
{:then}
<div class="flex space-x-3">
    <div class="grow">
        <h1 class="text-2xl">{wishlist.name}</h1>

        <h2 class="text-lg">Items</h2>
        <div class="flex space-y-3 flex-col">
            {#each wishlist_items as wishlist_item(wishlist_item)}
                <WishlistItem wishlist_item={wishlist_item} share_guid={share_guid} on:bought={() => loading_promise = load_wishlist()} />
            {/each}
        </div>
    </div>
</div>
{/await}
