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
    const ProfileViewRoot = ViewsRoot.append("profile");
    
    const UsersApiRoot = ApiRoot.append("users");
    const WishlistsApiRoot = ApiRoot.append("wishlists");
    const WishlistItemsApiRoot = ApiRoot.append("wishlist_items");
    const NotificationsApiRoot = ApiRoot.append("notifications");
    
    const Views = {
        Auth: {
            Login: AuthViewRoot.append("login"),
            SignUp: AuthViewRoot.append("sign-up"),
            Logout: AuthViewRoot.append("logout"),
            External: {
                Login: ExternalAuthRoot.append("login")
            }
        },
        Wishlist: WishlistViewRoot,
        Profile: ProfileViewRoot.to_string() + "/",
        Home: ViewsRoot.to_string() + "/"
    }
    
    const Api = {
        Users: {
            Create: UsersApiRoot.append("create").as_post(),
            Authenticate: UsersApiRoot.append("authenticate").as_post(),
            Get: UsersApiRoot.append("get").as_get(),
            Update: UsersApiRoot.append("update").as_patch()
        },
        Wishlists: {
            Get: WishlistsApiRoot.append("get").as_get(),
            GetName: WishlistsApiRoot.append("get_name").as_get(),
            GetLinkShare: WishlistsApiRoot.append("get_link_share").as_get(),
            GetAllForUser: WishlistsApiRoot.append("get_all_for_user").as_get(),
            GetCountForUser: WishlistsApiRoot.append("get_count_for_user").as_get(),
            GetSharedWithUser: WishlistsApiRoot.append("get_shared_with_user").as_get(),
            Post: WishlistsApiRoot.append("post").as_post(),
            PatchUpdateName: WishlistsApiRoot.append("update-name").as_patch(),
            PatchShare: WishlistsApiRoot.append("share").as_patch(),
            PatchShareLink: WishlistsApiRoot.append("share-link").as_patch(),
            PatchAddToAccount: WishlistsApiRoot.append("add-to-account").as_patch(),
            Delete: WishlistsApiRoot.append("delete").as_delete()
        },
        WishlistItems: {
            GetAllForWishlist: WishlistItemsApiRoot.append("get_all_for_wishlist").as_get(),
            Get: WishlistItemsApiRoot.append("get").as_get(),
            PostCreate: WishlistItemsApiRoot.append("/create").as_post(),
            PatchMarkAsBought: WishlistItemsApiRoot.append("mark-as-bought").as_patch(),
            PatchChangeText: WishlistItemsApiRoot.append("change-text").as_patch(),
            PatchReparent: WishlistItemsApiRoot.append("reparent").as_patch(),
            PatchEnsureOrder: WishlistItemsApiRoot.append("ensure-order").as_patch(),
            Delete: WishlistItemsApiRoot.append("delete").as_delete()
        },
        Notifications: {
            Get: NotificationsApiRoot.append("get").as_get(),
            PatchRead: NotificationsApiRoot.append("read").as_patch(),
            PatchAcceptShare: NotificationsApiRoot.append("accept_share").as_patch(),
            PatchRejectShare: NotificationsApiRoot.append("reject_share").as_patch(),
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
