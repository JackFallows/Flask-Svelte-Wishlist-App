const ViewsRoot = "";
const ApiRoot = "/api";

const EditViewRoot = ViewsRoot + "/edit";

const WishlistsApiRoot = ApiRoot + "/wishlists";

class Route {
    private route: string;

    constructor(route: string) {
        this.route = route;
    }

    public append(parameter: string | number): Route {
        this.route += `/${parameter}`;

        return this;
    }

    public to_string(): string {
        return this.route;
    }
}

const Views = {
    Edit: new Route(EditViewRoot)
}

const Api = {
    Wishlists: {
        Get: new Route(WishlistsApiRoot + "/get"),
        Post: new Route(WishlistsApiRoot + "/post")
    }
};

export { Route, Views, Api };
