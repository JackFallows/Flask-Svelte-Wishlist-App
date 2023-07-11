import './global.css';

import App from './App.svelte';

const app = new App({
	target: document.getElementById("app-content"),
	props: {
		name: 'world'
	}
});

export default app;
