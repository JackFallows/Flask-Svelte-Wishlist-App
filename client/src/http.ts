export async function Get<TResult>(route: string): Promise<TResult> {
    const response = await fetch(route);

    if (response.ok) {
        const result = await (response.json() as Promise<TResult>);
        return result;
    }

    return null;
};

export async function Post<T, TResult>(route: string, data: T): Promise<TResult> {
    const response = await fetch(route, {
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