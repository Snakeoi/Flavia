// src/stores/userStore.js
import { defineStore } from 'pinia';
import {ref} from "vue";
import ApiConnector from "@/assets/utils/axios/factory.js";

export const useUserStore = defineStore('userStore', () => {
  // State
  const data = ref(null);
  const loading = ref(false);
  const error = ref(null);

  // Actions
  const fetchUserData = async () => {
    loading.value = true;
    error.value = null;

    try {
      const response = await ApiConnector.get('/user/current');
      data.value = response.data;
    } finally {
      loading.value = false;
    }
  };

  // Return values for the store
  return {
    data: data,
    loading,
    error,
    fetchUserData,
  };
});
