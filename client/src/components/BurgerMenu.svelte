<script lang="ts">
    import DropDownMenu from "./DropDownMenu.svelte";

    let burger_button: HTMLButtonElement;
    let dropdown: DropDownMenu;
</script>

<div class="hidden sm:block">
    <slot></slot>
</div>
<div class="block sm:hidden">
    <button class="icon-button" bind:this={burger_button} on:click={dropdown.toggle}>
        <span class="fa-solid fa-bars pointer-events-none"></span>
    </button>

    <div class="dropdown-menu">
        <DropDownMenu button={burger_button} bind:this={dropdown}>
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
