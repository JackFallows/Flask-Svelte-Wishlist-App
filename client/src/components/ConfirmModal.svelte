<script lang="ts">
    import { onMount } from "svelte";
    let promise_resolver: (val: boolean) => void;

    let modal: HTMLDialogElement;

    onMount(() => {
        modal = <HTMLDialogElement>document.getElementById("confirm-modal");
    });

    function cancel_modal() {
        modal.close("false");
    }

    function confirm_modal() {
        modal.close("true");
    }

    function close_modal_hander() {
        const return_value = modal.returnValue === 'true';
        promise_resolver(return_value);
    }

    // methods exposed to parent components via bind
    export const methods = {
        show(): Promise<boolean> {
            modal.showModal();

            const open_promise = new Promise<boolean>(r => {
                promise_resolver = r;
            });

            return open_promise;
        }
    }
</script>

<dialog id="confirm-modal" class="dialog" on:close={close_modal_hander}>
    <div class="header">
        <h3>Are you sure?</h3>
    </div>
    <div class="body">
        <p>This action cannot be undone.</p>
        <button class="btn btn-secondary" on:click={cancel_modal}>Cancel</button>
        <button class="btn btn-danger" on:click={confirm_modal}>Delete</button>
    </div>
</dialog>

<style lang=less>
    .dialog {
        .header {
            background-color: #dc3545;
            color: #fff;
        }
    }
</style>
