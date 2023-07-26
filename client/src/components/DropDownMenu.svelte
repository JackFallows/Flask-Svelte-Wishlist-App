<script lang="ts">
    import '../tailwind.css';

    export let button: HTMLElement;
    export let classes: string = '';

    let dropdown: HTMLElement;
    let visible: boolean = false;

    export function toggle() {
        visible = !visible;
    }

    function auto_hide(e: Event) {
        if (visible && e.target != button) {
            visible = false;
        }
    }
</script>

<svelte:window on:click={auto_hide} />

<div class="{visible ? 'block' : 'hidden'} absolute bg-white shadow-lg border-slate-400 border p-2 rounded-md {classes}" bind:this={dropdown}>
    <slot>
    </slot>
</div>
