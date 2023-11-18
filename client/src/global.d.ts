/// <reference types="svelte" />

type Join = (room: string) => void;
type Notify = (event_name: string, data: any) => void;
type Respond = (to: string, with_callback: (data: any) => void) => void;

interface Window {
    page_title?: string;
    internal_login_enabled: boolean;
    user_id?: string;
    user_name?: string;
    profile_pic?: string;
    wishlist_id?: number;
    base_path: string;
    email_is_configured: boolean;
    version_number: string;
    user_has_enabled_email: boolean;
    notifications_api_url: string;
}

interface IValidationState {
    is_valid: boolean;
    failures: { [property: string]: string }[]
}

interface IHttpResult<T> {
    ok: boolean;
    status: number;
    get_json: () => T;
    get_error: <TError>() => TError;
}

interface IHttp {
    Get: <TResult>(route: GetRoute) => Promise<IHttpResult<TResult>>;
    Post: <T, TResult>(route: PostRoute, data: T) => Promise<IHttpResult<Result>>;
    Put: <T, TResult>(route: PutRoute, data: T) => Promise<IHttpResult<Result>>;
    Patch: <T, TResult>(route: PatchRoute, data: T) => Promise<IHttpResult<Result>>;
    Delete: <T, TResult>(route: DeleteRoute, data: T) => Promise<IHttpResult<Result>>;
}

interface IRoute {
    append(parameter: string | number): IRoute;
    to_string(): string;
}

interface IWishlistItem {
    id: number;
    wishlist_id: number;
    link: string;
    notes: string;
    bought: boolean;
    order_number: number;
    is_header: boolean;
}

interface IBoughtItem {
    id: number;
    user_id: string;
    wishlist_item_id: number;
    defer_until: Date;
}

interface IWishlist {
    id: number;
    user_id: string;
    name: string;
    shared: boolean;
    deleted: boolean;
    share_guid: string;

    wishlist_items: IWishlistItem[];
    bought_items: IBoughtItem[];
}

interface IWishlistLinkShare {
    id: number;
    name: string;
    share_guid: string;

    wishlist_items: IWishlistItem[];
}

interface IWishlistShare extends IWishlist {
    is_share: boolean;
    owner_name: string;
    owner_email: string;
}

interface IUser {
    name: string;
    email: string;
    profile_pic: string;
    email_on_share: boolean;
    email_on_update: boolean;
    email_on_owner_bought: boolean;
}

interface INotificationDto {
    id: number;
    message: string;
    created_at: Date;
    shared_wishlist_id: number;
    type: NotificationType;
}

interface ITab {
    id: string;
    label: string;
}

interface ITabContent {
    id: string;
    label: string;
    activate: () => void;
    deactivate: () => void;
}
