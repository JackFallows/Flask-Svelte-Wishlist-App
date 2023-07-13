const ViewsRoot = "/";
const ApiRoot = "/api/";

const EditViewRoot = ViewsRoot + "edit/";

const WishlistsApiRoot = ApiRoot + "wishlists/";

class Route {
    private route: string;

    constructor(route: string) {
        this.route = route;
    }

    public append(parameter: string | number): Route {
        this.route += `${parameter}/`;

        return this;
    }

    public to_string(): string {
        if (this.route.endsWith("/")) {
            // strip the trailing '/' as Flask doesn't like it
            return this.route.slice(0, this.route.length - 1);
        }

        return this.route;
    }
}

const Views = {
    Edit: new Route(EditViewRoot)
}

const Api = {
    Wishlists: {
        Get: new Route(WishlistsApiRoot + "get/"),
        Post: new Route(WishlistsApiRoot + "post/")
    }
};

export { Route, Views, Api };
