<script lang="ts">
    export let wishlist_item: IWishlistItem;

    const html_id = `wishlist-item-${wishlist_item.id ?? "new"}`
    
    let link: string = wishlist_item.link;
    let notes: string = wishlist_item.notes;
    let bought: boolean = wishlist_item.bought;

    $: {
        wishlist_item.link = link;
        wishlist_item.notes = notes;
        wishlist_item.bought = bought;
    }
</script>

<div class="alert alert-secondary" id="{html_id}">
    <input class="form-control" bind:value={link} id="{html_id + "-link"}" placeholder="Item link or name" />
    <textarea class="form-control" bind:value={notes} id="{html_id + "-notes"}" placeholder="Notes"></textarea>
</div>

<style lang="less">

</style>
