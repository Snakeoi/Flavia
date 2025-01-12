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
  const passed = String(props.inputValue)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
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