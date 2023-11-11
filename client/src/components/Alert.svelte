<script lang="ts">
    import { AlertColor } from "../enums";

    export let color: AlertColor;

    let bg_color: string;
    $: {
        switch (color) {
            case AlertColor.YELLOW:
                bg_color = "bg-yellow-300 dark:bg-yellow-700";
                break;
            case AlertColor.BLUE:
                bg_color = "bg-blue-200 dark:bg-blue-800";
                break;
        }
    }
</script>

<div class="{bg_color} p-6 my-2 rounded flex space-x-6 items-center">
    <span class="fa-solid fa-circle-info text-2xl"></span>
    <div>
        <slot></slot>
    </div>
</div>
