<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import IconButton from "./IconButton.svelte";

    export let id: string;

    let container: HTMLElement;
    const dispatch = createEventDispatcher();

    type move_type = "move_to_top" | "move_up" | "move_down" | "move_to_bottom";

    function move(e: PointerEvent, where: move_type) {
        if (e.pointerType === "touch") {
            const computedStyle = window.getComputedStyle(container);
            if (computedStyle.overflow === "hidden") {
                return;
            }
        }

        dispatch(where);
    }
</script>

<div bind:this={container} class="bg-white rounded-full relative min-w-[40px] h-[76px] overflow-hidden hover:overflow-visible">
    <div class="absolute flex flex-col space-y-1 -top-9 bg-white p-1 right-0 rounded-full hover:outline hover:outline-1 hover:outline-slate-200">
        <IconButton id="{id}-move-top-button" icon="fa-solid fa-angles-up" label="Move to top" small on:pointerdown={(e) => move(e, "move_to_top")} />
        <IconButton id="{id}-move-up-button" icon="fa-solid fa-angle-up" label="Move up" small on:pointerdown={(e) => move(e, "move_up")} />
        <IconButton id="{id}-move-down-button" icon="fa-solid fa-angle-down" label="Move down" small on:pointerdown={(e) => move(e, "move_down")} />
        <IconButton id="{id}-move-bottom-button" icon="fa-solid fa-angles-down" label="Move to bottom" small on:pointerdown={(e) => move(e, "move_to_bottom")} />
    </div>
</div>
