import { createApp } from 'vue';
import { webFormsPlugin } from '@getodk/web-forms';
import App from './App.vue';
import './styles.css';

createApp(App).use(webFormsPlugin).mount('#app');
