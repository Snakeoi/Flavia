<script setup>
import {computed, onMounted, ref} from "vue";
import {readResource} from "@/assets/utils/axios/crud.js";
import SearchInput from "@/components/common/SearchInput.vue";
import DataTable from "@/components/common/data_table/DataTable.vue";
import router from "@/router/index.js";
import {adminSettingsViewsStore} from "@/stores/adminSettingsViews.js";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";

const isLoading = ref(true);
const adminSettingsViews = adminSettingsViewsStore();
const users = ref([]);

const filteredUsers = computed(() => {
  return users.value.filter(user => user.username.includes(
      adminSettingsViews.userSearchField
  ) || user.email.includes(
      adminSettingsViews.userSearchField
  ));
})

onMounted(async () => {
  await readResource(
      '/user/',
      response => {
        users.value = response.data
      });
  isLoading.value = false;
});

const openUserDetails = (row) => {
  router.push({name: 'admin-user', params: {id: row.id}});
}
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
    <h1 class="title">Users</h1>
    <div class="field is-grouped is-grouped-right">
      <div class="control">
        <RouterLink class="button is-primary" :to="{name: 'admin-user-add'}">
          <i class="icon-user-plus mr-3"></i>Add
        </RouterLink>
      </div>
    </div>
    <div class="my-3">
      <SearchInput v-model="adminSettingsViews.userSearchField"/>
    </div>
    <DataTable
        :storageName="'users'"
        :data="filteredUsers"
        :onRowClick="openUserDetails"
        :structure="[
          {
            key: 'username',
            title: 'Username',
            type: 'string',
            isSortable: true
          },
          {
            key: 'email',
            title: 'Email',
            type: 'string',
            isSortable: true
          },
          {
            key: 'confirmed',
            title: 'Confirmed',
            type: 'checkmark',
            isSortable: true
          },
          {
            key: 'permissions',
            title: 'Permissions',
            type: 'tagList'
          },
          {
            key: 'member_since',
            title: 'member_since',
            type: 'date',
            isSortable: true
          },
          {
            key: 'last_seen',
            title: 'Last seen',
            type: 'date',
            isSortable: true
          }
        ]"
    />
  </ConditionalLoader>
</template>

<style scoped>

</style>