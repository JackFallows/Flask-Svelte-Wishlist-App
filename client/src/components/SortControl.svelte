<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import IconButton from "./IconButton.svelte";

    export let id: string;
    export let move_far: boolean = false;
    export let has_background: boolean = false;

    const dispatch = createEventDispatcher();

    type move_type = "move_up" | "move_down";

    function move(where: move_type) {
        dispatch(where);
    }
</script>

<div class="{has_background ? "bg-slate-200 dark:bg-slate-800" : "bg-transparent"} rounded-full min-w-[40px] h-[76px] flex flex-col items-center justify-between py-1">
    <IconButton id="{id}-move-up-button" icon="fa-solid {move_far ? "fa-angles-up" : "fa-angle-up"}" label="Move {move_far ? "to top" : "up"}" small on:click={() => move("move_up")} />
    <IconButton id="{id}-move-down-button" icon="fa-solid {move_far ? "fa-angles-down" : "fa-angle-down"}" label="Move {move_far ? "to bottom" : "down"}" small on:click={() => move("move_down")} />
</div>
