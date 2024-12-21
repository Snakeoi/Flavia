<script setup>
import {useToasterStore} from "@/stores/toaster.js";

const toasterStore = useToasterStore()
</script>

<template>
<div class="toaster">
  <div v-for="toast in toasterStore.messages" class="notification" :class="'is-' + toast.type" >
    <button class="delete" @click="toasterStore.removeMessage(toasterStore.messages.indexOf(toast))"></button>
    <span class="mr-4">{{ toast.message }}</span>
  </div>
</div>
</template>

<style scoped>
.toaster {
  z-index: 100;
  position: fixed;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  right: 0;
  bottom: 0;
  margin: 20px;
}
</style>