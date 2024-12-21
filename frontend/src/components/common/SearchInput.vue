<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
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
  <div class="control has-icons-left">
    <input
      class="input"
      type="email"
      placeholder="Search"
      :value="inputValue"
      @input="updateValue"
    />
    <span class="icon is-small is-left">
      <i class="icon-search"></i>
    </span>
  </div>
</template>

<style scoped>
</style>
