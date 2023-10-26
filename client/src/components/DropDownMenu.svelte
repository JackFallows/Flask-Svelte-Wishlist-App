<script lang="ts">
    import '../tailwind.css';

    export let button: HTMLElement;
    export let classes: string = '';
    export let left: boolean = false;

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

<div class="relative">
    <div class="{visible ? 'block' : 'hidden'} absolute {left ? "right-0" : "left-0"} min-w-max bg-white shadow-lg border-slate-400 border p-2 rounded-md {classes}" bind:this={dropdown}>
        <slot>
        </slot>
    </div>
</div>
