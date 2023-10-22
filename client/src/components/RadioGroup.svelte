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
        <label for={"radio-option-" + item.id.toString()} class="container border-2 border-slate-300 hover:border-purple-600 rounded">
            {item.name}
            <input type="radio" class="" id={"radio-option-" + item.id.toString()} name={group_id} value={item} bind:group={selected_item} />
            <span class="checkmark"></span>
        </label>
    {/each}
</div>

<style lang="less">
    // https://www.w3schools.com/howto/howto_css_custom_checkbox.asp
    /* Customize the label (the container) */
    .container {
        display: block;
        position: relative;
        padding-left: 35px;
        cursor: pointer;
        font-size: 22px;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }

    /* Hide the browser's default radio button */
    .container input {
        position: absolute;
        opacity: 0;
        cursor: pointer;
        height: 0;
        width: 0;
    }

    /* Create a custom radio button */
    .checkmark {
        position: absolute;
        top: 4px;
        left: 4px;
        height: 25px;
        width: 25px;
        background-color: #eee;
        border-radius: 50%;
    }

    /* On mouse-over, add a grey background color */
    .container:hover input ~ .checkmark {
        background-color: #ccc;
    }

    /* When the radio button is checked, add a blue background */
    .container input:checked ~ .checkmark {
        background-color: rgb(147, 51, 234);
    }

    /* Create the indicator (the dot/circle - hidden when not checked) */
    .checkmark:after {
        content: "";
        position: absolute;
        display: none;
    }

    /* Show the indicator (dot/circle) when checked */
    .container input:checked ~ .checkmark:after {
        display: block;
    }

    /* Style the indicator (dot/circle) */
    .container .checkmark:after {
        top: 9px;
        left: 9px;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: white;
    }
</style>
