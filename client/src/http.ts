import { GetRoute, PostRoute, PutRoute, PatchRoute, DeleteRoute } from "./routes";

export class HttpResult<T> implements IHttpResult<T> {
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

export async function Get<TResult>(route: GetRoute): Promise<HttpResult<TResult>> {
    const response = await fetch(route.to_string());

    const json = await response.json();

    return  new HttpResult<TResult>({ ok: response.ok, status: response.status, json });
};

export async function Post<T, TResult>(route: PostRoute, data: T): Promise<HttpResult<TResult>> {
    return await SendRequest('POST', route, data);
};

export async function Put<T, TResult>(route: PutRoute, data: T): Promise<HttpResult<TResult>> {
    return await SendRequest('PUT', route, data);
}

export async function Patch<T, TResult>(route: PatchRoute, data: T): Promise<HttpResult<TResult>> {
    return await SendRequest('PATCH', route, data);
}

export async function Delete<T, TResult>(route: DeleteRoute, data: T): Promise<HttpResult<TResult>> {
    return await SendRequest('DELETE', route, data);
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
