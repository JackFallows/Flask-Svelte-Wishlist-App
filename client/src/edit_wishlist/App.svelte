<script lang="ts">
    import { onMount } from 'svelte';

    interface $$Props {
        wishlist_id: number;
    }

    export let wishlist_id: number;

    let is_loading: boolean = false;

    onMount(async () => {
        if (wishlist_id == null) {
            return;
        }

        is_loading = true;
        // TODO
        is_loading = false;
    })
</script>

<button class="btn btn-outline-success" style="margin-bottom: 0">Save wishlist</button>
