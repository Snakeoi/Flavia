<script setup>
import {createResource, readResource, updateResource} from "@/assets/utils/axios/crud.js";
import {onBeforeMount, ref} from "vue";
import {useRoute} from 'vue-router'
import Input from "@/components/form/Input.vue";
import formatDate from "../../../assets/utils/common/formatDate.js";
import TagList from "@/components/common/TagList.vue";
import BoolToCheckmark from "@/components/common/BoolToCheckmark.vue";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";
import Switch from "@/components/form/Switch.vue";
import {useToasterStore} from "@/stores/toaster.js";

const toasterStore = useToasterStore();

const route = useRoute();
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

const editMode = ref(false);
const updateSchema = ref({});

onBeforeMount(async () => {
  await readResource(`/user/${route.params.id}`, response => {
    user.value = response.data;
  });
  await readResource('/user/permission-codes', response => {
    permissions.value = response.data;
  });
  await readResource('/user/schema/update', response => {
    updateSchema.value = response.data;
  })
  isLoading.value = false;
})

const saveUser = async () => {
    const data = {
      email: user.value.email,
      permissions: user.value.permissions,
      username: user.value.username,
    };
    await updateResource(
        `/user/${route.params.id}`,
        data,
        response => {
          user.value = response.data;
          editMode.value = false;
          toasterStore.addMessage('success', `Changes has been saved.`);
        },
        error => {
          toasterStore.bulkRegisterBackendErrors(error);
        }
    );
}

const addOrRemovePermission = (permission) => {
  if (user.value.permissions.includes(permission)) {
    user.value.permissions.splice(user.value.permissions.indexOf(permission), 1);
  } else {
    user.value.permissions.push(permission);
  }
}

const sendConfirmationEmail = async () => {
  await createResource(
    `/user/send_confirmation_email/${route.params.id}`,
    {},
    (response) => {
      toasterStore.addMessage('success', `Confirmation email has been resent to ${user.value.email}.`);
    },
    (error) => {
      toasterStore.bulkRegisterBackendErrors(error);
    }
  )
}
</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
    <div class="field is-grouped is-grouped-right">
      <div class="control">
        <button class="button is-primary" v-if="route.params.id" @click="editMode = !editMode">Edit</button>
      </div>
    </div>

    <div v-if="editMode">

      <div class="field is-horizontal">
        <div class="field-body">
          <div class="field">
            <div class="field mb-3">
              <label class="label">Name</label>
              <Input
                  v-model="user.username"
                  icon-left="icon-user"
                  :validators="updateSchema?.username.validators"
              />
            </div>
            <div class="field mb-3">
              <label class="label">Email</label>
              <Input
                  v-model="user.email"
                  icon-left="icon-envelope"
                  :validators="updateSchema?.email.validators"
              />
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

    </div>

    <div v-else>
      <h1 class="title is-1">{{ user.username }}</h1>
      <table class="table">
        <tbody>
        <tr>
          <td>Contact</td>
          <td><i class="icon-envelope mr-3"></i> <a :href="'mailto:' + user.email">{{ user.email }}</a></td>
        </tr>
        <tr>
          <td>Registered</td>
          <td>{{ formatDate(user.member_since) }}</td>
        </tr>
        <tr>
          <td>Is confirmed</td>
          <td>
            <BoolToCheckmark :value=user.confirmed />
            <button class="button ml-3 is-small is-primary" @click=sendConfirmationEmail :disabled="user.confirmed">
              Send confirmation email
            </button>
          </td>
        </tr>
        <tr>
          <td>Last seen</td>
          <td>{{ formatDate(user.last_seen) }}</td>
        </tr>
        <tr>
          <td>Permissions</td>
          <td>
            <TagList :tags="user.permissions"/>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </ConditionalLoader>
</template>

<style scoped>

</style>