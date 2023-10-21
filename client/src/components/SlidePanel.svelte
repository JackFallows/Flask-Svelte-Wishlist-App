<script lang="ts">
    import { fly } from "svelte/transition";

    export let visible: boolean = false;
</script>

{#if visible}
    <div class="absolute w-96 right-0 top-[64px] full-height border-l-[1px] border-slate-200 bg-white p-2 shadow-lg overflow-y-scroll" transition:fly={{ x: 100, duration: 100 }}>
        <slot></slot>
    </div>
{/if}

<style lang="less">
    .full-height {
        height: ~"calc(100vh - 64px)";
    }
</style>
