<script lang="ts">
    import { Views } from '../routes';

    export let wishlist: IWishlist;
</script>

<div class="mb-3" id="wishlist-{wishlist.id}">
    <button class="btn btn-outline-danger wishlist-button" on:click={() => location.href = Views.Edit.append(wishlist.id).to_string()}>
        <h2>{wishlist.name}</h2>
    </button>
</div>

<style lang="less">
    .wishlist-button {
        width: 100%;
    }
</style>
