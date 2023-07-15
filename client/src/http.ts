import { Route } from "./routes";

export async function Get<TResult>(route: Route): Promise<TResult> {
    const response = await fetch(route.to_string());

    if (response.ok) {
        const result = await (response.json() as Promise<TResult>);
        return result;
    }

    return null;
};

export async function Post<T, TResult>(route: Route, data: T): Promise<TResult> {
    const response = await fetch(route.to_string(), {
        method: 'POST',
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

    return null;
};

export async function Put<T, TResult>(route: Route, data: T): Promise<TResult> {
    const response = await fetch(route.to_string(), {
        method: 'PUT',
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

    return null;
}
