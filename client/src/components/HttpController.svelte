<script lang="ts">
    import { setContext } from "svelte";
    import Modal from "./Modal.svelte";
    import { DeleteRoute, GetRoute, PatchRoute, PostRoute, PutRoute, makeRoutes } from "../routes";

    const { Views } = makeRoutes(window.base_path);

    let session_expiry_modal: Modal;

    const login_url = window.internal_login_enabled ? Views.Auth.Login : Views.Auth.External.Login;

    setContext("http", {
        Get,
        Post,
        Put,
        Patch,
        Delete
    });

    class HttpResult<T> implements IHttpResult<T> {
        public ok: boolean;
        public status: number;
        
        private json: any;

        constructor({ ok, status, json }: { ok: boolean, status: number, json: any }) {
            this.ok = ok;
            this.status = status;
            this.json = json;
        }

        public get_json(): T {
            return <T>this.json;
        }

        public get_error<TError>(): TError {
            return <TError>this.json;
        }
    }

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

    async function SendRequest<T, TResult>(method: string, route: IRoute, data: T): Promise<HttpResult<TResult>> {
        const response = await fetch(route.to_string(), {
            method,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.status === 405) {
            throw {
                status: response.status
            };
        }

        const json = await response.json();

        return new HttpResult<TResult>({ ok: response.ok, status: response.status, json });
    }

    function Get<TResult>(route: GetRoute): Promise<IHttpResult<TResult>> {
        return run_http<TResult>(async () => {
            const response = await fetch(route.to_string());
            const json = await response.json();
            return new HttpResult<TResult>({ ok: response.ok, status: response.status, json });
        });
    };

    function Post<T, TResult>(route: PostRoute, data: T): Promise<IHttpResult<TResult>> {
        return run_http<TResult>(() => SendRequest('POST', route, data))
    };

    function Put<T, TResult>(route: PutRoute, data: T): Promise<IHttpResult<TResult>> {
        return run_http<TResult>(() => SendRequest('PUT', route, data));
    }

    function Patch<T, TResult>(route: PatchRoute, data: T): Promise<IHttpResult<TResult>> {
        return run_http<TResult>(() => SendRequest('PATCH', route, data));
    }

    function Delete<T, TResult>(route: DeleteRoute, data: T): Promise<IHttpResult<TResult>> {
        return run_http<TResult>(() => SendRequest('DELETE', route, data));
    }
</script>

<Modal id="session-expiry-modal" prevent_escape bind:this={session_expiry_modal}>
    <span slot="header">Session expired</span>
    <span slot="body">
        Please log back in.
    </span>
    <span slot="buttons">
        <a class="button" href="{login_url.to_string()}">Log in</a>
    </span>
</Modal>

<slot></slot>
