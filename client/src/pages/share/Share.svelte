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

<div class="dark:text-slate-100">
    {#await loading_promise}
        Loading...
    {:then}
        <div class="flex space-x-3">
            <div class="grow">
                <h1 class="text-2xl">{wishlist.name}</h1>

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

                <div class="flex space-y-3 flex-col">
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
