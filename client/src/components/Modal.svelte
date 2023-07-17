<script lang="ts">
    import { onMount } from "svelte";

    export let id: string;
    export let is_danger: boolean = false;

    let promise_resolver: (val?: string) => void;

    let modal: HTMLDialogElement;

    onMount(() => {
        modal = <HTMLDialogElement>document.getElementById(`modal-${id}`);
    });

    function close_modal(return_value?: string) {
        modal.close(return_value);
    }

    function close_modal_handler() {
        const return_value = modal.returnValue;
        modal.returnValue = "";
        promise_resolver(return_value);
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

<dialog id="modal-{id}" class="dialog {is_danger ? "dialog-danger" : "dialog-primary"}" on:close={close_modal_handler}>
    <div class="header">
        <h3>
            <slot name="header"></slot>
        </h3>
    </div>
    <div class="body">
        <div>
            <slot name="body"></slot>
        </div>
        <slot name="buttons" {close_modal}>
            <button class="btn btn-secondary" on:click={() => close_modal()}>Cancel</button>
            <button class="btn btn-{is_danger ? "danger" : "primary"}" on:click={() => close_modal("true")}>Ok</button>
        </slot>
</div>
</dialog>

<style lang=less>
    .dialog {
        &.dialog-danger {
            .header {
                background-color: #dc3545;
            }
        }

        &.dialog-primary {
            .header {
                background-color: #0d6efd;
            }
        }

        .header {
            color: #fff;
        }
    }
</style>
