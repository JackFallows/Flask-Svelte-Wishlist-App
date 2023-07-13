<script lang="ts">
    interface $$Props {
        wishlist_id: number;
    }

    interface IWishlist {
        name: string;
    }

    export let wishlist_id: number;

    let loading_promise = load_wishlist();

    let wishlist_name: string;

    async function load_wishlist() {
        if (wishlist_id == null) {
            return;
        }

        const wishlist_response = await fetch(`/api/wishlists/get/${wishlist_id}`);

        if (wishlist_response.ok) {
            const wishlist = await (wishlist_response.json() as Promise<IWishlist>);

            wishlist_name = wishlist.name;
        }
    }

    async function save_wishlist() {
        if (wishlist_id == null) {
            // create new
            const create_response = await fetch(`/api/wishlists/post`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: wishlist_name ?? "My wishlist" })
            });

            if (create_response.ok) {
                const wishlist = await create_response.json();
                location.href = `/edit/${wishlist.id}`;
            }
        } else {
            // update existing
        }
    }
</script>

{#await loading_promise}
<p>Loading...</p>
{:then}
<div class="form-container">
    <div class="form-section-left">
        <div class="mb-3">
            <label class="form-label" for="wishlist-name">Wishlist name</label>
            <input class="form-control" id="wishlist-name" placeholder="My wishlist" bind:value={wishlist_name} />
        </div>
    </div>
    <div class="form-section-right">
        <button class="btn btn-outline-success" style="margin-bottom: 0" on:click={save_wishlist}>Save wishlist</button>
    </div>
</div>
{/await}

<style lang="less">
    .form-container {
        display: flex;

        padding-top: 20px;

        .form-section-left {
            flex-grow: 1;
            padding-right: 120px;
        }

        .form-section-right {
            flex-grow: 0;
            right: 8px;
            position: fixed;
        }
    }
</style>