<script lang="ts">
    import '../../tailwind.css';

    import { Get, Patch } from '../../http';
    import { makeRoutes } from '../../routes';
    import { ToastType } from '../../enums';
    import WishlistItem from '../WishlistItem.svelte';
    import Toast from '../Toast.svelte';

    let share_guid: string = location.href.substring(location.href.lastIndexOf('/') + 1);

    let toast: Toast;

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

    async function mark_item_bought(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        remove_item(item);

        await save_changes(Patch(Api.WishlistItems.PatchLinkShareMarkBought.append(share_guid).append(item.id), null));
    }

    function remove_item(item: IWishlistItem) {
        const item_index = wishlist_items.indexOf(item);
        if (item_index === -1) {
            return;
        }

        wishlist_items.splice(item_index, 1);
        wishlist_items = wishlist_items; // trigger reactivity
    }

    async function save_changes(request: Promise<any>) {
        toast.show("Saving...", ToastType.INFO);
        await request;
        toast.show("Saved!", ToastType.SUCCESS);
    }
</script>

<Toast bind:this={toast} />
{#await loading_promise}
    Loading...
{:then}
<div class="flex space-x-3">
    <div class="grow">
        <h1 class="text-2xl">{wishlist.name}</h1>

        <h2 class="text-lg">Items</h2>
        <div class="flex space-y-3 flex-col">
            {#each wishlist_items as wishlist_item(wishlist_item)}
                <WishlistItem wishlist_item={wishlist_item} on:buy={mark_item_bought} />
            {/each}
        </div>
    </div>
</div>
{/await}
