<script setup>
const props = defineProps({
      value: {
        type: Boolean,
        required: true,
      }
});
</script>

<template>
  <i v-if="value" class="icon-check has-text-success"></i>
  <i v-else class="icon-times has-text-danger"></i>
</template>

<style scoped>

</style>