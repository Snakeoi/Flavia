<script setup>
import {onMounted} from "vue";
import {RouterView} from "vue-router";
import Menu from "@/components/Menu.vue";
import {useUserStore} from "@/stores/user.js";
import Toaster from "@/components/Toaster.vue";

const userStore = useUserStore();
const { data, loading, error, fetchUserData } = userStore;

onMounted(() => {
  fetchUserData();
});
</script>

<template>
  <Menu/>
  <Toaster/>
  <div class="container is-fluid">
    <RouterView />
  </div>
</template>

<style scoped>

</style>