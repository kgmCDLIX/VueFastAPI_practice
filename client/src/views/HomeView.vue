<script setup> // основная страница
import PipeMap from '../components/PipeMap.vue'
import PipePassport from '../components/PipePassport.vue'
</script>

<template>
  <section>
    <h1>Карта</h1>

    <div class="layout">
      <PipeMap />
      <PipePassport />
    </div>
  </section>
</template>

<style scoped>
.layout {
  display: flex;
  gap: 20px;
  align-items: stretch;
}
</style>