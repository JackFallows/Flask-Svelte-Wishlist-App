/// <reference types="svelte" />

interface Window {
    internal_login_enabled: boolean;
    user_name?: string;
    profile_pic?: string;
    wishlist_id?: number;
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

    wishlist_items: IWishlistItem[];
}
