<script setup>
defineProps(['value'])
</script>
<template>
  <ul>
    <li v-for="(v, idx) in value" :key="idx">
      <div>{{ v }}</div>
    </li>
  </ul>
</template>
<style scoped>
li {
  list-style: none;
  padding: 0.5rem 0;
  border-top: 1px solid #888;
}

ul {
  padding: 0;
}
</style>
