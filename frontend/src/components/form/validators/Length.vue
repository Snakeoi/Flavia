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
  const tests = []

  if (props.validator.equal !== null) {
      tests.push(props.inputValue.length === props.validator.equal);
  }
  if (props.validator.min !== null) {
      tests.push(props.inputValue.length >= props.validator.min);
  }
  if (props.validator.max !== null) {
      tests.push(props.inputValue.length <= props.validator.max);
  }

  const passed = !(tests.includes(false));

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