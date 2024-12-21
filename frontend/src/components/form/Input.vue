<script setup>
import { ref, watch } from 'vue';

// Definiowanie właściwości (props)
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
});

const emit = defineEmits(['update:modelValue']);

const inputValue = ref(props.modelValue);

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

function updateValue(event) {
  emit('update:modelValue', event.target.value);
}
</script>

<template>
  <div class="control" :class="{'has-icons-left': iconLeft, 'has-icons-right': iconRight}">
    <input
        v-model="inputValue"
        class="input"
        :class="props.class"
        @input="updateValue"
    />
    <span v-if="iconLeft" class="icon is-small is-left">
      <i :class="iconLeft"></i>
    </span>
    <span v-if="iconRight" class="icon is-small is-right">
      <i :class="iconRight"></i>
    </span>
  </div>
</template>

<style scoped>
/* Dodatkowe style jeśli potrzebne */
</style>
