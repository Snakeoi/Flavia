<script setup>

import SideMenu from "@/components/admin/SideMenu.vue";
</script>

<template>
<div class="section">
  <div class="columns is-desktop">
    <aside class="column is-narrow-desktop">
      <SideMenu></SideMenu>
    </aside>
    <main class="column">
      <RouterView/>
    </main>
  </div>
</div>
</template>

<style scoped>

</style>