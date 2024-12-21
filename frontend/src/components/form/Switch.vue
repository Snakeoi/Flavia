<script setup>
const props = defineProps({
  isOn: Boolean,
})
</script>

<template>
<span class="is-clickable">
  <span v-if="isOn">
    <i class="icon-check-square-o has-text-success"></i>
  </span>
  <span v-else>
    <i class="icon-square-o"></i>
  </span>
</span>
</template>

<style scoped>

</style>