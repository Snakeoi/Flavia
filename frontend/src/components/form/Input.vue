<script setup>
import { ref, watch } from 'vue';
import Validators from "@/components/form/validators/Validators.vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
  },
  iconLeft: {
    type: String,
  },
  iconRight: {
    type: String,
  },
  class: {
    type: String,
  },
  type: {
    type: String,
    default: 'text',
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
const isValid = ref(true);

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

function updateValue(event) {
  emit('update:modelValue', event.target.value);
}

const setValidity = (value) => {
  isValid.value = value;
  emit('update:isValid', value);
}
</script>

<template>
  <div class="control" :class="{'has-icons-left': iconLeft, 'has-icons-right': iconRight}">
    <input
        v-model="inputValue"
        class="input"
        :class="props.class"
        @input="updateValue"
        :type="props.type"
    />
    <span v-if="iconLeft" class="icon is-small is-left">
      <i :class="iconLeft"></i>
    </span>
    <span v-if="iconRight" class="icon is-small is-right">
      <i :class="iconRight"></i>
    </span>
  </div>
  <Validators :validators="props.validators" :inputValue="inputValue" @update:isValid="setValidity"/>
</template>

<style scoped>
</style>
