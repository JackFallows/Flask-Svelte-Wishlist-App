import { test, expect } from '@playwright/experimental-ct-svelte';
import App from './App.svelte';

test.use({ viewport: { width: 500, height: 500 } });

test('missing username displays "Hello there!"', async ({ mount }) => {
    const component = await mount(App);
    await expect(component).toContainText("Hello there!");
});

test('provided username displays "Hello {name}!"', async ({ mount }) => {
    const component = await mount(App, {
        props: {
            name: "Jack"
        }
    });
    
    await expect(component).toContainText("Hello Jack!");
});

test('no wishlists - text and button shown', async ({ mount, page }) => {
    await page.route("/api/wishlists/get_all_for_user", async (route) => {
        await route.fulfill({
            status: 200,
            body: JSON.stringify([])
        });
    });

    const component = await mount(App, {
        props: {
            name: "Jack"
        }
    });

    await expect(component).toContainText("You have no wishlists");
    await expect(component.locator("#no-wishlists-create-button")).toBeVisible()
});

test('one wishlist - wishlist component shown', async ({ mount, page }) => {
    await page.route("/api/wishlists/get_all_for_user", async (route) => {
        await route.fulfill({
            status: 200,
            body: JSON.stringify([{ id: 1, name: "My test wishlist" }])
        });
    });

    const component = await mount(App, {
        props: {
            name: "Jack"
        }
    });

    await expect(component.locator("#wishlist-1")).toContainText("My test wishlist");
});
