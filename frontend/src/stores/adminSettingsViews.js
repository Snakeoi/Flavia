import { defineStore } from 'pinia';
import {ref} from "vue";

export const adminSettingsViewsStore = defineStore('adminSettingsViewsStore', () => {
  // State
  const userSearchField = ref('');

  // Return values for the store
  return {
    userSearchField: userSearchField,
  };
});
