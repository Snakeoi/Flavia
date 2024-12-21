<script setup>
const props = defineProps({
  tags: {
    type: Array,
    required: true,
  }
})
</script>

<template>
  <span class="tags">
    <span v-for="tag in tags" class="tag">{{ tag }}</span>
  </span>
</template>

<style scoped>

</style>