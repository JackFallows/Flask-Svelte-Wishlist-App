<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import IconButton from "./IconButton.svelte";

    export let id: string;

    let container: HTMLElement;
    const dispatch = createEventDispatcher();

    let do_not_move: boolean = false;

    function move_to_top() {
        move("move_to_top");
    }

    function move_up() {
        move("move_up");
    }

    function move_down() {
        move("move_down");
    }

    function move_to_bottom() {
        move("move_to_bottom");
    }

    function move(event: string) {
        if (do_not_move) {
            do_not_move = false;
            return;
        }

        dispatch(event);
    }
    
    function touch_start() {
        const computedStyle = window.getComputedStyle(container);
        if (computedStyle.overflow === "hidden") {
            do_not_move = true;
        }
    }
</script>

<div bind:this={container} class="bg-white rounded-full relative min-w-[40px] h-[76px] overflow-hidden hover:overflow-visible" on:touchstart={touch_start}>
    <div class="absolute flex flex-col space-y-1 -top-9 bg-white p-1 right-0 rounded-full hover:outline hover:outline-1 hover:outline-slate-200">
        <IconButton id="{id}-move-top-button" icon="fa-solid fa-angles-up" label="Move to top" small on:click={move_to_top} />
        <IconButton id="{id}-move-up-button" icon="fa-solid fa-angle-up" label="Move up" small on:click={move_up} />
        <IconButton id="{id}-move-down-button" icon="fa-solid fa-angle-down" label="Move down" small on:click={move_down} />
        <IconButton id="{id}-move-bottom-button" icon="fa-solid fa-angles-down" label="Move to bottom" small on:click={move_to_bottom} />
    </div>
</div>
