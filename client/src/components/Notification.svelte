<script lang="ts">
    import { createEventDispatcher, getContext } from "svelte";
    import { makeRoutes } from "../routes";
    import { NotificationType } from "../enums";
    import PanelMessage from "./PanelMessage.svelte";

    export let notification: INotificationDto;

    const { Patch } = <IHttp>getContext("http");
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

<PanelMessage>
    <div slot="heading" class="flex items-center">
        <span class="flex-grow">
            {notification.created_at.toLocaleString()}
        </span>
        {#if notification.type !== NotificationType.SHARE}
        <button class="hover:text-purple-600 dark:hover:text-purple-300 text-sm" on:click={() => read_notification()}>
            <span class="fa-solid fa-xmark fa-fw"></span>
        </button>
        {/if}
    </div>
    <div slot="body">
        <p>{notification.message}</p>
        {#if notification.type === NotificationType.SHARE && notification.shared_wishlist_id != null}
        <p class="mt-3 mb-1">Accept?</p>
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
</PanelMessage>
