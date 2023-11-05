{#if $$slots.body}
    <div class="border border-slate-200 rounded-md p-2">
        <p class="bg-slate-200 px-2 py-1 -mx-2 -mt-2 mb-2 text-xs text-slate-600">
            <slot name="heading"></slot>
        </p>
        <slot name="body"></slot>
    </div>
{:else}
    <div class="border border-slate-200 bg-slate-200 px-2 py-1 rounded-md text-slate-600 text-xs">
        <slot name="heading"></slot>
    </div>
{/if}
