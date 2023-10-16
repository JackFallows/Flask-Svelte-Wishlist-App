<script lang="ts">
    import '../tailwind.css';
    import { setContext } from 'svelte';
    
    let collapses: (() => void)[] = [];

    function register_collapse(collapse: () => void) {
        if (!collapses.includes(collapse)) {
            collapses.push(collapse);
        }
    }

    function collapse_all() {
        for (const collapse of collapses) {
            collapse();
        }
    }

    setContext("register_collapse", register_collapse);
    setContext("collapse_all", collapse_all);
</script>

<div class="flex flex-col space-y-1">
    <slot></slot>
</div>
