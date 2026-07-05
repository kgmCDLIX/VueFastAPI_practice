<script setup> // паспорт выбранной трубы
import { usePipeStore } from '../stores/pipeStore'

const pipeStore = usePipeStore()
</script>

<template>
  <aside class="passport">
    <template v-if="pipeStore.selectedPipe">
      <div class="passport-header">
        <h2>Паспорт трубы</h2>

        <button @click="pipeStore.clearSelectedPipe">
          Закрыть
        </button>
      </div>

      <p><strong>Название:</strong> {{ pipeStore.selectedPipe.name }}</p>
      <p><strong>Диаметр:</strong> {{ pipeStore.selectedPipe.diameter }}</p>
      <p><strong>Материал:</strong> {{ pipeStore.selectedPipe.material }}</p>
      <p><strong>Давление:</strong> {{ pipeStore.selectedPipe.pressure }}</p>
      <p><strong>Длина:</strong> {{ pipeStore.selectedPipe.length }}</p>
      <p><strong>Состояние:</strong> {{ pipeStore.selectedPipe.condition }}</p>
    </template>

    <template v-else>
      <h2>Паспорт трубы</h2>
      <p>Выберите трубу на карте.</p>
    </template>
  </aside>
</template>

<style scoped>
.passport {
  width: 320px;
  padding: 20px;
  border: 1px solid #ddd;
  background: white;
}

.passport-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  cursor: pointer;
}
</style>