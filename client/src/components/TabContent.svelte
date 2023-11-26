<script lang="ts">
    import { getContext } from "svelte";

    export let id: string;
    export let label: string;
    export let icon: string = null;

    let active: boolean = false;

    const obj: ITabContent = {
        id,
        label,
        icon,
        activate() {
            active = true;
        },
        deactivate() {
            active = false;
        }
    }

    const add_tab_content: (tab_content: ITabContent) => void = getContext("add_tab_content");
    const tabs_no_content: boolean = getContext("tabs_no_content");

    add_tab_content(obj);
</script>

<div class="{active && !tabs_no_content ? "block p-2" : "hidden"}">
    <slot></slot>
</div>
