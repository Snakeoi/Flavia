import { defineStore } from 'pinia';
import {ref} from "vue";

export const useUiStore = defineStore('uiStore', () => {
  // State
  const tables = ref({});

  // Return values for the store
  return {
    tables: tables,
  };
});
