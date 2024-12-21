<script setup>
const props = defineProps({
  active: {
    type: Boolean,
    required: true
  },
  direction: {
    type: String,
    required: true,
    validator(value) {
      return ['', 'asc', 'desc'].includes(value)
    }
  },
})
</script>

<template>
  <span class="ml-3">
    <span v-if="active && direction === 'asc'"><i class="icon-sort-asc"></i></span>
    <span v-else-if="active && direction === 'desc'"><i class="icon-sort-desc"></i></span>
    <span v-else><i class="icon-sort has-text-text-50"></i></span>
  </span>
</template>

<style scoped>

</style>