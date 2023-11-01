<script lang="ts">
    import Page from "../Page.svelte";
    import Wishlist from "./Wishlist.svelte";

    export let wishlist_id: number;
</script>

<Page>
    <Wishlist wishlist_id={wishlist_id} />
</Page>
