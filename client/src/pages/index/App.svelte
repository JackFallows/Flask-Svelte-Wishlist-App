<script lang="ts">
    import Page from "../Page.svelte";
    import Home from "./Home.svelte";

	export let name: string;
</script>

<Page>
    <Home name={name}></Home>
</Page>
