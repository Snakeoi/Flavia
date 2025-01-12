<script setup>
import {computed} from "vue";

const props = defineProps({
  validator: {
    type: Object,
    required: true,
  },
  inputValue: {
    type: String,
    required: true,
  }
});

const emit = defineEmits(["onTest"]);

const isValid = computed(() =>{
  const regex = new RegExp(props.validator.regex);
  const passed = regex.test(props.inputValue);
  emit('onTest', {
    type: props.validator.type,
    passed: passed
  });
  return passed;
});
</script>

<template>
  <li v-if="!isValid">
    {{validator.error}}
  </li>
</template>

<style scoped>

</style>