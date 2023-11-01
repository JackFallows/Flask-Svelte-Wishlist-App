<script lang="ts">
	import '../../tailwind.css';

	import { getContext } from 'svelte';
	import Wishlist from '../../components/Wishlist.svelte';
    import { makeRoutes } from "../../routes";

	export let name: string;

	const { Get } = <IHttp>getContext("http");

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
		<div class="rounded-lg border border-slate-200 p-6 shadow">
			<h1 class="text-purple-600 text-4xl sm:text-6xl">Wishlist App</h1>
			<p class="text-xl mt-3">Log in or create an account to get started</p>
		</div>
		<div class="flex flex-col space-y-6 sm:flex-row sm:space-x-6 sm:space-y-0 justify-between mt-6">
			<div class="rounded-lg border border-slate-200 p-6 shadow w-[100%] sm:w-[50%]">
				<h2 class="text-purple-600 text-2xl sm:text-4xl mb-3">Create...</h2>
				<ul class="text-left text-xl">
					<li>Create multiple separate lists</li>
					<li>Add dozens of items with a link/name and optional description</li>
					<li>Arrange the items under headings, and</li>
					<li>Sort them how you'd like</li>
				</ul>
			</div>
			<div class="rounded-lg border border-slate-200 p-6 shadow w-[100%] sm:w-[50%]">
				<h2 class="text-purple-600 text-2xl sm:text-4xl mb-3">...And share</h2>
				<ul class="text-left text-xl">
					<li>Share select lists that you have created</li>
					<li>Send them directly to other users of the site, or copy a link</li>
					<li>Receive notifications when lists that have been shared with you have been updated</li>
				</ul>
			</div>
		</div>
	{:else}
		<h1 class="text-purple-600 text-4xl sm:text-6xl">Hello {name}!</h1>
	{/if}
</main>

{#if user_is_authenticated}
{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="flex flex-col space-y-3 sm:flex-row sm:space-x-3 sm:space-y-0">
	<div class="{shared_wishlists.length > 0 ? "sm:w-[50%]" : "grow"}">
		<div class="rounded-md border-2 border-slate-200">
			<div class="bg-slate-200 text-center p-2">
				<h2>Your wishlists</h2>
			</div>
			<div class="p-2">
				{#if wishlists.length === 0}
				<div class="text-center">
					<p>You have no wishlists. Click the button below to create one.</p>
					<div class="my-3">
						<a class="button" href="{Views.Wishlist.to_string()}" id="no-wishlists-create-button">Create wishlist</a>
					</div>
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
	<div class="sm:w-[50%]">
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

<style lang="less">
	main {
		text-align: center;
		padding: 1em;
		margin: 0 auto;
	}

	h1, h2 {
		text-transform: uppercase;
		font-weight: 100;
	}

	ul {
		li:not(:last-child) {
			margin-bottom: 15px;
		}
	}
</style>
