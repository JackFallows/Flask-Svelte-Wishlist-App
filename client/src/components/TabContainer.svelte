<script lang="ts">
    import { setContext } from "svelte";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    let tabs: ITab[] = [];
    let tab_contents: ITabContent[] = [];

    let active_tab: ITab;
    let active_tab_content: ITabContent;

    setContext("add_tab_content", (tab_content: ITabContent) => {
        const tab: ITab = { id: tab_content.id, label: tab_content.label };
        tabs.push(tab)
        tab_contents.push(tab_content);

        if (tab_contents.length === 1) {
            active_tab = tab;
            active_tab_content = tab_content;
            tab_content.activate();
        }
    });

    function activate_tab(tab: ITab) {
        if (tab == active_tab) {
            return;
        }

        active_tab_content?.deactivate();
        active_tab = tab;
        active_tab_content = tab_contents.find(tc => tc.id === tab.id);
        active_tab_content.activate();

        dispatch("change_tab", active_tab);
    }
</script>

<div>
    <div class="px-2 pt-2 bg-slate-200 dark:bg-slate-700 flex space-x-3 items-center">
        {#each tabs as tab(tab)}
            <div class="p-3 {active_tab.id === tab.id ? "bg-white dark:bg-slate-600 rounded-t-xl" : ""}">
                <button class="{active_tab.id !== tab.id ? "hover:text-purple-600 dark:hover:text-purple-300 hover:underline" : "cursor-default"}" on:click={() => activate_tab(tab)}>{tab.label}</button>
            </div>
        {/each}
    </div>
    <div class="p-2">
        <slot></slot>
    </div>
</div>
