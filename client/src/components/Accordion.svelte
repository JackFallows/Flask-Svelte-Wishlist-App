<script lang="ts">
    import '../tailwind.css';
    
    let collapses: (() => void)[] = [];

    export function register_collapse(collapse: () => void) {
        if (!collapses.includes(collapse)) {
            collapses.push(collapse);
        }
    }

    export function collapse_all() {
        for (const collapse of collapses) {
            collapse();
        }
    }
</script>

<div class="flex flex-col space-y-1">
    <slot></slot>
</div>
