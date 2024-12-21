<script setup>
import {useUserStore} from "@/stores/user.js";

const userStore = useUserStore();
</script>

<template>
<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <img alt="logo" src="/images/logo.svg" style="width: 80px">
    </a>

    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
      <RouterLink :to="{name: 'home'}" class="navbar-item">
        Home
      </RouterLink>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div v-if="!userStore.data" class="buttons">
          <a class="button is-primary" href="/user/register">
            <span class="icon">
              <i class="icon-user-plus"></i>
            </span>
            <span>Sign up</span>
          </a>
          <a class="button is-light" href="/user/login">
            <span class="icon">
              <i class="icon-sign-in"></i>
            </span>
            <span>Log in</span>
          </a>
        </div>
        <div v-else class="buttons">
          <RouterLink :to="{name: 'admin-dashboard'}" class="button is-light is-outlined">
            <span class="icon">
              <i class="icon-cog"></i>
            </span>
          </RouterLink>

          <a class="button is-light is-outlined">
            <span class="icon">
              <i class="icon-user"></i>
            </span>
            <strong>{{ userStore.data.username }}</strong>
          </a>
          <a class="button is-primary" href="/user/logout">
            <span class="icon">
              <i class="icon-sign-out"></i>
            </span>
            <span>Log out</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>

<style scoped>

</style>