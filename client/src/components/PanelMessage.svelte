<script lang="ts">
    export let highlighted: boolean = false;

    let border_color: string = highlighted
        ? "border-blue-200 dark:border-blue-600"
        : "border-slate-200 dark:border-slate-800";
    let bg_color: string = highlighted
        ? "bg-blue-200 dark:bg-blue-600"
        : "bg-slate-200 dark:bg-slate-800";

</script>

{#if $$slots.body}
    <div class="border {border_color} rounded-md p-2">
        <p class="{bg_color} px-2 py-1 -mx-2 -mt-2 mb-2 text-xs text-slate-600 dark:text-slate-100">
            <slot name="heading"></slot>
        </p>
        <slot name="body"></slot>
    </div>
{:else}
    <div class="border {border_color} {bg_color} px-2 py-1 rounded-md text-slate-600 dark:text-slate-100 text-xs">
        <slot name="heading"></slot>
    </div>
{/if}
