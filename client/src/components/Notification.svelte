<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Patch } from "../http";
    import { makeRoutes } from "../routes";
    import { NotificationType } from "../enums";

    export let notification: INotificationDto;

    const { Api } = makeRoutes(window.base_path);

    let dispatch = createEventDispatcher();

    async function read_notification(): Promise<void> {
        await Patch(Api.Notifications.PatchRead.append(notification.id), null);

        dispatch("notification_changed");
    }

    async function accept_share(): Promise<void> {
        await Patch(Api.Notifications.PatchAcceptShare.append(notification.id), null);
        dispatch("notification_changed");
    }

    async function reject_share(): Promise<void> {
        await Patch(Api.Notifications.PatchRejectShare.append(notification.id), null);
        dispatch("notification_changed");
    }
</script>

<div class="border-[1px] border-slate-200 rounded-md p-2">
    <p class="bg-slate-200 px-2 py-1 -mx-2 -mt-2 mb-2 text-xs text-slate-600 flex items-center">
        <span class="flex-grow">
            {notification.created_at.toLocaleString()}
        </span>
        {#if notification.type !== NotificationType.SHARE}
        <button class="hover:text-purple-600 text-sm" on:click={() => read_notification()}>
            <span class="fa-solid fa-xmark"></span>
        </button>
        {/if}
    </p>
    <p>{notification.message}</p>
    {#if notification.type === NotificationType.SHARE && notification.shared_wishlist_id != null}
    <p>Accept?</p>
    <div class="inline-block">
        <div class="button-group">
            <button class="button" on:click={() => accept_share()}>
                <span class="fa-solid fa-check"></span> Yes
            </button>
            <button class="button" on:click={() => reject_share()}>
                <span class="fa-solid fa-xmark"></span> No
            </button>
        </div>
    </div>
    {/if}
</div>
