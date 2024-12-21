<script setup>
import {computed, ref, watch} from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  class: {
    type: String,
    default: ''
  },
  displayPassword: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits([
    'update:modelValue',
    'update:displayPassword',
]);

const inputValue = ref(props.modelValue);
const displayPassword = ref(props.displayPassword);

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

watch(() => props.displayPassword, (newValue) => {
  displayPassword.value = newValue;
});

const updateValue = (event) => {
  emit('update:modelValue', event.target.value);
}

const switchDisplayPassword = () => {
  displayPassword.value = !displayPassword.value
  emit('update:displayPassword', displayPassword.value);
}

const type = computed(() => {
  if (displayPassword.value) {
    return 'text';
  } else {
    return 'password';
  }
})
</script>

<template>
  <div class="control has-icons-left has-icons-right">
    <input
        v-model="inputValue"
        class="input"
        :type="type"
        :class="props.class"
        @input="updateValue"
    />
    <span class="icon is-small is-left">
      <i class="icon-lock"></i>
    </span>
    <span class="icon is-small is-right is-clickable" @click="switchDisplayPassword">
      <i class="has-text-link" :class="{'icon-eye': !displayPassword, 'icon-eye-slash': displayPassword}"></i>
    </span>
  </div>
</template>

<style scoped>
</style>
