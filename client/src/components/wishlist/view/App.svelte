<script lang="ts">
    import '../../../tailwind.css';

    import { Get } from '../../../http';
    import { makeRoutes } from '../../../routes';
    import WishlistItem from '../../WishlistItem.svelte';

    export let wishlist_id: number;

    const { Api, Views } = makeRoutes(window.base_path);

    let loading_promise: Promise<any> = load_wishlist();

    let wishlist: IWishlist;
    let wishlist_as_share: IWishlistShare;
    let is_owned: boolean;
    let total_wishlists: number;
    let has_other_wishlists: boolean;

    $: wishlist_as_share = (<IWishlistShare>wishlist)?.owner_name != null ? (<IWishlistShare>wishlist) : null;
    $: is_owned = wishlist_as_share == null;
    $: has_other_wishlists = wishlist_id == null ? total_wishlists > 0 : total_wishlists > 1;

    let wishlist_items: IWishlistItem[];

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }
        
        const wishlistPayload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));
        const countPayload = await Get<{ total_wishlists: number }>(Api.Wishlists.GetCountForUser);

        wishlist = wishlistPayload.get_json();
        wishlist_items = wishlist.wishlist_items;
        total_wishlists = countPayload.get_json().total_wishlists;
    }

    function remove_item(item: IWishlistItem) {
        const item_index = wishlist_items.indexOf(item);
        if (item_index === -1) {
            return;
        }

        wishlist_items.splice(item_index, 1);
        wishlist_items = wishlist_items; // trigger reactivity
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
                <WishlistItem wishlist_item={wishlist_item} is_owned={is_owned} has_other_wishlists={has_other_wishlists} on:bought={(e) => remove_item(e.detail)} on:moved={(e) => remove_item(e.detail)} />
            {/each}
        </div>
    </div>

    {#if is_owned}
    <aside class="">
        <a class="button" href="{ Views.Wishlist.Edit.append(wishlist_id).to_string() }">
            Edit wishlist
        </a>
    </aside>
    {/if}
</div>
{/await}
