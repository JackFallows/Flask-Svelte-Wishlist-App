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
