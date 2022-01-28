/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
const path = require('path')


// https://vitejs.dev/config/
export default defineConfig({
  test: {
    global: true,
    environment: 'happy-dom'
  },
  resolve:{
    alias:{
      '@' : path.resolve(__dirname, './src')
    },
  },
  plugins: [
    vue()
  ],
})
