<script setup>

import PasswordInput from "@/components/form/PasswordInput.vue";

import {ref, watch} from 'vue';
import generatePassword from "@/assets/utils/common/generatePassword.js";
import Validators from "@/components/form/validators/Validators.vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  class: {
    type: String,
    default: ''
  },
  validators: {
    type: Array,
    default: {},
  }
});

const emit = defineEmits([
    'update:modelValue',
    'update:isValid',
]);

const inputValue = ref(props.modelValue);
const displayPassword = ref(false)
const isValid = ref(true);

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

const getRegex = () => {
  const validator = props.validators.filter(v => v.type === 'regex')[0];
  if (validator !== undefined) {
    return new RegExp(validator.regex);
  } else {
    console.error('Regex validator is undefined.');
  }
}

const getLength = () => {
  const validator = props.validators.filter(v => v.type === 'length')[0];
  if (validator !== undefined) {
    return validator.min;
  } else {
    console.error('Length validator is undefined.');
  }
}

const setGeneratedPassword = () => {
  const regex = getRegex();
  const length = getLength();

  inputValue.value = generatePassword(
      regex,
      length,
  )
  displayPassword.value = true;
  updateValue(inputValue.value)
}

const setValidity = (value) => {
  isValid.value = value;
  emit('update:isValid', value);
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
        :validators="validators"
        @update:isValid="setValidity"
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