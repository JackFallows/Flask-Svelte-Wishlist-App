{#if $$slots.body}
    <div class="border border-slate-200 dark:border-slate-700 rounded-md p-2">
        <p class="bg-slate-200 dark:bg-slate-700 px-2 py-1 -mx-2 -mt-2 mb-2 text-xs text-slate-600 dark:text-slate-100">
            <slot name="heading"></slot>
        </p>
        <slot name="body"></slot>
    </div>
{:else}
    <div class="border border-slate-200 dark:border-slate-600 bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded-md text-slate-600 dark:text-slate-100 text-xs">
        <slot name="heading"></slot>
    </div>
{/if}
