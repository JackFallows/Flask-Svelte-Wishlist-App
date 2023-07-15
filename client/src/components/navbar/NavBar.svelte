<script lang="ts">
    import { Views } from '../../routes'

    export let name: string;
    export let profile_pic: string;

    const user_is_authenticated = name != null;
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
                    <a class="nav-link active" aria-current="page" href="/">Home</a>
                </li>
            </ul>
            {#if user_is_authenticated}
                <a class="btn btn-outline-primary me-2" style="margin-bottom: 0" href="/edit">Create wishlist</a>
                <div class="dropdown">
                    <button class="btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Hi, { name }
                        <img src="{ profile_pic }" alt="Profile pic" width="24" height="24" class="d-inline-block align-text-top" style="border-radius: 20px">
                    </button>
                    <ul class="dropdown-menu">
                      <li><a class="dropdown-item" href="{ Views.Auth.Logout.to_string() }">Logout</a></li>
                    </ul>
                </div>
            {:else}
            <ul class="navbar-nav mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link" href="{ Views.Auth.External.Login.to_string() }">Log in</a>
                </li>
            </ul>
            {/if}
        </div>
    </div>
</nav>

<style lang="less">

</style>
