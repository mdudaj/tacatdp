declare module '@getodk/web-forms' {
  import type { Component } from 'vue';

  export const OdkWebForm: Component;
  export const POST_SUBMIT__NEW_INSTANCE: unknown;
  export const webFormsPlugin: {
    install: (app: import('vue').App) => void;
  };
}
