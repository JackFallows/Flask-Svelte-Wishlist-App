import { GetRoute, PostRoute, PutRoute, PatchRoute, DeleteRoute } from "./routes";

export async function Get<TResult>(route: GetRoute): Promise<TResult> {
    const response = await fetch(route.to_string());

    if (response.ok) {
        const result = await (response.json() as Promise<TResult>);
        return result;
    }

    return null;
};

export async function Post<T, TResult>(route: PostRoute, data: T): Promise<TResult> {
    return await SendRequest('POST', route, data);
};

export async function Put<T, TResult>(route: PutRoute, data: T): Promise<TResult> {
    return await SendRequest('PUT', route, data);
}

export async function Patch<T, TResult>(route: PatchRoute, data: T): Promise<TResult> {
    return await SendRequest('PATCH', route, data);
}

export async function Delete<T, TResult>(route: DeleteRoute, data: T): Promise<TResult> {
    return await SendRequest('DELETE', route, data);
}

async function SendRequest<T, TResult>(method: string, route: IRoute, data: T): Promise<TResult> {
    const response = await fetch(route.to_string(), {
        method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        const result = await response.json();
        return result;
    }

    throw response;
}
