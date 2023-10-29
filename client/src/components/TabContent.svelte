<script lang="ts">
    import { getContext } from "svelte";
    
    export let for_tab_id: string;

    let active: boolean = false;

    const obj: ITabContent = {
        for_tab_id,
        activate() {
            active = true;
        },
        deactivate() {
            active = false;
        }
    }

    const add_tab_content: (tab_content: ITabContent) => void = getContext("add_tab_content");

    add_tab_content(obj);
</script>

<div class="{active ? "block" : "hidden"}">
    <slot></slot>
</div>
