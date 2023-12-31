<script lang="ts">
    import '../tailwind.css';

    export let id: string;
    export let is_danger: boolean = false;
    export let is_wide: boolean = false;
    export let prevent_escape: boolean = false;

    let promise_resolver: (val?: string) => void;

    let modal: HTMLDialogElement;

    function close_modal(return_value?: string) {
        modal.close(return_value);
    }

    function close_modal_handler() {
        const return_value = modal.returnValue;
        modal.returnValue = "";
        promise_resolver(return_value);
    }

    function cancel_modal_handler(event) {
        if (prevent_escape) {
            event.preventDefault();
        }
    }

    // expose to parent components via bind
    export function show(): Promise<string> {
        modal.showModal();

        const open_promise = new Promise<string>(r => {
            promise_resolver = r;
        });

        return open_promise;
    }
</script>

<dialog id="modal-{id}" class="backdrop:bg-slate-600 dark:backdrop:bg-slate-900 backdrop:opacity-60 {is_wide ? 'w-[32rem]' : 'w-96'} h-96 rounded-md border-2 shadow-md {is_danger ? 'border-red-600' : 'border-slate-200 dark:border-slate-700'} mt-20" bind:this={modal} on:close={close_modal_handler} on:cancel={cancel_modal_handler}>
    <div class="flex flex-col h-full">
        <div class="{is_danger ? 'bg-red-600' : 'bg-slate-200 dark:bg-slate-700'} p-2">
            <h1 class="text-xl {is_danger ? 'text-white' : 'text-black dark:text-slate-100'}">
                <slot name="header"></slot>
            </h1>
        </div>
        <div class="p-2 grow overflow-y-auto dark:bg-slate-600 dark:text-slate-100">
            <div>
                <slot name="body"></slot>
            </div>
        </div>
        <div class="p-2 dark:bg-slate-600">
            <slot name="buttons" {close_modal}>
                <button class="button" on:click={() => close_modal()}>Cancel</button>
                <button class="button" on:click={() => close_modal("true")}>Ok</button>
            </slot>
        </div>
    </div>
</dialog>
