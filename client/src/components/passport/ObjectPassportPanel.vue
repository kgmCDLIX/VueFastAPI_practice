<script setup>
import { computed } from 'vue'
import { useNetworkStore } from '../../stores/networkStore'

const networkStore = useNetworkStore()

const title = computed(() => {
  if (!networkStore.selectedObject) {
    return 'Паспорт объекта'
  }

  const titles = {
    vertex: 'Паспорт скважины',
    pipe: 'Паспорт трубы',
    pipe_part: 'Паспорт части трубы',
  }

  return titles[networkStore.selectedObject.type] || 'Паспорт объекта'
})

const objectFields = computed(() => {
  if (!networkStore.selectedObject) {
    return []
  }

  return Object.entries(networkStore.selectedObject.data)
    .filter(([key]) => key !== 'id')
    .map(([key, value]) => ({
      key,
      value,
    }))
})
</script>

<template>
  <v-card min-height="560">
    <v-card-title>
      {{ title }}
    </v-card-title>

    <v-card-subtitle v-if="networkStore.selectedObject">
      {{ networkStore.selectedObject.data.name }}
    </v-card-subtitle>

    <v-card-text>
      <template v-if="networkStore.selectedObject">
        <v-list lines="two">
          <v-list-item
            v-for="field in objectFields"
            :key="field.key"
          >
            <v-list-item-title>
              {{ field.key }}
            </v-list-item-title>

            <v-list-item-subtitle>
              {{ field.value }}
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>

        <v-divider class="my-4" />

        <v-btn
          block
          color="error"
          variant="tonal"
          prepend-icon="mdi-close"
          @click="networkStore.clearSelectedObject"
        >
          Закрыть паспорт
        </v-btn>
      </template>

      <v-alert
        v-else
        type="info"
        variant="tonal"
        title="Объект не выбран"
        text="Выберите скважину, трубу или часть трубы на схеме."
      />
    </v-card-text>
  </v-card>
</template>