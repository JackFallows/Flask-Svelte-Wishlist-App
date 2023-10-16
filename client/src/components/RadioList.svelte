<script lang="ts">
    interface IRadioListItem {
        id: string | number;
        name: string;
    }

    export let group_id: string;
    export let items: IRadioListItem[];

    export let selected_item: IRadioListItem = null;

</script>

<div class="flex flex-col space-y-1">
    {#each items as item}
        <label for={item.id.toString()} class="block p-2 cursor-pointer border-2 rounded border-slate-300 hover:border-purple-600">
            <input type="radio" id={item.id.toString()} name={group_id} value={item.id} bind:group={selected_item} />
            {item.name}
        </label>
    {/each}
</div>
