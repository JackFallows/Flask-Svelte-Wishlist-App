<script lang="ts">
    import { Views, Api } from '../../routes';
    import { Get, Put } from '../../http';

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

    let share_notifications_loading_promise: Promise<INotification[]> = load_share_notifications();

    async function load_share_notifications(): Promise<INotification[]> {
        if (!user_is_authenticated) {
            return [];
        }

        return await Get(Api.Wishlists.GetPendingSharedForUser);
    }

    async function accept_share(wishlist_id: number): Promise<void> {
        await Put(Api.Wishlists.AcceptShare.append(wishlist_id), null);
        share_notifications_loading_promise = load_share_notifications();
    }

    async function reject_share(wishlist_id: number): Promise<void> {
        await Put(Api.Wishlists.RejectShare.append(wishlist_id), null);
        share_notifications_loading_promise = load_share_notifications();
    }
</script>

<nav class="navbar fixed-top navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <span class="navbar-brand">Wishlist App</span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-supported-content" aria-controls="navbar-supported-content" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar-supported-content">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="{ Views.Home }">Home</a>
                </li>
            </ul>
            {#if user_is_authenticated}
                <a class="btn btn-outline-primary me-2" style="margin-bottom: 0" href="{ Views.Wishlist.Create.to_string() }">Create wishlist</a>
                <div class="dropdown">
                    <button class="btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <span class="fa-solid fa-bell"></span>
                    </button>
                    <ul class="dropdown-menu">
                        {#await share_notifications_loading_promise}
                            Loading...
                        {:then notifications}
                            {#if notifications.length === 0}
                            <li>
                                No notifications
                            </li>
                            {/if}
                            {#each notifications as notification}
                                <li>
                                    <p>{notification.user_name} has given you access to '{notification.wishlist_name}'</p>
                                    <p>Accept?</p>
                                    <div class="btn-group" role="group">
                                        <button class="btn btn-success" on:click={() => accept_share(notification.wishlist_id)}>
                                            <span class="fa-solid fa-check"></span>
                                        </button>
                                        <button class="btn btn-danger" on:click={() => reject_share(notification.wishlist_id)}>
                                            <span class="fa-solid fa-xmark"></span>
                                        </button>
                                    </div>
                                </li>
                            {/each}
                        {/await}
                    </ul>
                </div>
                <div class="dropdown">
                    <button class="btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Hi, { name }
                        <img src="{ profile_pic }" alt="Profile pic" width="24" height="24" class="d-inline-block align-text-top" style="border-radius: 20px">
                    </button>
                    <ul class="dropdown-menu" style="left: -34px">
                      <li><a class="dropdown-item" href="{ Views.Auth.Logout.to_string() }">Logout</a></li>
                    </ul>
                </div>
            {:else}
            <ul class="navbar-nav mb-2 mb-lg-0">
                {#if internal_login_enabled}
                <a class="nav-link" href="{ Views.Auth.SignUp.to_string() }">Sign up</a>
                {/if}
                <li class="nav-item">
                    <a class="nav-link" href="{ external_login_page.to_string() }">Log in</a>
                </li>
            </ul>
            {/if}
        </div>
    </div>
</nav>

<style lang="less">

</style>
