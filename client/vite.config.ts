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
        navbar: resolve(__dirname, './src/components/navbar/main.ts'),
        sign_up: resolve(__dirname, './src/components/sign_up/main.ts'),
        login: resolve(__dirname, './src/components/login/main.ts'),
        index: resolve(__dirname, './src/components/index/main.ts'),
        wishlist: resolve(__dirname, './src/components/wishlist/main.ts'),
        share: resolve(__dirname, './src/components/share/main.ts'),
        profile: resolve(__dirname, './src/components/profile/main.ts')
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
