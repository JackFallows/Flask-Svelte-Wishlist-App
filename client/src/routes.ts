class Route implements IRoute {
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

    public as_get(): GetRoute {
        return new GetRoute(this);
    }

    public as_post(): PostRoute {
        return new PostRoute(this);
    }

    public as_put(): PutRoute {
        return new PutRoute(this);
    }

    public as_patch(): PatchRoute {
        return new PatchRoute(this);
    }

    public as_delete(): DeleteRoute {
        return new DeleteRoute(this);
    }
}

class GetRoute implements IRoute {
    private route: IRoute;

    constructor(route: IRoute) {
        this.route = route;
    }

    append(parameter: string | number): GetRoute {
        return new GetRoute(this.route.append(parameter));
    }

    to_string(): string {
        return this.route.to_string();
    }
}

class PostRoute implements IRoute {
    private route: IRoute;

    constructor(route: IRoute) {
        this.route = route;
    }

    append(parameter: string | number): PostRoute {
        return new PostRoute(this.route.append(parameter));
    }

    to_string(): string {
        return this.route.to_string();
    }
}

class PutRoute implements IRoute {
    private route: IRoute;

    constructor(route: IRoute) {
        this.route = route;
    }

    append(parameter: string | number): PutRoute {
        return new PutRoute(this.route.append(parameter));
    }

    to_string(): string {
        return this.route.to_string();
    }
}

class PatchRoute implements IRoute {
    private route: IRoute;

    constructor(route: IRoute) {
        this.route = route;
    }

    append(parameter: string | number): PatchRoute {
        return new PatchRoute(this.route.append(parameter));
    }

    to_string(): string {
        return this.route.to_string();
    }
}

class DeleteRoute implements IRoute {
    private route: IRoute;

    constructor(route: IRoute) {
        this.route = route;
    }

    append(parameter: string | number): DeleteRoute {
        return new DeleteRoute(this.route.append(parameter));
    }

    to_string(): string {
        return this.route.to_string();
    }
}

function makeRoutes(base_path: string) {
    const ViewsRoot = new Route(base_path);
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
            Create: UsersApiRoot.append("create").as_post(),
            Authenticate: UsersApiRoot.append("authenticate").as_post()
        },
        Wishlists: {
            Get: WishlistsApiRoot.append("get").as_get(),
            GetAllForUser: WishlistsApiRoot.append("get_all_for_user").as_get(),
            GetSharedWithUser: WishlistsApiRoot.append("get_shared_with_user").as_get(),
            GetPendingSharedForUser: WishlistsApiRoot.append("get_pending_shares_for_user").as_get(),
            Post: WishlistsApiRoot.append("post").as_post(),
            Put: WishlistsApiRoot.append("put").as_put(),
            PatchShare: WishlistsApiRoot.append("share").as_patch(),
            PatchAcceptShare: WishlistsApiRoot.append("accept_share").as_patch(),
            PatchRejectShare: WishlistsApiRoot.append("reject_share").as_patch(),
            Delete: WishlistsApiRoot.append("delete").as_delete()
        },
        WishlistItems: {
            GetAllForWishlist: WishlistItemsApiRoot.append("get_all_for_wishlist").as_get(),
            PatchMarkAsBought: WishlistItemsApiRoot.append("mark-as-bought").as_patch()
        }
    };
    
    return {
        Views,
        Api
    };
}

export {
    Route,
    GetRoute,
    PostRoute,
    PutRoute,
    PatchRoute,
    DeleteRoute,
    makeRoutes
};
