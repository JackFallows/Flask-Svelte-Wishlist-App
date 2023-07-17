<script lang="ts">
	import Wishlist from '../Wishlist.svelte';
	import { Get } from '../../http';
    import { Api, Views } from "../../routes";

	export let name: string;

	let user_is_authenticated: boolean = name != null;

	let wishlists: IWishlist[] = [];
	let shared_wishlists: IWishlistShare[] = [];
	
	let loading_promise = get_wishlists();

	async function get_wishlists() {
		if (!user_is_authenticated) {
			return;
		}

		wishlists = await Get<IWishlist[]>(Api.Wishlists.GetAllForUser);
		shared_wishlists = await Get<IWishlistShare[]>(Api.Wishlists.GetSharedWithUser);
	}
</script>

<main>
	{#if !user_is_authenticated}
	<h1>Hello there!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	{:else}
	<h1>Hello {name}!</h1>
	{/if}
</main>

{#if user_is_authenticated}
{#await loading_promise}
<p>Loading...</p>
{:then}
<h2>Your wishlists</h2>

{#if wishlists.length === 0}
<div class="text-center">
	<p>You have no wishlists. Click the button below to create one.</p>
	<a class="btn btn-primary" href="{Views.Wishlist.Create.to_string()}" id="no-wishlists-create-button">Create wishlist</a>
</div>
{:else}
<div class="container">
	<div class="row row-cols-2">
		{#each wishlists as w (w.id)}
		<div class="col">
			<Wishlist wishlist={w} on:delete={() => loading_promise = get_wishlists()} />
		</div>
		{/each}
	</div>
</div>
{/if}

{#if shared_wishlists.length > 0}
<h2>Friends' lists</h2>
<div class="container">
	<div class="row row-cols-2">
		{#each shared_wishlists as shared_wishlist(shared_wishlist.id)}
			<div class="col">
				<div class="card">
					<div class="card-body">
						<h5 class="card-title">{shared_wishlist.owner_name}</h5>
						<h6 class="card-subtitle mb-2 text-body-secondary">{shared_wishlist.owner_email}</h6>
						<Wishlist wishlist={shared_wishlist} is_third_party />
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>
{/if}

{/await}
{/if}

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
