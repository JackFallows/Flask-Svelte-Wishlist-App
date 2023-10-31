<script lang="ts">
    import { setContext } from "svelte";
    import Modal from "./Modal.svelte";
    import { DeleteRoute, GetRoute, PatchRoute, PostRoute, PutRoute, makeRoutes } from "../routes";
    import { Get, Post, Put, Patch, Delete, HttpResult } from "../http";

    const { Views } = makeRoutes(window.base_path);

    let session_expiry_modal: Modal;

    setContext("http", <IHttp>{
        Get: <TResult>(route: GetRoute) => run_http<TResult>(() => Get(route)),
        Post: <T, TResult>(route: PostRoute, data: T) => run_http<TResult>(() => Post(route, data)),
        Put: <T, TResult>(route: PutRoute, data: T) => run_http<TResult>(() => Put(route, data)),
        Patch: <T, TResult>(route: PatchRoute, data: T) => run_http<TResult>(() => Patch(route, data)),
        Delete: <T, TResult>(route: DeleteRoute, data: T) => run_http<TResult>(() => Delete(route, data))
    });

    async function run_http<TResult>(exec: () => Promise<IHttpResult<TResult>>) {
        try {
            const result = await exec();
            return result;
        } catch (e) {
            if (e.status && e.status === 405) {
                session_expiry_modal.show();
            } else {
                throw e;
            }
        }
    }
</script>

<Modal id="session-expiry-modal" prevent_escape bind:this={session_expiry_modal}>
    <span slot="header">Session expired</span>
    <span slot="body">
        Please log back in.
    </span>
    <span slot="buttons">
        <a class="button" href="{Views.Auth.Login.to_string()}">Log in</a>
    </span>
</Modal>

<slot></slot>
