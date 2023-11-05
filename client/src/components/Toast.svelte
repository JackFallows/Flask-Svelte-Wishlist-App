<script lang="ts">
    import { fade } from "svelte/transition";
    import { ToastType } from "../enums";

    let visible: boolean = false;
    let message = null;
    let bg_color: string;
    let text_color: string;
    let icon: string;

    let timeout: NodeJS.Timeout = null;

    export function show(msg: string, type: ToastType) {
        if (timeout) {
            clearTimeout(timeout);
            timeout = null;
        }

        message = msg;

        switch (type) {
            case ToastType.INFO:
                bg_color = "bg-slate-800";
                text_color = "text-white";
                icon = "fa-info";
                break;
            case ToastType.SUCCESS:
                bg_color = "bg-green-600";
                text_color = "text-white";
                icon = "fa-check";
                break;
        }

        visible = true;

        timeout = setTimeout(function () {
            visible = false;
            timeout = null;
        }, 5000);
    }
</script>

{#if visible}
    <div class="absolute right-4 bottom-4 rounded shadow-lg {bg_color} {text_color} px-8 py-4 text-xl flex items-center space-x-3 z-10" in:fade={{ duration: 100 }} out:fade={{ duration: 1000 }}>
        <span class="fa-solid {icon}"></span>
        <span>
            {message}
        </span>
    </div>
{/if}
