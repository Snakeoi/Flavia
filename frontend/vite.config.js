import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import path from 'path'
import { readdirSync, readFileSync, writeFileSync, rmSync } from 'fs'

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function rewriteCssPaths() {
  return {
    name: 'rewrite-css-paths',
    apply: 'build',
    closeBundle() {
      const assetsDir = path.resolve(__dirname, '../application/static/assets');
      const files = readdirSync(assetsDir);

      files.forEach(file => {
        if (file.endsWith('.css')) {
          const filePath = path.join(assetsDir, file);
          let content = readFileSync(filePath, 'utf8');
          content = content.replace(/\/assets\//g, '/static/assets/');
          writeFileSync(filePath, content);
        }
      });
    }
  };
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VueDevTools(),
    rewriteCssPaths(),
    {
      name: 'remove-html',
      writeBundle() {
        try {
          rmSync(path.resolve(__dirname, '../application/static/index.html'));
        } catch (err) {
          console.error('Error removing index.html:', err);
        }
      }
    }
  ],
  server: {
    proxy: {
      '/user': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../application/static/',
    emptyOutDir: true
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
