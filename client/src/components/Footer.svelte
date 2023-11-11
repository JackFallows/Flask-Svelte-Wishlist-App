<script lang="ts">

</script>

<footer class="flex flex-col space-y-1 sm:space-y-0 sm:flex-row w-full h-24 mt-12 px-4 py-2 sm:py-4 bg-slate-100 dark:bg-slate-800">
    <div class="grow flex flex-col space-y-1 md:space-y-3">
        <div class="grow flex items-baseline space-x-3">
            <span class="text-xl dark:text-slate-100">Wishlist App</span>
            <span class="text-xs text-slate-600 dark:text-slate-300">
                {#if window.version_number}
                    {@html window.version_number} <span class="fa-solid fa-arrow-up-right-from-square"></span>
                {:else}
                    <span>VXX, XXXX-XX-XX</span>
                {/if}
            </span>
        </div>
        <div class="flex space-x-3 dark:text-slate-100">
            <div><a class="hover:text-purple-600 dark:hover:text-purple-300" href="https://www.jackfallows.co.uk/" target="_blank">www.jackfallows.co.uk</a> <span class="fa-solid fa-arrow-up-right-from-square"></span></div>
            <span>|</span>
            <div><a class="hover:text-purple-600 dark:hover:text-purple-300" href="https://github.com/JackFallows/Flask-Svelte-Wishlist-App" target="_blank">GitHub</a> <span class="fa-solid fa-arrow-up-right-from-square"></span></div>
        </div>
    </div>
    <div class="sm:self-end text-slate-600 dark:text-slate-100">
        &copy; {(new Date()).getFullYear()} Jack Fallows
    </div>
</footer>
