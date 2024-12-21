<script setup>

import PasswordInput from "@/components/form/PasswordInput.vue";

import {ref, watch} from 'vue';
import generatePassword from "@/assets/utils/common/generatePassword.js";

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  class: {
    type: String,
    default: ''
  },
  length: {
    type: Number,
    required: true
  },
  regex: {
    type: RegExp,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const inputValue = ref(props.modelValue);
const displayPassword = ref(false)

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

watch(() => props.modelValue, (newValue) => {
  updateValue(newValue);
});

const updateValue = (value) => {
  emit('update:modelValue', value);
}

const updateDisplayPassword = (value) => {
  displayPassword.value = value
}

const setGeneratedPassword = () => {
  inputValue.value = generatePassword(
      props.regex,
      props.length,
  )
  displayPassword.value = true;
  updateValue(inputValue.value)
}
</script>

<template>
<div class="field has-addons">
  <div class="control">
    <PasswordInput
        :modelValue="inputValue"
        @update:modelValue="updateValue"
        :displayPassword="displayPassword"
        @update:displayPassword="updateDisplayPassword"
        :class="props.class"
    />
  </div>
  <div class="control">
    <button
        @click="setGeneratedPassword"
        class="button is-info">
      Generate
    </button>
  </div>
</div>
</template>

<style scoped>

</style>