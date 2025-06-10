import { registerPlugins } from '@/plugins'

import App from '@/App.vue'

import { createApp } from 'vue'

import "@/styles/main.scss";

import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
