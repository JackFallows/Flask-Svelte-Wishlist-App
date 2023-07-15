import NavBar from './NavBar.svelte';

const nav_bar = new NavBar({
	target: document.getElementById("nav-content"),
	props: {
		name: window.user_name,
        profile_pic: window.profile_pic
	}
});

export default nav_bar;
