import { resolve } from 'path';
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    rollupOptions: {
      input: {
        navbar: resolve(__dirname, './src/components/navbar/main.ts'),
        sign_up: resolve(__dirname, './src/components/sign_up/main.ts'),
        login: resolve(__dirname, './src/components/login/main.ts'),
        index: resolve(__dirname, './src/components/index/main.ts'),
        view_wishlist: resolve(__dirname, './src/components/wishlist/view/main.ts'),
        edit_wishlist: resolve(__dirname, './src/components/wishlist/edit/main.ts'),
      },
    },
    sourcemap: true,
    minify: false,
    cssCodeSplit: false,
    copyPublicDir: false,
    outDir: './public/build',
    assetsDir: '.'
  },
})
