<script setup>

import {ref} from "vue";

const links = ref([
  {
    text: 'Users',
    icon: 'icon-users',
    routeName: 'admin-users'
  }
]);

</script>

<template>
<nav class="panel is-primary">
    <RouterLink
        :to="{name: link.routeName}"
        v-for="link in links"
        :class="{'is-active': $route.name === link.routeName}"
        class="panel-block"
    >
      <span class="panel-icon">
        <i :class="link.icon" aria-hidden="true"></i>
      </span>{{ link.text }}
    </RouterLink>
</nav>
</template>

<style scoped>

</style>