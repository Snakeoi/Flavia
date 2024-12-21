<script setup>
import {createResource, readResource} from "@/assets/utils/axios/crud.js";
import {onBeforeMount, ref} from "vue";
import Input from "@/components/form/Input.vue";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";
import Switch from "@/components/form/Switch.vue";
import router from "@/router/index.js";
import {useToasterStore} from "@/stores/toaster.js";
import GeneratePasswordInput from "@/components/form/GeneratePasswordInput.vue";

const toasterStore = useToasterStore();

const isLoading = ref(true);

const user = ref({
  email: "",
  permissions: [],
  username: "",
  password: "",
  send_confirmation_email: true,
  confirmed: false,
});
const permissions = ref([]);

const createSchema = ref({});


onBeforeMount(async () => {
  await readResource('/user/permission-codes', response => {
    permissions.value = response.data;
  });
  await readResource('/user/schema/create', response => {
    createSchema.value = response.data;
  });
  isLoading.value = false;
})

const addOrRemovePermission = (permission) => {
  if (user.value.permissions.includes(permission)) {
    user.value.permissions.splice(user.value.permissions.indexOf(permission), 1);
  } else {
    user.value.permissions.push(permission);
  }
}

const saveUser = async () => {
  const data = {
    email: user.value.email,
    permissions: user.value.permissions,
    username: user.value.username,
    send_confirmation_email: user.value.send_confirmation_email,
    password: user.value.password,
  };
  await createResource(
    `/user/`,
    data,
    (response) => {
      user.value = response.data;
      router.push({name: 'admin-user', params: {id: response.data.id}});
      toasterStore.addMessage('success', `User ${response.data.username} has been added.`);
    },
    error => {
      toasterStore.bulkRegisterBackendErrors(error);
    });
}
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">



      <div class="field is-horizontal">
        <div class="field-body">
          <div class="field">
            <div class="field mb-3">
              <label class="label">Name</label>
              <Input v-model="user.username" icon-left="icon-user"/>
            </div>
            <div class="field mb-3">
              <label class="label">Email</label>
              <Input v-model="user.email" icon-left="icon-envelope"/>
            </div>
            <div class="field mb-3">
              <label class="label">Password</label>
              <GeneratePasswordInput
                  v-model="user.password"
                  :regex="/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$/"
                  :length="16"
              />
            </div>
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" class="checkbox" v-model="user.send_confirmation_email"/>
                Send registration email on save.
              </label>
            </div>
          </div>
          <div class="field">
            <label class="label">Permissions</label>
            <table class="table box">
              <tbody>
              <tr v-for="permission in permissions">
                <td>
                  <Switch :is-on="user.permissions.includes(permission)" @click="addOrRemovePermission(permission)"/>
                </td>
                <td>{{ permission }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button class="button is-primary" @click="saveUser">Save</button>
        </div>
      </div>


  </ConditionalLoader>
</template>

<style scoped>

</style>