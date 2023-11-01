import { resolve } from 'path';
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

const isRelease = process.env.RELEASE == "1" ? true : false;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    rollupOptions: {
      input: {
        sign_up: resolve(__dirname, './src/pages/sign_up/main.ts'),
        login: resolve(__dirname, './src/pages/login/main.ts'),
        home: resolve(__dirname, './src/pages/index/main.ts'),
        wishlist: resolve(__dirname, './src/pages/wishlist/main.ts'),
        share: resolve(__dirname, './src/pages/share/main.ts'),
        profile: resolve(__dirname, './src/pages/profile/main.ts')
      },
    },
    sourcemap: !isRelease,
    minify: isRelease,
    cssCodeSplit: false,
    copyPublicDir: false,
    outDir: './public/build',
    assetsDir: '.'
  },
})
