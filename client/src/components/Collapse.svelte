<script lang="ts">
    import '../tailwind.css';
    import { createEventDispatcher } from 'svelte';
    import Accordion from './Accordion.svelte';
    
	const dispatch = createEventDispatcher();

    export let heading: string;
    export let collapsed: boolean = false;
    export let accordion: Accordion = null;

    function collapse() {
        collapsed = true;
        dispatch('collapse_change', { collapsed });
    }

    $: {
        if (accordion) {
            accordion.register_collapse(collapse);
        }
    }

    function toggle() {
        if (accordion && collapsed) {
            accordion.collapse_all();
            collapsed = false;
        } else {
            collapsed = !collapsed;
        }

        dispatch('collapse_change', { collapsed });
    }
</script>

<div>
    <button class="bg-slate-200 p-2 w-full flex justify-between" on:click={() => toggle()}>
        <span class="text-xl">{heading}</span>
        <span class="text-2xl fa-solid {collapsed ? 'fa-chevron-down' : 'fa-chevron-up'}"></span>
    </button>
    <div class="overflow-y-hidden transition-all duration-300 {collapsed ? 'max-h-0' : 'max-h-96'}">
        <div class="p-1 border-r-2 border-b-2 border-l-2 border-slate-200">
            <slot></slot>
        </div>
    </div>
</div>
