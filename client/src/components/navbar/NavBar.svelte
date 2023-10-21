<script lang="ts">
    import '../../tailwind.css';

    import { makeRoutes } from '../../routes';
    import { Get } from '../../http';

    import DropDownMenu from '../DropDownMenu.svelte';
    import Notification from '../Notification.svelte';
    import SlidePanel from '../SlidePanel.svelte';

    export let page: string = "";
    export let internal_login_enabled: boolean;
    export let name: string;
    export let profile_pic: string;

    const { Views, Api } = makeRoutes(window.base_path);

    const user_is_authenticated = name != null;
    const external_login_page = internal_login_enabled ? Views.Auth.Login : Views.Auth.External.Login;

    let user_dropdown_button: HTMLElement;
    let user_dropdown: DropDownMenu;

    let notifications_panel_visible: boolean = false;

    let notifications: INotificationDto[];

    let notifications_loading_promise: Promise<INotificationDto[]> = load_notifications();

    async function load_notifications(): Promise<INotificationDto[]> {
        if (!user_is_authenticated) {
            return [];
        }

        notifications = await Get<INotificationDto[]>(Api.Notifications.Get).then(r => r.get_json());

        for (const notification of notifications) {
            notification.created_at = new Date(<number><any>notification.created_at * 1000)
        }

        return notifications;
    }

    function on_notification_changed() {
        notifications_loading_promise = load_notifications();
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
            <div class="p-3 {notifications_panel_visible ? 'bg-white rounded-t-xl' : ''}">
                <button class="icon-button relative" type="button" aria-label="Notifications button" on:click={() => notifications_panel_visible = !notifications_panel_visible}>
                    <span class="fa-solid fa-bell pointer-events-none {notifications?.length > 0 ? 'text-orange-600' : ''}"></span>
                    {#if notifications?.length > 0}
                    <span class="absolute text-white text-xl w-full left-0 top-1 text-center pointer-events-none">{notifications.length < 10 ? notifications.length : '*'}</span>
                    {/if}
                </button>
                <SlidePanel bind:visible={notifications_panel_visible}>
                    {#await notifications_loading_promise}
                        Loading...
                    {:then}
                        {#if notifications.length === 0}
                            <p>
                                No notifications
                            </p>
                        {/if}
                        <div class="flex flex-col space-y-3">
                            {#each notifications as notification}
                                <Notification notification={notification} on:notification_changed={on_notification_changed} />
                            {/each}
                        </div>
                    {/await}
                </SlidePanel>
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
                    <a class="button w-full block" href="{ Views.Profile }">Profile</a>
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
