<script lang="ts">
    import '../../tailwind.css';

    import { getContext } from 'svelte';
    import { makeRoutes } from '../../routes';
    import { AlertColor } from '../../enums';
    import WishlistItem from '../../components/WishlistItem.svelte';
    import Alert from '../../components/Alert.svelte';

    let share_guid: string = location.href.substring(location.href.lastIndexOf('/') + 1);

    const is_logged_in: boolean = window.user_name != null;

    const { Get, Patch } = <IHttp>getContext("http");
    const { Api, Views } = makeRoutes(window.base_path);

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

    async function add_to_account() {
        await Patch(Api.Wishlists.PatchAddToAccount.append(share_guid), {});
        location.href = Views.Wishlist.append(wishlist.id).to_string();
    }
</script>

<div class="dark:text-slate-100 pb-8">
    {#await loading_promise}
        Loading...
    {:then}
        <div class="flex space-x-3">
            <div class="grow">
                <div class="sticky z-[1] top-16 bg-white/90 dark:bg-slate-700/90 backdrop-blur-sm py-4 flex justify-between items-center border-b border-slate-300">
                    <h1 class="text-2xl">{wishlist.name}</h1>
                </div>

                <Alert color={AlertColor.BLUE}>
                    <p>Add this wishlist to your account to mark items as bought and receive notifications when it changes!</p>
                    {#if !is_logged_in}
                        <p>Use the buttons in the top right to log in or create an account.</p>
                    {:else}
                        <p class="mt-2">
                            <button class="button" on:click={add_to_account}>
                                <span class="fa-solid fa-plus pointer-events-none"></span> Add to my account
                            </button>
                        </p>
                    {/if}
                </Alert>

                <div class="flex space-y-8 flex-col">
                    {#each wishlist_items as wishlist_item(wishlist_item)}
                        <div>
                            <WishlistItem wishlist_item={wishlist_item} is_link_share />
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    {/await}
</div>
