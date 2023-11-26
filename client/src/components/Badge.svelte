<script lang="ts">
    import { BadgeColor } from "../enums";

    export let color: BadgeColor;

    let bg_color: string;
    $: {
        switch (color) {
            case BadgeColor.YELLOW:
                bg_color = "bg-yellow-300 dark:bg-yellow-700";
                break;
            case BadgeColor.GREEN:
                bg_color = "bg-green-200 dark:bg-green-800";
                break;
        }
    }

</script>

<span class="rounded-full {bg_color} dark:text-white p-2 min-w-[40px] text-center whitespace-nowrap">
    <slot></slot>
</span>
