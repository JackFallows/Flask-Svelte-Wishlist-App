<script lang="ts">
    import { ToastType } from '../../enums';
    import { Get, Patch } from '../../http';
    import { makeRoutes } from '../../routes';
    import EditableHeading from '../EditableHeading.svelte';
    import Toast from '../Toast.svelte';
    import WishlistItem from '../WishlistItem.svelte';

    export let wishlist_id: number;

    const { Api } = makeRoutes(window.base_path);

    let toast: Toast;

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

    async function save_wishlist_name() {
        toast.show("Saving...", ToastType.INFO);
        await Patch(Api.Wishlists.PatchUpdateName.append(wishlist_id), { name: wishlist.name });
        toast.show("Saved!", ToastType.SUCCESS);
    }
</script>

<Toast bind:this={toast} />
{#await loading_promise}
    Loading...
{:then}
    {#if is_owned}
        <EditableHeading tag="h1" classes="text-2xl" bind:value={wishlist.name} on:save={save_wishlist_name} />
    {:else}
        <h1 class="text-2xl">{wishlist.name}</h1>
    {/if}
    {#if wishlist_as_share != null}
    <div>
        <span class="text-lg text-black">{wishlist_as_share.owner_name}</span>
        <span class="text-base text-slate-600">{wishlist_as_share.owner_email}</span>
    </div>
    {/if}

    <div class="mt-4 flex space-y-3 flex-col">
        {#each wishlist_items as wishlist_item(wishlist_item)}
            <WishlistItem
                wishlist_item={wishlist_item}
                is_owned={is_owned}
                has_other_wishlists={has_other_wishlists}
                on:bought={(e) => remove_item(e.detail)}
                on:moved={(e) => remove_item(e.detail)}
            />
        {/each}
    </div>
{/await}
