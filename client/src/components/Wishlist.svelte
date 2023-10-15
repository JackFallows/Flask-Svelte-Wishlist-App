<script lang="ts">
    import '../tailwind.css';

    import { createEventDispatcher } from 'svelte';
    import { Delete, Patch } from '../http';
    import { makeRoutes } from '../routes';
    import Modal from './Modal.svelte';
    import Collapse from './Collapse.svelte';
    import Accordion from './Accordion.svelte';

    export let wishlist: IWishlist;
    export let is_third_party: boolean = false; // someone shared it with us

    const { Views, Api } = makeRoutes(window.base_path);

    let delete_modal: Modal;
    let share_modal: Modal;
    let share_accordion: Accordion;
    let is_sharing_to_user: boolean = true;
    let share_link: string = null;

    function sharing_to_user_change(e: { detail: { collapsed: boolean } }) {
        is_sharing_to_user = !e.detail.collapsed;
    }

    let share_email: string;

    const dispatch = createEventDispatcher();

    async function share_wishlist() {
        const confirmed = await share_modal.show();
        if (!confirmed) {
            return;
        }

        await Patch(Api.Wishlists.PatchShare, {
            wishlist_id: wishlist.id,
            email: share_email
        });

        share_email = "";

        dispatch('shared');
    }

    async function get_share_link() {
        const result = await Patch<any, { share_guid: string }>(Api.Wishlists.PatchShareLink.append(wishlist.id), {});
        const json = result.get_json();
        share_link = `${location.origin}/share/${json.share_guid}`;
    }

    async function delete_wishlist() {
        const confirmed = await delete_modal.show();
        if (!confirmed) {
            return;
        }

        await Delete(Api.Wishlists.Delete.append(wishlist.id), null);

        dispatch('delete');
    }
</script>

<div class="flex flex-nowrap space-x-3 w-full" id="wishlist-{wishlist.id}">
    <button class="button grow flex items-center relative" on:click={() => location.href = Views.Wishlist.View.append(wishlist.id).to_string()}>
        {#if wishlist.shared}
        <span class="fa-solid fa-users absolute right-2.5"></span>
        {/if}
        <h2 class="grow">{wishlist.name}</h2>
    </button>
    {#if !is_third_party}
    <button class="icon-button" aria-label="Share button" on:click={share_wishlist}>
        <span class="fa-solid fa-share-nodes"></span>
    </button>
    <button class="icon-button" aria-label="Delete button" on:click={delete_wishlist}>
        <span class="fa-solid fa-trash" style="pointer-events: none;"></span>
    </button>
    {/if}
</div>


<Modal bind:this={delete_modal} id="delete-{wishlist.id}" is_danger={true}>
    <span slot="header">
        Are you sure?
    </span>
    <span slot="body">
        This action cannot be undone.
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        <button class="danger-button" on:click={() => close("true")}>Delete</button>
    </span>
</Modal>

<Modal bind:this={share_modal} id="share-{wishlist.id}" is_wide={true}>
    <span slot="header">
        Share wishlist '{wishlist.name}'
    </span>
    <span slot="body">
        <Accordion bind:this={share_accordion}>
            <Collapse heading="Share to existing user" bind:accordion={share_accordion} on:collapse_change={sharing_to_user_change}>
                <p>
                    Enter the email address of the user with whom you want to share this wishlist (the user must already have an account on this site):
                    <input type="email" class="text-input" style="width: 100%" bind:value={share_email} />
                </p>
                <p>
                    Please be aware that <b>the recipient will gain visibility of the name and email address of the sender</b> (that's you!).<br />
                    Only share wishlists with those you trust with this information.
                </p>
            </Collapse>
            <Collapse heading="Share with link" collapsed={true} bind:accordion={share_accordion}>
                <p>Click the button below to generate a unique link to your wishlist which you can share with people who do not have an account on this website.</p>
                {#if !share_link}
                <button class="button" on:click={get_share_link}>Get link</button>
                {:else}
                <input type="text" class="text-input" style="width: 100%" readonly bind:value={share_link} />
                <button class="button mt-1" on:click={() => navigator.clipboard.writeText(share_link)}>Copy to clipboard</button>
                {/if}
            </Collapse>
        </Accordion>
    </span>
    <span slot="buttons" let:close_modal={close}>
        <button class="button" on:click={() => close()}>Cancel</button>
        {#if is_sharing_to_user}
        <button class="button" on:click={() => close("true")}>Ok</button>
        {/if}
    </span>
</Modal>

<style lang="less">
    
</style>
