<script lang="ts">
    import { setContext, createEventDispatcher } from "svelte";

    export let no_content: boolean = false;
    export let light: boolean = false;

    const dispatch = createEventDispatcher();

    let tabs: ITab[] = [];
    let tab_contents: ITabContent[] = [];

    let active_tab: ITab;
    let active_tab_content: ITabContent;

    setContext("add_tab_content", (tab_content: ITabContent) => {
        const tab: ITab = { id: tab_content.id, label: tab_content.label, icon: tab_content.icon };
        tabs.push(tab)
        tab_contents.push(tab_content);

        if (tab_contents.length === 1) {
            active_tab = tab;
            active_tab_content = tab_content;
            tab_content.activate();
        }
    });

    setContext("tabs_no_content", no_content);

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
    <div class="px-2 pt-2 {light ? "bg-transparent" : "bg-slate-200 dark:bg-slate-700"} flex space-x-3 items-center">
        {#each tabs as tab(tab)}
            <div class="p-3 {active_tab.id === tab.id ? `${light ? "bg-slate-200" : "bg-white"} dark:bg-slate-600 rounded-t-xl` : ""}">
                <button class="{active_tab.id !== tab.id ? "hover:text-purple-600 dark:hover:text-purple-300 hover:underline" : "cursor-default"}" on:click={() => activate_tab(tab)}>
                    {#if tab.icon}
                        <span class="{tab.icon}" title="{tab.label}"></span>
                    {:else}
                        {tab.label}
                    {/if}
                </button>
            </div>
        {/each}
    </div>
    <slot></slot>
</div>
