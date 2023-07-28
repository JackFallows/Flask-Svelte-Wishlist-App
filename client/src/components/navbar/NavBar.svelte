<script lang="ts">
    import '../../tailwind.css';

    import { Views, Api } from '../../routes';
    import { Get, Patch } from '../../http';

    import DropDownMenu from '../DropDownMenu.svelte';

    export let page: string = "";
    export let internal_login_enabled: boolean;
    export let name: string;
    export let profile_pic: string;

    interface INotification {
        user_name: string;
        email: string;
        wishlist_id: number;
        wishlist_name: string;
    }

    const user_is_authenticated = name != null;
    const external_login_page = internal_login_enabled ? Views.Auth.Login : Views.Auth.External.Login;

    let user_dropdown_button: HTMLElement;
    let user_dropdown: DropDownMenu;

    let notifications_dropdown_button: HTMLElement;
    let notifications_dropdown: DropDownMenu;

    let notifications: INotification[];

    let share_notifications_loading_promise: Promise<INotification[]> = load_share_notifications();

    async function load_share_notifications(): Promise<INotification[]> {
        if (!user_is_authenticated) {
            return [];
        }

        notifications = await Get<INotification[]>(Api.Wishlists.GetPendingSharedForUser).then(r => r.get_json());

        return notifications;
    }

    async function accept_share(wishlist_id: number): Promise<void> {
        await Patch(Api.Wishlists.PatchAcceptShare.append(wishlist_id), null);
        share_notifications_loading_promise = load_share_notifications();
    }

    async function reject_share(wishlist_id: number): Promise<void> {
        await Patch(Api.Wishlists.PatchRejectShare.append(wishlist_id), null);
        share_notifications_loading_promise = load_share_notifications();
    }
</script>

<nav class="z-50 fixed top-0 flex w-screen bg-slate-300 h-16 items-center text-xl px-3 justify-between shadow-md">
    <div class="flex items-center space-x-3">
        <a class="icon-button" aria-current="page" href="{ Views.Home }" aria-label="Home button"><span class="fa-solid fa-home"></span></a>
        {#if page != ""}
        <span class="fa fa-chevron-right"></span>
        <span>{page}</span>
        {/if}
    </div>
<div class="flex space-x-3 items-center">
        {#if user_is_authenticated}
            <a class="button" href="{ Views.Wishlist.Create.to_string() }">Create wishlist</a>
            <div class="relative">
                <button class="icon-button {notifications?.length > 0 ? 'text-orange-600' : ''}" type="button" aria-label="Notifications button" bind:this={notifications_dropdown_button} on:click={() => notifications_dropdown.toggle()}>
                    <span class="fa-solid fa-bell pointer-events-none"></span>
                </button>
                <DropDownMenu bind:this={notifications_dropdown} button={notifications_dropdown_button} classes="right-0 w-80">
                    {#await share_notifications_loading_promise}
                        Loading...
                    {:then}
                        {#if notifications.length === 0}
                            <p>
                                No notifications
                            </p>
                        {/if}
                        {#each notifications as notification}
                            <div>
                                <p>{notification.user_name} has given you access to '{notification.wishlist_name}'</p>
                                <p>Accept?</p>
                                <div class="inline-block">
                                    <div class="button-group">
                                        <button class="button" on:click={() => accept_share(notification.wishlist_id)}>
                                            <span class="fa-solid fa-check"></span> Yes
                                        </button>
                                        <button class="button" on:click={() => reject_share(notification.wishlist_id)}>
                                            <span class="fa-solid fa-xmark"></span> No
                                        </button>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    {/await}
                </DropDownMenu>
            </div>
            <div class="relative h-10">
                {#if profile_pic != null}
                <button class="rounded-full h-10 w-10 hover:bg-purple-600 transition-all" type="button" bind:this={user_dropdown_button} on:click={() => user_dropdown.toggle()}>
                    <img src="{ profile_pic }" alt="Hi, {name}" width="30" height="30" class="rounded-full mx-auto pointer-events-none">
                </button>
                {:else}
                <button class="icon-button" aria-label="Hi, {name}" bind:this={user_dropdown_button} on:click={() => user_dropdown.toggle()}>
                    <span class="fa-solid fa-user pointer-events-none"></span>
                </button>
                {/if}
                <DropDownMenu bind:this={user_dropdown} button={user_dropdown_button} classes="right-0 w-48">
                    <a class="button w-full block" href="{ Views.Auth.Logout.to_string() }">Logout</a>
                </DropDownMenu>
            </div>
        {:else}
            <div class="button-group">
                {#if internal_login_enabled}
                    <a class="button" href="{ Views.Auth.SignUp.to_string() }">Sign up</a>
                {/if}
                <a class="button" href="{ external_login_page.to_string() }">Log in</a>
            </div>
        {/if}
    </div>
</nav>

<style lang="less">

</style>
