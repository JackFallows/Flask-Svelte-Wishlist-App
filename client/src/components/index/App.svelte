<script lang="ts">
	import '../../tailwind.css';

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

		wishlists = (await Get<IWishlist[]>(Api.Wishlists.GetAllForUser)).get_json();
		shared_wishlists = (await Get<IWishlistShare[]>(Api.Wishlists.GetSharedWithUser)).get_json();
	}
</script>

<main>
	{#if !user_is_authenticated}
	<h1 class="text-purple-600">Hello there!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	{:else}
	<h1 class="text-purple-600">Hello {name}!</h1>
	{/if}
</main>

{#if user_is_authenticated}
{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="flex flex-col space-y-3 md:flex-row md:space-x-3 md:space-y-0">
	<div class="grow">
		<div class="rounded-md border-2 border-slate-200">
			<div class="bg-slate-200 text-center p-2">
				<h2>Your wishlists</h2>
			</div>
			<div class="p-2">
				{#if wishlists.length === 0}
				<div class="text-center">
					<p>You have no wishlists. Click the button below to create one.</p>
					<a class="button" href="{Views.Wishlist.Create.to_string()}" id="no-wishlists-create-button">Create wishlist</a>
				</div>
				{:else}
				<div class="">
					{#each wishlists as w (w.id)}
					<div class="">
						<Wishlist wishlist={w} on:delete={() => loading_promise = get_wishlists()} />
					</div>
					{/each}
				</div>
				{/if}
			</div>
		</div>
	</div>
	{#if shared_wishlists.length > 0}
	<div class="grow">
		<div class="rounded-md border-2 border-slate-200">
			<div class="bg-slate-200 text-center p-2">
				<h2>Friends' lists</h2>
			</div>
			<div class="p-2">
				{#each shared_wishlists as shared_wishlist(shared_wishlist.id)}
				<div class="card">
					<div class="card-body">
						<p class="card-title">{shared_wishlist.owner_name}</p>
						<p class="card-subtitle mb-2 text-body-secondary">{shared_wishlist.owner_email}</p>
						<Wishlist wishlist={shared_wishlist} is_third_party />
					</div>
				</div>
				{/each}
			</div>
		</div>
	</div>
	{/if}
</div>
{/await}
{/if}

<style lang="postcss">
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
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
