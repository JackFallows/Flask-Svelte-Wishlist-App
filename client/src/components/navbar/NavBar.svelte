<script lang="ts">
    import '../../tailwind.css';

    import { makeRoutes } from '../../routes';
    import { Get } from '../../http';

    import Notification from '../Notification.svelte';
    import SlidePanel from '../SlidePanel.svelte';

    export let page: string = "";
    export let internal_login_enabled: boolean;
    export let name: string;
    export let profile_pic: string;

    const { Views, Api } = makeRoutes(window.base_path);

    const user_is_authenticated = name != null;
    const external_login_page = internal_login_enabled ? Views.Auth.Login : Views.Auth.External.Login;

    let notifications_panel_visible: boolean = false;
    let user_panel_visible: boolean = false;

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

    function toggle_notifications_panel() {
        user_panel_visible = false;
        notifications_panel_visible = !notifications_panel_visible;
    }

    function toggle_user_panel() {
        notifications_panel_visible = false;
        user_panel_visible = !user_panel_visible;
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
    <div class="flex space-x-4 items-center">
        {#if user_is_authenticated}
            <a class="button" href="{ Views.Wishlist.Create.to_string() }">Create wishlist</a>
            <div class="flex items-center">
                <div class="p-3 {notifications_panel_visible ? 'bg-white rounded-t-xl' : ''}">
                    <button class="icon-button relative" type="button" aria-label="Notifications button" on:click={toggle_notifications_panel}>
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
                <div class="p-3 {user_panel_visible ? 'bg-white rounded-t-xl' : ''}">
                    {#if profile_pic != null}
                    <button class="rounded-full h-10 w-10 hover:bg-purple-600 transition-all" type="button" on:click={toggle_user_panel}>
                        <img src="{ profile_pic }" alt="Hi, {name}" width="30" height="30" class="rounded-full mx-auto pointer-events-none">
                    </button>
                    {:else}
                    <button class="icon-button" aria-label="Hi, {name}" on:click={toggle_user_panel}>
                        <span class="fa-solid fa-user pointer-events-none"></span>
                    </button>
                    {/if}
                    <SlidePanel bind:visible={user_panel_visible}>
                        <div class="flex flex-col space-y-3">
                            <a class="w-full block bg-white hover:bg-slate-100 p-1" href="{ Views.Profile }">
                                <span class="fa-fw fa-regular fa-user"></span>
                                Profile
                            </a>
                            <hr />
                            <a class="w-full block bg-white hover:bg-slate-100 p-1" href="{ Views.Auth.Logout.to_string() }">
                                <span class="fa-fw fa-solid fa-person-walking-arrow-right"></span>
                                Logout
                            </a>
                        </div>
                </SlidePanel>
                </div>
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
