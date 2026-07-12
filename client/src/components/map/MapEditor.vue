<script setup> // Карта с трубами
import { usePipeStore } from '../../stores/networkStore.js'

const pipeStore = usePipeStore()
</script>

<template>
  <div class="map">
    <h2>Карта трубопровода</h2>

    <div class="pipes">
      <button
        v-for="pipe in pipeStore.pipes"
        :key="pipe.id"
        class="pipe"
        @click="pipeStore.selectPipe(pipe)"
      >
        {{ pipe.name }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.map {
  flex: 1;
  min-height: 500px;
  padding: 20px;
  border: 1px solid #ddd;
  background: #f5f7f9;
}

.pipes {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}

.pipe {
  width: 220px;
  padding: 12px;
  border: 2px solid #3b82f6;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  text-align: left;
}

.pipe:hover {
  background: #eaf2ff;
}
</style>