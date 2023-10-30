<script lang="ts">
    import { getContext } from "svelte";

    export let id: string;
    export let label: string;

    let active: boolean = false;

    const obj: ITabContent = {
        id,
        label,
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
