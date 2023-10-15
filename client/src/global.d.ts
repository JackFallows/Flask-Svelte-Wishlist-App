/// <reference types="svelte" />

interface Window {
    page_title?: string;
    internal_login_enabled: boolean;
    user_name?: string;
    profile_pic?: string;
    wishlist_id?: number;
    base_path: string;
    email_is_configured: boolean;
}

interface IValidationState {
    is_valid: boolean;
    failures: { [property: string]: string }[]
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
}

interface IWishlist {
    id: number;
    user_id: string;
    name: string;
    shared: boolean;
    deleted: boolean;
    share_guid: string;

    wishlist_items: IWishlistItem[];
}

interface IWishlistLinkShare {
    id: number;
    name: string;
    share_guid: string;

    wishlist_items: IWishlistItem[];
}

interface IWishlistShare extends IWishlist {
    owner_name: string;
    owner_email: string;
}

interface IUser {
    name: string;
    email: string;
    profile_pic: string;
    email_on_share: boolean;
    email_on_update: boolean;
}
