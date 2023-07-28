<script lang="ts">
    import '../../../tailwind.css';

    import { Get } from '../../../http';
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
<div class="flex space-x-3">
    <div class="grow">
        <h1 class="text-2xl">{wishlist.name}</h1>
        {#if wishlist_as_share != null}
        <div>
            <span class="text-lg text-black">{wishlist_as_share.owner_name}</span>
            <span class="text-base text-slate-600">{wishlist_as_share.owner_email}</span>
        </div>
        {/if}

        <h2 class="text-lg">Items</h2>
        <div class="flex space-y-3 flex-col">
            {#each wishlist_items as wishlist_item(wishlist_item)}
                <WishlistItem wishlist_item={wishlist_item} on:bought={() => loading_promise = load_wishlist()} />
            {/each}
        </div>
    </div>

    {#if wishlist_as_share == null}
    <aside class="h-screen sticky top-0">
        <a class="button" href="{ Views.Wishlist.Edit.append(wishlist_id).to_string() }">
            Edit wishlist
        </a>
    </aside>
    {/if}
</div>
{/await}
