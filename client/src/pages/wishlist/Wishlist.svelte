<script lang="ts">
    import { getContext } from 'svelte';
    import { flip } from 'svelte/animate';
    import { fade } from 'svelte/transition';
    import { ToastType } from '../../enums';
    import { makeRoutes } from '../../routes';
    import EditableHeading from '../../components/EditableHeading.svelte';
    import Toast from '../../components/Toast.svelte';
    import WishlistItem from '../../components/WishlistItem.svelte';
    import Collaborate from '../../components/Collaborate.svelte';
    import Collapse from '../../components/Collapse.svelte';
    import TabContainer from '../../components/TabContainer.svelte';
    import TabContent from '../../components/TabContent.svelte';
    import PanelMessage from '../../components/PanelMessage.svelte';
    import RichText from '../../components/RichText.svelte';
    import IconButton from '../../components/IconButton.svelte';
    import RestoreModal from '../../components/modals/RestoreModal.svelte';

    export let wishlist_id: number;

    const { Delete, Get, Patch, Post } = <IHttp>getContext("http");
    const { Api, Views } = makeRoutes(window.base_path);

    let toast: Toast;
    let collaborate: Collaborate;
    let restore_modal: RestoreModal;

    let wishlist: IWishlist;
    let wishlist_items: IWishlistItem[] = [];
    let bought_items: IBoughtItem[] = [];
    let wishlist_as_share: IWishlistShare;
    let is_owned: boolean;
    let total_wishlists: number;
    let has_other_wishlists: boolean;
    let visible_wishlist_items: IWishlistItem[];
    let bought_wishlist_items: { bought: IBoughtItem, item: IWishlistItem }[];
    let most_recent_bought_item: IBoughtItem;

    let editing_items: IWishlistItem[] = [];
    let locked_items: IWishlistItem[] = [];

    let loading_promise: Promise<any> = load_wishlist();

    let current_tab_id: string = "list-tab";

    $: wishlist_as_share = (<IWishlistShare>wishlist)?.is_share ? (<IWishlistShare>wishlist) : null;
    $: is_owned = wishlist_as_share == null;
    $: has_other_wishlists = wishlist_id == null ? total_wishlists > 0 : total_wishlists > 1;
    $: {
        const bought_item_ids = bought_items.map(bi => bi.wishlist_item_id);
        visible_wishlist_items = wishlist_items.filter(wi => !bought_item_ids.includes(wi.id));
        bought_wishlist_items = bought_items.map(bi => ({
            bought: bi,
            item: wishlist_items.find(wi => wi.id === bi.wishlist_item_id)
        }));
    }
    $: {
        most_recent_bought_item = bought_items.reduce((most_recent: IBoughtItem, bought_item: IBoughtItem) => {
            if (bought_item.current_user_bought && (most_recent == null || bought_item.id > most_recent.id)) {
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
            bought_item.defer_until = bought_item.defer_until != null ? new Date(<number><any>bought_item.defer_until * 1000 - (new Date().getTimezoneOffset() * 60000)) : null;
            bought_item.bought_date = new Date(<number><any>bought_item.bought_date * 1000);
        }

        total_wishlists = countPayload.get_json().total_wishlists;
    }

    function change_tab(event: CustomEvent<ITab>) {
        const tab = event.detail;
        current_tab_id = tab.id;
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

    async function changing_item_text(event: CustomEvent<{ item: IWishlistItem, cancelled?: boolean }>) {
        const { item, cancelled } = event.detail;

        if (item.id == null) {
            return;
        }

        if (!cancelled) {
            editing_items = [ ...editing_items, item ];
        } else {
            editing_items = editing_items.filter(i => i !== item);
        }

        collaborate?.notify('item:editing', {
            wishlist_item_id: item.id,
            cancelled
        });
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

            collaborate?.notify('item:created', {
                wishlist_item_id: item.id
            });
        } else {
            // update existing
            await save_changes(
                Patch(Api.WishlistItems.PatchChangeText.append(item.id), {
                    name: item.link,
                    description: item.notes
                })
            );

            editing_items = editing_items.filter(i => i.id !== item.id);

            collaborate?.notify('item:edited', {
                wishlist_item_id: item.id
            });
        }
    }

    async function move_item_out(event: CustomEvent<{ item: IWishlistItem, target_wishlist_id: number }>) {
        const { item, target_wishlist_id } = event.detail;

        remove_item(item);

        await save_changes(
            Patch(Api.WishlistItems.PatchReparent.append(item.id).append(target_wishlist_id), {})
        );

        await ensure_order();

        collaborate?.notify('item:removed', {
            wishlist_item_id: item.id
        });
    }

    async function move_item_to_top(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        const current_index = wishlist_items.indexOf(item);
        if (current_index <= 0) {
            return;
        }

        const target_index = 0;

        await rearrange(item, current_index, target_index);
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

    async function move_item_to_bottom(event: CustomEvent<{ item: IWishlistItem }>) {
        const { item } = event.detail;

        const current_index = wishlist_items.indexOf(item);
        if (current_index === (wishlist_items.length - 1)) {
            return;
        }

        const target_index = wishlist_items.length - 1;

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

        collaborate?.notify('item:removed', {
            wishlist_item_id: item.id
        });
    }

    async function mark_item_bought(event: CustomEvent<{ item: IWishlistItem, defer_until: string }>) {
        const { item, defer_until } = event.detail;

        const bought_item = await save_changes<IBoughtItem>(Patch(Api.WishlistItems.PatchMarkAsBought.append(item.id), {
            defer_until
        }));

        if (bought_item.defer_until) {
            bought_item.defer_until = new Date(<number><any>bought_item.defer_until * 1000 - (new Date().getTimezoneOffset() * 60000));
        }

        bought_item.bought_date = new Date(<number><any>bought_item.bought_date * 1000);

        bought_items.push(bought_item);
        bought_items = bought_items; // trigger reactivity

        collaborate?.notify('item:bought', {
            wishlist_item_id: item.id,
            is_deferred: bought_item.defer_until != null,
            bought_date: bought_item.bought_date
        });
    }

    async function restore_item(wishlist_item_id: number) {
        const confirm = await restore_modal.show(wishlist_items.find(wi => wi.id === wishlist_item_id).link);

        if (!confirm) {
            return;
        }

        await save_changes(Patch(Api.WishlistItems.PatchRestore.append(wishlist_item_id), {}));

        bought_items = bought_items.filter(bi => bi.wishlist_item_id !== wishlist_item_id);

        collaborate?.notify('item:restored', {
            wishlist_item_id: wishlist_item_id
        });
    }

    async function rearrange(item: IWishlistItem, current_index: number, target_index: number) {
        wishlist_items.splice(current_index, 1);
        wishlist_items.splice(target_index, 0, item);

        await ensure_order();

        collaborate?.notify('item:moved', {
            wishlist_item_id: item.id
        });
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

        collaborate?.notify('item:rename', {});
    }

    async function save_changes<T>(request: Promise<IHttpResult<T>>): Promise<T> {
        toast.show("Saving...", ToastType.INFO);
        const result = await request;
        toast.show("Saved!", ToastType.SUCCESS);
        return await result.get_json();
    }

    function collaborate_init(notify: Notify) {
        notify("item:get_status", {});
    }

    async function handle_collaborator_notification(event: CustomEvent<{ event_name: string, data: any }>) {
        const { event_name, data } = event.detail;

        function update_order_numbers(updated_items: IWishlistItem[]) {
            for (const item of wishlist_items) {
                const updated = updated_items.find(wi => wi.id === item.id);
                item.order_number = updated.order_number;
            }

            wishlist_items = wishlist_items.sort((a, b) => {
                if (a.order_number < b.order_number) {
                    return -1;
                }

                if (a.order_number > b.order_number) {
                    return 1;
                }

                return 0;
            });
        }

        if (event_name === "get_status") {
            for (const editing_item of editing_items) {
                collaborate?.notify('item:editing', {
                    wishlist_item_id: editing_item.id
                });
            }
        } else if (event_name === "bought") {
            const { wishlist_item_id, is_deferred, bought_date }: { wishlist_item_id: number, is_deferred: boolean, bought_date: Date } = data;

            if (is_deferred && is_owned) {
                return;
            }

            toast.show("An item was bought by another user", ToastType.INFO);

            bought_items = [ ...bought_items, <IBoughtItem>{ wishlist_item_id, bought_date: new Date(bought_date), current_user_bought: false } ];
        } else if (event_name === "restored") {
            const { wishlist_item_id }: { wishlist_item_id: number } = data;

            bought_items = bought_items.filter(bi => bi.wishlist_item_id !== wishlist_item_id);
        } else if (event_name === "editing") {
            const { wishlist_item_id, cancelled }: { wishlist_item_id: number, cancelled?: boolean } = data;

            if (!cancelled) {
                locked_items = [ ...locked_items, wishlist_items.find(i => i.id === wishlist_item_id) ];
            } else {
                locked_items = locked_items.filter(i => i.id !== wishlist_item_id);
            }
        } else if (event_name === "edited") {
            const { wishlist_item_id }: { wishlist_item_id: number } = data;

            const updated_item_result = await Get<IWishlistItem>(Api.WishlistItems.Get.append(wishlist_item_id));
            const updated_item = updated_item_result.get_json();

            wishlist_items.splice(wishlist_items.findIndex(i => i.id === updated_item.id), 1, updated_item);
            wishlist_items = wishlist_items;
            locked_items = locked_items.filter(i => i.id !== updated_item.id);
        } else if (event_name === "moved") {
            const wishlist_payload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));
            const tmp_wishlist = wishlist_payload.get_json();
            update_order_numbers(tmp_wishlist.wishlist_items);
        } else if (event_name === "created") {
            const { wishlist_item_id }: { wishlist_item_id: number } = data;

            const wishlist_payload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));
            const tmp_wishlist = wishlist_payload.get_json();
            const new_item = tmp_wishlist.wishlist_items.find(i => i.id === wishlist_item_id);

            wishlist_items.splice(0, 0, new_item);
            update_order_numbers(tmp_wishlist.wishlist_items);

            toast.show(`${wishlist_as_share.owner_name} added ${new_item.is_header ? "a heading" : "an item"}`, ToastType.INFO);
        } else if (event_name === "removed") {
            const { wishlist_item_id }: { wishlist_item_id: number } = data;

            const wishlist_payload = await Get<IWishlist>(Api.Wishlists.Get.append(wishlist_id));
            const tmp_wishlist = wishlist_payload.get_json();
            
            const deleted = wishlist_items.splice(wishlist_items.findIndex(i => i.id === wishlist_item_id), 1);
            update_order_numbers(tmp_wishlist.wishlist_items);

            toast.show(`${wishlist_as_share.owner_name} removed ${deleted[0].is_header ? "a heading" : "an item"}`, ToastType.INFO);
        } else if (event_name === "rename") {
            const new_name_result = await Get<{ name: string }>(Api.Wishlists.GetName.append(wishlist_id));
            const new_name = new_name_result.get_json().name;
            wishlist.name = new_name;
            toast.show(`${wishlist_as_share.owner_name} renamed the wishlist`, ToastType.INFO);
        }
    }
</script>

<Toast bind:this={toast} />
<div class="dark:text-slate-100 pb-8">
    {#await loading_promise}
        Loading...
    {:then}
        <div class="sticky z-[1] top-16 bg-white/90 dark:bg-slate-700/90 backdrop-blur-sm border-b border-slate-200 dark:border-slate-600">
            <div class="flex justify-between items-center">
                {#if is_owned}
                    <div class="pr-2 grow py-4">
                        <EditableHeading tag="h1" classes="text-2xl" is_editing={wishlist_id == 0} placeholder="Enter a name for your wishlist" bind:value={wishlist.name} on:save={save_wishlist_name} />
                    </div>
                {:else}
                    <div class="grow flex flex-col py-4">
                        <h1 class="text-2xl grow">{wishlist.name}</h1>
                        {#if wishlist_as_share != null && wishlist_as_share.owner_name != null}
                            <div>
                                <span class="fa-solid fa-users"></span>
                                <span class="text-lg text-black dark:text-slate-100">{wishlist_as_share.owner_name}</span>
                                <span class="text-base text-slate-600 dark:text-slate-300">{wishlist_as_share.owner_email}</span>
                            </div>
                        {/if}
                    </div>
                {/if}
                {#if wishlist_id != 0}
                    <div class="flex flex-col self-end">
                        <div class="flex space-x-3 items-baseline">
                            <Collaborate bind:this={collaborate} room={`wishlist:${wishlist_id}`} hidden={is_owned} listen_for={[ "get_status", "bought", "restored", "editing", "edited", "moved", "created", "removed", "rename" ]} after_init={collaborate_init} on:notification={handle_collaborator_notification} />
                            <TabContainer light no_content on:change_tab={change_tab}>
                                <TabContent id="list-tab" label="List" icon="fa-solid fa-list" />
                                <TabContent id="history-tab" label="Bought items" icon="fa-solid fa-clock-rotate-left" />
                            </TabContainer>
                        </div>
                    </div>
                {/if}
            </div>
        </div>

        {#if current_tab_id === "list-tab"}
            <div in:fade={{ delay: 150, duration: 150 }} out:fade={{ duration: 150 }}>
                {#if is_owned && wishlist_id != 0}
                    <div class="mt-8 flex space-x-3">
                        <button class="button" on:click={() => add_item(false)}>Add item</button>
                        <button class="button" on:click={() => add_item(true)}>Add heading</button>
                    </div>
                {/if}

                <div class="mt-8 flex space-y-8 flex-col">
                    {#each visible_wishlist_items as wishlist_item(wishlist_item)}
                        <div animate:flip={{ duration: 200 }}>
                            <WishlistItem
                                wishlist_item={wishlist_item}
                                is_owned={is_owned}
                                is_locked={locked_items.some(i => i === wishlist_item)}
                                has_other_wishlists={has_other_wishlists}
                                most_recent_bought_item={most_recent_bought_item}
                                on:changing_text={changing_item_text}
                                on:change_text={change_item_text}
                                on:move_out={move_item_out}
                                on:move_to_top={move_item_to_top}
                                on:move_up={move_item_up}
                                on:move_down={move_item_down}
                                on:move_to_bottom={move_item_to_bottom}
                                on:buy={mark_item_bought}
                                on:remove={delete_item}
                            />
                        </div>
                    {/each}
                </div>
            </div>
        {:else}
            <div in:fade={{ delay: 150, duration: 150 }} out:fade={{ duration: 150 }}>
                <div class="mt-8 flex space-y-8 flex-col">
                    {#if bought_wishlist_items.length === 0}
                        <p>No items have been bought.</p>
                    {/if}
                    {#each bought_wishlist_items as bought_wishlist_item(bought_wishlist_item.item)}
                        <div animate:flip={{ duration: 200 }}>
                            <PanelMessage highlighted={bought_wishlist_item.bought.current_user_bought}>
                                <div slot="heading" class="flex justify-between items-baseline">
                                    <div>
                                        {#if bought_wishlist_item.bought.current_user_bought}
                                        You bought this item
                                        {:else}
                                        Someone else bought this item
                                        {/if}
                                    </div>
                                    <div>
                                        {bought_wishlist_item.bought.bought_date.toLocaleString()}
                                    </div>
                                </div>
                                <div slot="body">
                                    <div class="flex items-center justify-between">
                                        <div>
                                            <RichText text={bought_wishlist_item.item.link} />
                                        </div>
                                        {#if bought_wishlist_item.bought.current_user_bought}
                                            <IconButton id="restore-item-{bought_wishlist_item.item.id}" label="Restore" icon="fa-solid fa-rotate-left" on:click={() => restore_item(bought_wishlist_item.item.id)} />
                                        {/if}
                                    </div>

                                    {#if bought_wishlist_item.item.notes?.trim().length > 0}
                                        <div class="bg-slate-200 dark:bg-slate-800 rounded-b-md -mx-2 -mb-2 mt-2">
                                            <Collapse heading="Description" subtle collapsed>
                                                <div class="text-sm">
                                                    <RichText text={bought_wishlist_item.item.notes} />
                                                </div>
                                            </Collapse>
                                        </div>
                                    {/if}
                                </div>
                            </PanelMessage>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    {/await}
</div>

<RestoreModal bind:this={restore_modal} />
