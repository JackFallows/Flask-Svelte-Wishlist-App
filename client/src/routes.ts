class Route {
    private route: string;

    constructor(route: string) {
        this.route = route ?? "";
    }

    public append(parameter: string | number): Route {
        return new Route(this.route + `/${parameter}`);
    }

    public to_string(): string {
        return this.route;
    }
}

const ViewsRoot = new Route("");
const ApiRoot = ViewsRoot.append("api");

const AuthViewRoot = ViewsRoot.append("auth");
const ExternalAuthRoot = AuthViewRoot.append("external");
const EditViewRoot = ViewsRoot.append("edit");

const WishlistsApiRoot = ApiRoot.append("wishlists");
const WishlistItemsApiRoot = ApiRoot.append("wishlist_items");

const Views = {
    Auth: {
        Logout: AuthViewRoot.append("logout"),
        External: {
            Login: ExternalAuthRoot.append("login")
        }
    },
    Edit: EditViewRoot
}

const Api = {
    Wishlists: {
        Get: WishlistsApiRoot.append("get"),
        GetAllForUser: WishlistsApiRoot.append("get_all_for_user"),
        Post: WishlistsApiRoot.append("post"),
        Put: WishlistsApiRoot.append("put")
    },
    WishlistItems: {
        GetAllForWishlist: WishlistItemsApiRoot.append("get_all_for_wishlist"),
        Post: WishlistItemsApiRoot.append("post")
    }
};

export { Route, Views, Api };
