<script lang="ts">
    import { flip } from 'svelte/animate';
    import { ToastType } from '../../enums';
    import { Delete, Get, Patch } from '../../http';
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

    async function change_item_text(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;
        await save_changes(
            Patch(Api.WishlistItems.PatchChangeText.append(item.id), {
                name: item.link,
                description: item.notes
            })
        );
    }

    async function move_item_out(event: CustomEvent<{ item: IWishlistItem, target_wishlist_id: number }>) {
        const { item, target_wishlist_id } = event.detail;

        await save_changes(
            Patch(Api.WishlistItems.PatchReparent.append(item.id).append(target_wishlist_id), {})
        );
    }

    async function move_item_up(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        const current_index = wishlist_items.indexOf(item);
        if (current_index <= 0) {
            return;
        }

        const target_index = current_index - 1;

        await rearrange(item, current_index, target_index);
    }

    async function move_item_down(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        const current_index = wishlist_items.indexOf(item);
        if (current_index === (wishlist_items.length - 1)) {
            return;
        }

        const target_index = current_index + 1;

        await rearrange(item, current_index, target_index);
    }

    async function delete_item(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        remove_item(item);

        await save_changes(
            Delete(Api.WishlistItems.Delete.append(item.id), {})
        );
    }

    async function mark_item_bought(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        remove_item(item);

        await save_changes(Patch(Api.WishlistItems.PatchMarkAsBought.append(item.id), null));
    }

    async function rearrange(item: IWishlistItem, current_index: number, target_index: number) {
        wishlist_items.splice(current_index, 1);
        wishlist_items.splice(target_index, 0, item);
        wishlist_items = wishlist_items.map((wi, i) => {
            wi.order_number = i;
            return wi;
        });

        await save_changes(
            Patch(Api.WishlistItems.PatchReorder.append(item.id).append(item.order_number), {})
        );
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
        await save_changes(
            Patch(Api.Wishlists.PatchUpdateName.append(wishlist_id), { name: wishlist.name })
        );
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

    <div class="mt-8 flex space-y-3 flex-col">
        {#each wishlist_items as wishlist_item(wishlist_item)}
            <div animate:flip={{ duration: 200 }}>
                <WishlistItem
                    wishlist_item={wishlist_item}
                    is_owned={is_owned}
                    has_other_wishlists={has_other_wishlists}
                    on:change_text={change_item_text}
                    on:move_out={move_item_out}
                    on:move_up={move_item_up}
                    on:move_down={move_item_down}
                    on:buy={mark_item_bought}
                    on:remove={delete_item}
                />
            </div>
        {/each}
    </div>
{/await}
