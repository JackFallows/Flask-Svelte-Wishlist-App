<script lang="ts">
    import '../../tailwind.css';

    import { getContext } from 'svelte';
    import { makeRoutes } from "../../routes";
    import GoogleSignInButton from '../../components/GoogleSignInButton.svelte';

    const { Post } = <IHttp>getContext("http");
    const { Api, Views } = makeRoutes(window.base_path);

    let email: string = "";
    let name: string = "";
    let password1: string = "";
    let password2: string = "";

    let loading_promise: Promise<any> = null;

    async function sign_up() {
        const payload = {
            email,
            name,
            password1,
            password2
        };

        const response = await Post(Api.Users.Create, payload);

        if (response.ok) {
            await new Promise(() => {
                location.href = Views.Home
            });

            return;
        }

        console.error(response.get_error<IValidationState>());
    }
</script>

{#await loading_promise}
Loading...
{:then}
<div class="flex flex-col space-y-3 md:flex-row md:items-center md:space-x-10">
    <div>
        <h1 class="text-2xl">Sign up</h1>
        <div class="mb-2">
            <label for="email" class="">Email address</label><br />
            <input type="email" class="text-input md:w-96" id="email" bind:value={email} />
        </div>

        <div class="mb-2">
            <label for="name" class="">Name</label><br />
            <input type="text" class="text-input md:w-96" id="name" bind:value={name} />
        </div>

        <div class="mb-2">
            <label for="password1" class="">Password</label><br />
            <input type="password" class="text-input md:w-96" id="password1" bind:value={password1} />
        </div>

        <div class="mb-2">
            <label for="password2" class="">Confirm password</label><br />
            <input type="password" class="text-input md:w-96" id="password2" bind:value={password2} />
        </div>

        <button class="success-button" id="sign-up" on:click={() => loading_promise = sign_up()}>Sign up</button>
    </div>
    <div class="text-center md:text-left">
        <span class="text-4xl text-purple-600">OR</span>
    </div>
    <div class="text-center md:text-left">
        <GoogleSignInButton href={ Views.Auth.External.Login.to_string() } />
    </div>
</div>
{/await}
