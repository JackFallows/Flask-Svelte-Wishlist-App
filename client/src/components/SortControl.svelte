<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import IconButton from "./IconButton.svelte";

    export let id: string;

    const dispatch = createEventDispatcher();

    function move_to_top() {
        dispatch("move_to_top");
    }

    function move_up() {
        dispatch("move_up");
    }

    function move_down() {
        dispatch("move_down");
    }

    function move_to_bottom() {
        dispatch("move_to_bottom");
    }
</script>

<div class=" bg-white rounded-full relative min-w-[40px] h-[76px] overflow-hidden hover:overflow-visible">
    <div class="absolute flex flex-col space-y-1 -top-9 bg-white p-1 right-0 rounded-full hover:outline hover:outline-1 hover:outline-slate-200">
        <IconButton id="{id}-move-top-button" icon="fa-solid fa-angles-up" label="Move to top" small on:click={move_to_top} />
        <IconButton id="{id}-move-up-button" icon="fa-solid fa-angle-up" label="Move up" small on:click={move_up} />
        <IconButton id="{id}-move-down-button" icon="fa-solid fa-angle-down" label="Move down" small on:click={move_down} />
        <IconButton id="{id}-move-bottom-button" icon="fa-solid fa-angles-down" label="Move to bottom" small on:click={move_to_bottom} />
    </div>
</div>
