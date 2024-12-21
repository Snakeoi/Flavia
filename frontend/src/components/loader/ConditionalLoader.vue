<script setup>
import Loader from "@/components/loader/Loader.vue";

const props = defineProps({
  isLoading: {
    type: Boolean,
  }
})
</script>

<template>
<div v-if="isLoading" class="is-flex is-justify-content-center is-align-items-center">
  <Loader/>
</div>
<slot v-else></slot>
</template>

<style scoped>

</style>