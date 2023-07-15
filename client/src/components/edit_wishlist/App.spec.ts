import { test, expect } from '@playwright/experimental-ct-svelte';
import App from './App.svelte';

test('does not load wishlist info if id not provided', async ({ mount, page }) => {
    let got_called = false;

    await page.route("/api/wishlists/get/*", async (route) => {
        got_called = true;

        await route.fulfill({
            status: 200,
            body: null
        });
    });

    await mount(App);

    await new Promise(r => setTimeout(r, 100)); // give it time so we're sure it didn't run the API request

    expect(got_called).toBe(false);
});

test('loads wishlist info if id provided', async ({ mount, page }) => {
    let got_called = false;

    await page.route("/api/wishlists/get/*", async (route) => {
        got_called = true;

        await route.fulfill({
            status: 200,
            body: JSON.stringify({ name: "My wishlist name", wishlist_items: [] })
        });
    });

    const component = await mount(App, {
        props: {
            wishlist_id: 1
        }
    });

    await new Promise(r => setTimeout(r, 100)); // give it chance to try to run the API request

    expect(got_called).toBe(true);
    
    await expect(component.locator("#wishlist-name")).toHaveValue("My wishlist name");
});
