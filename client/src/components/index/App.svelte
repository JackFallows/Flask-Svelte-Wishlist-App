<script lang="ts">
	import '../../tailwind.css';

	import Wishlist from '../Wishlist.svelte';
	import { Get } from '../../http';
    import { makeRoutes } from "../../routes";

	export let name: string;

	const { Api, Views } = makeRoutes(window.base_path);

	let user_is_authenticated: boolean = name != null;

	let wishlists: IWishlist[] = [];
	let shared_wishlists: { owner_name: string, owner_email: string, wishlists: IWishlistShare[] }[] = [];
	
	let loading_promise = get_wishlists();

	async function get_wishlists() {
		if (!user_is_authenticated) {
			return;
		}

		const wishlistsPayload = await Get<IWishlist[]>(Api.Wishlists.GetAllForUser);
		const sharedWishlistsPayload = await Get<IWishlistShare[]>(Api.Wishlists.GetSharedWithUser);

		wishlists = wishlistsPayload.get_json();

		const flat_shared_wishlists = sharedWishlistsPayload.get_json();

		shared_wishlists = flat_shared_wishlists.reduce((groups, list) => {
			const existing_group = groups.find(g => g.owner_name === list.owner_name && g.owner_email === list.owner_email);
			if (existing_group) {
				existing_group.wishlists.push(list);
			} else {
				groups.push({
					owner_name: list.owner_name,
					owner_email: list.owner_email,
					wishlists: [list]
				});
			}

			return groups;
		}, []);
	}
</script>

<main>
	{#if !user_is_authenticated}
	<h1 class="text-purple-600 text-4xl sm:text-6xl">Hello there!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	{:else}
	<h1 class="text-purple-600 text-4xl sm:text-6xl">Hello {name}!</h1>
	{/if}
</main>

{#if user_is_authenticated}
{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="flex flex-col space-y-3 sm:flex-row sm:space-x-3 sm:space-y-0">
	<div class="grow">
		<div class="rounded-md border-2 border-slate-200">
			<div class="bg-slate-200 text-center p-2">
				<h2>Your wishlists</h2>
			</div>
			<div class="p-2">
				{#if wishlists.length === 0}
				<div class="text-center">
					<p>You have no wishlists. Click the button below to create one.</p>
					<a class="button" href="{Views.Wishlist.to_string()}" id="no-wishlists-create-button">Create wishlist</a>
				</div>
				{:else}
				<div class="flex flex-col space-y-3">
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
			<div class="p-2 flex flex-col space-y-3">
				{#each shared_wishlists as shared_wishlist_group}
					<div class="{shared_wishlist_group.owner_name == null ? "" : "border"} rounded-md border-slate-200 p-2 flex flex-col space-y-3">
						{#if shared_wishlist_group.owner_name != null}
							<div>
								<span class="text-base text-black">{shared_wishlist_group.owner_name}</span>
								<span class="text-sm text-slate-500">{shared_wishlist_group.owner_email}</span>
							</div>
						{/if}
						{#each shared_wishlist_group.wishlists as shared_wishlist}
							<Wishlist wishlist={shared_wishlist} is_third_party />
						{/each}
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
		margin: 0 auto;
	}

	h1 {
		text-transform: uppercase;
		font-weight: 100;
	}
</style>
