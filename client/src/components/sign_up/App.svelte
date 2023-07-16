<script lang="ts">
    import { Post } from "../../http";
    import { Api, Views } from "../../routes";

    let email: string = "";
    let name: string = "";
    let password1: string = "";
    let password2: string = "";

    let loading_promise: Promise<void> = null;

    async function sign_up() {
        const payload = {
            email,
            name,
            password1,
            password2
        };

        loading_promise = Post(Api.Users.Create, payload);

        await loading_promise;

        await new Promise(() => {
            location.href = Views.Home
        });
    }
</script>

{#await loading_promise}
Loading...
{:then} 
<label for="email" class="form-label">Email address</label>
<input type="email" class="form-control" id="email" bind:value={email} />

<label for="name" class="form-label">Name</label>
<input type="text" class="form-control" id="name" bind:value={name} />

<label for="password1" class="form-label">Password</label>
<input type="password" class="form-control" id="password1" bind:value={password1} />

<label for="password2" class="form-label">Confirm password</label>
<input type="password" class="form-control" id="password2" bind:value={password2} />

<button class="btn btn-success" id="sign-up" on:click={sign_up}>Sign up</button>
{/await}
