<script lang="ts">
    import { getContext } from 'svelte';
    import { flip } from 'svelte/animate';
    import { ToastType } from '../../enums';
    import { makeRoutes } from '../../routes';
    import EditableHeading from '../../components/EditableHeading.svelte';
    import Toast from '../../components/Toast.svelte';
    import WishlistItem from '../../components/WishlistItem.svelte';

    export let wishlist_id: number;

    const { Delete, Get, Patch, Post } = <IHttp>getContext("http");
    const { Api, Views } = makeRoutes(window.base_path);

    let toast: Toast;

    let wishlist: IWishlist;
    let wishlist_items: IWishlistItem[] = [];
    let bought_items: IBoughtItem[] = [];
    let wishlist_as_share: IWishlistShare;
    let is_owned: boolean;
    let total_wishlists: number;
    let has_other_wishlists: boolean;
    let visible_wishlist_items: IWishlistItem[];
    let most_recent_bought_item: IBoughtItem;

    let loading_promise: Promise<any> = load_wishlist();

    $: wishlist_as_share = (<IWishlistShare>wishlist)?.is_share ? (<IWishlistShare>wishlist) : null;
    $: is_owned = wishlist_as_share == null;
    $: has_other_wishlists = wishlist_id == null ? total_wishlists > 0 : total_wishlists > 1;
    $: {
        const bought_item_ids = bought_items.map(bi => bi.wishlist_item_id);
        visible_wishlist_items = wishlist_items.filter(wi => !bought_item_ids.includes(wi.id));
    }
    $: {
        most_recent_bought_item = bought_items.reduce((most_recent: IBoughtItem, bought_item: IBoughtItem) => {
            if (bought_item.user_id === window.user_id && (most_recent == null || bought_item.id > most_recent.id)) {
                most_recent = bought_item;
            }

            return most_recent;
        }, null);
    }

    async function load_wishlist() {
        if (wishlist_id == 0) {
            wishlist = <any>{
                name: ""
            };
            wishlist_items = [];
            return;
        }
        
        const wishlistPayload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));
        const countPayload = await Get<{ total_wishlists: number }>(Api.Wishlists.GetCountForUser);

        wishlist = wishlistPayload.get_json();
        wishlist_items = wishlist.wishlist_items;
        bought_items = wishlist.bought_items ?? [];

        for (const bought_item of bought_items) {
            bought_item.defer_until = bought_item.defer_until != null ? new Date(<number><any>bought_item.defer_until * 1000) : null;
        }

        total_wishlists = countPayload.get_json().total_wishlists;
    }

    function add_item(is_header: boolean = false) {
        const new_item: IWishlistItem = {
            id: null,
            wishlist_id,
            link: "",
            notes: "",
            bought: false,
            order_number: 0,
            is_header
        };
        wishlist_items = [new_item, ...wishlist_items.map((wi, i) => {
            wi.order_number = i + 1;
            return wi;
        })];
    }

    async function change_item_text(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        if (item.id == null) {
            // create new
            const result = await save_changes<{ wishlist_item_id: number }>(
                Post(Api.WishlistItems.PostCreate, item)
            );

            item.id = result.wishlist_item_id;

            wishlist_items.splice(wishlist_items.indexOf(item), 1, item);
            wishlist_items = wishlist_items; // trigger reactivity

            await ensure_order();
        } else {
            // update existing
            await save_changes(
                Patch(Api.WishlistItems.PatchChangeText.append(item.id), {
                    name: item.link,
                    description: item.notes
                })
            );
        }
    }

    async function move_item_out(event: CustomEvent<{ item: IWishlistItem, target_wishlist_id: number }>) {
        const { item, target_wishlist_id } = event.detail;

        remove_item(item);

        await save_changes(
            Patch(Api.WishlistItems.PatchReparent.append(item.id).append(target_wishlist_id), {})
        );

        await ensure_order();
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

        if (item.id != null) {
            await save_changes(
                Delete(Api.WishlistItems.Delete.append(item.id), {})
            );
        }
        
        await ensure_order();
    }

    async function mark_item_bought(event: CustomEvent<{ item: IWishlistItem, defer_until: string }>) {
        const { item, defer_until } = event.detail;

        const bought_item = await save_changes<IBoughtItem>(Patch(Api.WishlistItems.PatchMarkAsBought.append(item.id), {
            defer_until
        }));

        if (bought_item.defer_until) {
            bought_item.defer_until = new Date(<number><any>bought_item.defer_until * 1000);
        }

        bought_items.push(bought_item);
        bought_items = bought_items; // trigger reactivity
    }

    async function rearrange(item: IWishlistItem, current_index: number, target_index: number) {
        wishlist_items.splice(current_index, 1);
        wishlist_items.splice(target_index, 0, item);

        await ensure_order()
    }

    async function ensure_order() {
        let current_order_number = 0;
        for (const item of wishlist_items) {
            item.order_number = item.id == null ? 0 : current_order_number++;
        }
        wishlist_items = wishlist_items; // trigger reactivity

        const payload = wishlist_items
            .filter(wi => wi.id != null && wi.id != 0)
            .map(wi => ({ wishlist_item_id: wi.id, order_number: wi.order_number }));

        await save_changes(
            Patch(Api.WishlistItems.PatchEnsureOrder.append(wishlist.id), payload)
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
        if (wishlist_id == 0) {
            const wishlist_id_result = await save_changes(
                Post<{ name: string, wishlist_items: IWishlistItem[] }, IWishlist>(
                    Api.Wishlists.Post, {
                        name: wishlist.name, wishlist_items
                    }
                )
            );

            location.href = Views.Wishlist.append(wishlist_id_result.id).to_string();
            return;
        }

        await save_changes(
            Patch(Api.Wishlists.PatchUpdateName.append(wishlist_id), { name: wishlist.name })
        );
    }

    async function save_changes<T>(request: Promise<IHttpResult<T>>): Promise<T> {
        toast.show("Saving...", ToastType.INFO);
        const result = await request;
        toast.show("Saved!", ToastType.SUCCESS);
        return await result.get_json();
    }
</script>

<Toast bind:this={toast} />
{#await loading_promise}
    Loading...
{:then}
    {#if is_owned}
        <div class="pr-2">
            <EditableHeading tag="h1" classes="text-2xl" is_editing={wishlist_id == 0} placeholder="Enter a name for your wishlist" bind:value={wishlist.name} on:save={save_wishlist_name} />
        </div>
    {:else}
        <div class="flex flex-col sm:flex-row">
            <h1 class="text-2xl grow">{wishlist.name}</h1>
            {#if wishlist_as_share != null && wishlist_as_share.owner_name != null}
                <div>
                    <span class="fa-solid fa-users"></span>
                    <span class="text-lg text-black">{wishlist_as_share.owner_name}</span>
                    <span class="text-base text-slate-600">{wishlist_as_share.owner_email}</span>
                </div>
            {/if}
        </div>
    {/if}

    {#if is_owned && wishlist_id != 0}
        <div class="mt-8 flex space-x-3">
            <button class="button" on:click={() => add_item(false)}>Add item</button>
            <button class="button" on:click={() => add_item(true)}>Add heading</button>
        </div>
    {/if}

    <div class="mt-8 flex space-y-3 flex-col">
        {#each visible_wishlist_items as wishlist_item(wishlist_item)}
            <div animate:flip={{ duration: 200 }}>
                <WishlistItem
                    wishlist_item={wishlist_item}
                    is_owned={is_owned}
                    has_other_wishlists={has_other_wishlists}
                    most_recent_bought_item={most_recent_bought_item}
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