<script lang="ts">
	import '../../tailwind.css';

    import { getContext } from 'svelte';
    import { makeRoutes } from "../../routes";
    import { AlertColor } from '../../enums';
    import Alert from '../../components/Alert.svelte';

    const { Get, Patch } = <IHttp>getContext("http");
	const { Api, Views } = makeRoutes(window.base_path);

    let user_name: string;
    let email: string;
    let email_on_share: boolean;
    let email_on_update: boolean;
    let email_on_owner_bought: boolean;

    let loading_promise = get_user();

    async function get_user() {
        const userPayload = await Get<IUser>(Api.Users.Get);

        const user = userPayload.get_json();

        user_name = user.name;
        email = user.email;
        email_on_share = user.email_on_share;
        email_on_update = user.email_on_update;
        email_on_owner_bought = user.email_on_owner_bought;
    }

    async function save_user() {
        const payload = {
            email_on_share,
            email_on_update,
            email_on_owner_bought
        };

        const response = await Patch(Api.Users.Update, payload);

        if (response.ok) {
            await new Promise(() => {
                location.href = Views.Home
            });

            return;
        }

        console.error(response.get_error<IValidationState>());
    }

</script>

<div class="dark:text-slate-100 pt-4">
    {#await loading_promise}
        Loading...
    {:then}
        <main>
            <h1 class="text-2xl">{user_name}</h1>
            <p>{email}</p>
            <hr />

            <div class="my-8">
                <h2 class="text-xl">Email notifications</h2>

                {#if window.email_is_configured}
                    <label for="email-on-share-checkbox">Receive an email notification when a wishlist is shared with you?</label>
                    <input id="email-on-share-checkbox" type="checkbox" name="email_on_share" bind:checked={email_on_share} />
                    <br />

                    <label for="email-on-update-checkbox">Receive an email notification when a wishlist that has already been shared with you is updated?</label>
                    <input id="email-on-update-checkbox" type="checkbox" name="email_on_update" bind:checked={email_on_update} />
                    <br />

                    <label for="email-on-owner-bought-checkbox">Receive an email notification when the owner of a wishlist shared with you buys an item that you previously bought yourself?</label>
                    <input id="email-on-owner-bought-checkbox" type="checkbox" name="email_on_owner_bought" bind:checked={email_on_owner_bought} />

                    <div>
                        <button class="success-button mt-8" id="save-button" on:click={() => loading_promise = save_user()}>Save</button>
                    </div>
                {:else}
                    <Alert color={AlertColor.YELLOW}>
                        <p>Email notifications are unavailable due to system configuration.</p>
                    </Alert>
                {/if}
            </div>
        </main>
    {/await}
</div>
