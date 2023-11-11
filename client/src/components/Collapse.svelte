<script lang="ts">
    import '../tailwind.css';
    import { createEventDispatcher, getContext } from 'svelte';
    
	const dispatch = createEventDispatcher();

    let accordion_register_collapse: (collapse_func: () => void) => void = getContext('register_collapse');
    let accordion_collapse_all: () => void = getContext('collapse_all');

    export let heading: string;
    export let collapsed: boolean = false;
    export let subtle: boolean = false;

    function collapse() {
        collapsed = true;
        dispatch('collapse_change', { collapsed });
    }

    if (accordion_register_collapse) {
        accordion_register_collapse(collapse);
    }

    function toggle() {
        if (accordion_collapse_all && collapsed) {
            accordion_collapse_all();
            collapsed = false;
        } else {
            collapsed = !collapsed;
        }

        dispatch('collapse_change', { collapsed });
    }
</script>

<div class="w-full">
    <button class="{subtle ? 'hover:text-purple-600 dark:hover:text-purple-300' : 'bg-slate-200'} p-2 w-full flex justify-between" on:click={() => toggle()}>
        <span class="{subtle ? 'text-sm' : 'text-xl'}">{heading}</span>
        <span class="{subtle ? 'text-base' : 'text-2xl'} fa-solid {collapsed ? 'fa-chevron-down' : 'fa-chevron-up'}"></span>
    </button>
    <div class="overflow-y-hidden transition-all duration-300 {collapsed ? 'max-h-0' : 'max-h-96'}">
        <div class="{subtle ? 'p-2' : 'p-1 border-r-2 border-b-2 border-l-2 border-slate-200'}">
            <slot></slot>
        </div>
    </div>
</div>
