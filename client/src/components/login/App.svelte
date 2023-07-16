<script lang="ts">
    import { Post } from '../../http';
    import { Views, Api } from '../../routes';

    let email: string = "";
    let password: string = "";

    let loading_promise: Promise<void>;

    async function external_login() {
        loading_promise = new Promise(() => {
            location.href = Views.Auth.External.Login.to_string();
        });

        await loading_promise;
    }

    async function internal_login() {
        const payload = {
            email,
            password
        };

        loading_promise = Post(Api.Users.Authenticate, payload);

        await loading_promise;

        await new Promise(() => {
            location.href = Views.Home;
        });
    }
</script>

{#await loading_promise}
Loading...
{:then}
<button class="btn btn-outline-danger" on:click={external_login}>Log in with Google</button>

<h2>Or</h2>

<label class="form-label" for="email">Email address</label>
<input class="form-control" id="email" type="email" bind:value={email} />

<label class="form-label" for="password">Password</label>
<input class="form-control" id="password" type="password" bind:value={password} />

<button class="btn btn-primary" on:click={internal_login}>Log in</button>
{/await}
