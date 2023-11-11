<script lang="ts">
    export let id: string;
    export let label: string;
    export let icon: string;
</script>

<button class="text-left text-xl w-full block bg-white dark:bg-slate-600 hover:bg-slate-100 dark:hover:bg-slate-500 dark:text-slate-100 p-1" id={id} on:click>
    <span class="fa-fw {icon} pointer-events-none"></span>
    {label}
</button>
