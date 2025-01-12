<script setup>
import Regex from "@/components/form/validators/Regex.vue";
import {ref} from "vue";
import Length from "@/components/form/validators/Length.vue";
import Email from "@/components/form/validators/Email.vue";

const props = defineProps({
  validators: {
    type: Object,
    required: true,
  },
  inputValue: {
    required: true,
  }
})

const emit = defineEmits(['update:isValid']);

const tests = ref({});

const collectTest = (value) => {
  tests.value[value.type] = value.passed;
  checkValidity();
};

const checkValidity = () => {
  let isValid = true;
  for (const test in tests.value) {
    if (!tests.value[test]) {
      isValid = false;
    }
  }
  emit('update:isValid', isValid);
}
</script>

<template>
<ul v-for="validator in validators" class="has-text-danger">
  <Regex v-if="validator.type === 'regex'" :validator="validator" :inputValue="inputValue" @onTest="collectTest"/>
  <Length v-if="validator.type === 'length'" :validator="validator" :inputValue="inputValue" @onTest="collectTest"/>
  <Email v-if="validator.type === 'email'" :validator="validator" :inputValue="inputValue" @onTest="collectTest"/>
</ul>
</template>

<style scoped>

</style>