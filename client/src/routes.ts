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
const WishlistViewRoot = ViewsRoot.append("wishlist");

const UsersApiRoot = ApiRoot.append("users");
const WishlistsApiRoot = ApiRoot.append("wishlists");
const WishlistItemsApiRoot = ApiRoot.append("wishlist_items");

const Views = {
    Auth: {
        Login: AuthViewRoot.append("login"),
        SignUp: AuthViewRoot.append("sign-up"),
        Logout: AuthViewRoot.append("logout"),
        External: {
            Login: ExternalAuthRoot.append("login")
        }
    },
    Wishlist: {
        Create: WishlistViewRoot.append("create"),
        Edit: WishlistViewRoot.append("edit"),
        View: WishlistViewRoot.append("view")
    },
    Home: ViewsRoot.to_string() + "/"
}

const Api = {
    Users: {
        Create: UsersApiRoot.append("create"),
        Authenticate: UsersApiRoot.append("authenticate")
    },
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
