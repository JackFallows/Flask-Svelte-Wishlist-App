<script lang="ts">

</script>

<div class="flex flex-col space-y-1 md:space-y-0 md:flex-row w-full h-24 mt-12 px-4 py-2 md:py-4 bg-slate-100">
    <div class="grow flex flex-col space-y-1 md:space-y-3">
        <div class="grow flex items-baseline space-x-3">
            <span class="text-xl">Wishlist App</span>
            {#if window.version_number}
                {@html window.version_number}
            {:else}
                <span class="text-xs text-slate-600">VXX, XXXX-XX-XX</span>
            {/if}
        </div>
        <div class="flex space-x-3">
            <div><a class="hover:text-purple-600" href="https://www.jackfallows.co.uk/" target="_blank">www.jackfallows.co.uk</a> <span class="fa-solid fa-arrow-up-right-from-square"></span></div>
            <span>|</span>
            <div><a class="hover:text-purple-600" href="https://github.com/JackFallows/Flask-Svelte-Wishlist-App" target="_blank">GitHub</a> <span class="fa-solid fa-arrow-up-right-from-square"></span></div>
        </div>
    </div>
    <div class="md:self-end">
        Copyright &copy; {(new Date()).getFullYear()} Jack Fallows. All rights reserved.
    </div>
</div>
