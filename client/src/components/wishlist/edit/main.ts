import App from './App.svelte';

const app = new App({
	target: document.getElementById("app-content"),
	props: {
		wishlist_id: window.wishlist_id
	}
});

export default app;
