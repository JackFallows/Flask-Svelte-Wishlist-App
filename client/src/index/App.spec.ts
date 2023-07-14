import { test, expect } from '@playwright/experimental-ct-svelte';
import App from './App.svelte';

test.use({ viewport: { width: 500, height: 500 } });

test('should work', async ({ mount }) => {
    const component = await mount(App);
    await expect(component).toContainText("Hello there!");
});