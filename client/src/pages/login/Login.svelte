<script lang="ts">
    import { getContext } from 'svelte';
    import { makeRoutes } from '../../routes';
    import GoogleSignInButton from '../../components/GoogleSignInButton.svelte';

    const { Post } = <IHttp>getContext("http");
    const { Views, Api } = makeRoutes(window.base_path);

    let email: string = "";
    let password: string = "";

    let loading_promise: Promise<IHttpResult<void>>;

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
<div class="flex flex-col space-y-3 md:flex-row md:items-center md:space-x-10">
    <div>
        <h1 class="text-2xl">Log in</h1>

        <div class="mb-2">
            <label class="" for="email">Email address</label><br />
            <input class="text-input md:w-96" id="email" type="email" bind:value={email} />
        </div>
        
        <div class="mb-2">
            <label class="" for="password">Password</label><br />
            <input class="text-input md:w-96" id="password" type="password" bind:value={password} />
        </div>
        
        <button class="button" on:click={internal_login}>Log in</button>
    </div>
    <div class="text-center md:text-left">
        <span class="text-4xl text-purple-600">OR</span>
    </div>
    <div class="text-center md:text-left">
        <GoogleSignInButton href={ Views.Auth.External.Login.to_string() } />
    </div>
</div>



{/await}
