// stores/toaster.js
import { defineStore } from "pinia";
import { reactive } from "vue";

export const useToasterStore = defineStore("toaster", () => {
  const state = reactive({
    messages: [],
  });

  const addMessage = (type, message) => {
    const toast = { type, message };
    state.messages.push(toast);

    // Usuń wiadomość po 10 sekundach
    setTimeout(() => {
      removeMessage(state.messages.indexOf(toast));
    }, 10000); // 10 sekund
  };

  const bulkRegisterBackendErrors = (error) => {
    if (error.response?.data.errors) {
      error.response?.data.errors.forEach(message => {
        addMessage('danger', message);
      })
    } else {
      addMessage('danger', error.message);
    }
  }

  const removeMessage = (index) => {
    if (index >= 0) {
      state.messages.splice(index, 1);
    }
  };

  return {
    messages: state.messages,
    addMessage,
    removeMessage,
    bulkRegisterBackendErrors
  };
});
