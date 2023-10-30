<script lang="ts">
    import { setContext } from "svelte";
    import DropDownMenu from "./DropDownMenu.svelte";
    import IconButton from "./IconButton.svelte";

    export let id: string;
    export let label: string;

    let burger_button: HTMLButtonElement;
    let dropdown: DropDownMenu;

    setContext("burger", true);
</script>

<div class="hidden sm:flex space-x-3 flex-nowrap items-center">
    <slot></slot>
</div>
<div class="block sm:hidden">
    <IconButton id={id} icon="fa-solid fa-bars" label={label} expand_in_burger_menu={false} bind:button={burger_button} on:click={dropdown.toggle} />

    <div class="dropdown-menu">
        <DropDownMenu button={burger_button} left bind:this={dropdown}>
            <slot></slot>
        </DropDownMenu>
    </div>
</div>

<style lang="less">
    .dropdown-menu {
        :global(button) {
            display: block;
        }
    }
</style>
