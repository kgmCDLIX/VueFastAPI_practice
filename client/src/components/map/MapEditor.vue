<script setup>
import { computed } from 'vue'
import { useNetworkStore } from '../../stores/networkStore'

const networkStore = useNetworkStore()

const pipe = computed(() => networkStore.pipes[0])
const firstVertex = computed(() => networkStore.vertices[0])
const secondVertex = computed(() => networkStore.vertices[1])

const hasData = computed(() => {
  return firstVertex.value && secondVertex.value && pipe.value
})
</script>

<template>
  <v-card min-height="560">
    <v-card-title class="d-flex align-center justify-space-between">
      <span>Схема сети</span>

      <v-chip color="primary" variant="tonal">
        Данные с backend
      </v-chip>
    </v-card-title>

    <v-card-subtitle>
      Кликните по скважине, трубе или части трубы, чтобы открыть паспорт.
    </v-card-subtitle>

    <v-card-text>
      <v-progress-linear
        v-if="networkStore.isLoading"
        indeterminate
        color="primary"
        class="mb-4"
      />

      <v-alert
        v-if="networkStore.error"
        type="error"
        variant="tonal"
        class="mb-4"
        :text="networkStore.error"
      />

      <v-alert
        v-if="!networkStore.isLoading && !hasData"
        type="warning"
        variant="tonal"
        title="Нет данных"
        text="Backend работает, но данные для схемы пока не пришли или их недостаточно."
      />

      <v-sheet
        v-if="hasData"
        rounded="lg"
        border
        class="pa-6 d-flex align-center justify-space-between"
        min-height="360"
      >
        <v-card
          width="180"
          color="blue-lighten-5"
          border
          class="text-center"
          @click="networkStore.selectObject('vertex', firstVertex)"
        >
          <v-card-text>
            <v-icon icon="mdi-map-marker" size="32" class="mb-2" />

            <div class="font-weight-bold">
              {{ firstVertex.name }}
            </div>

            <v-chip size="small" color="success" variant="tonal" class="mt-2">
              {{ firstVertex.condition }}
            </v-chip>
          </v-card-text>
        </v-card>

        <v-sheet class="flex-grow-1 mx-4">
          <v-row dense>
            <v-col
              v-for="part in networkStore.pipeParts"
              :key="part.id"
              cols="6"
            >
              <v-btn
                block
                height="52"
                color="grey-darken-3"
                variant="flat"
                @click="networkStore.selectObject('pipe_part', part)"
              >
                {{ part.name }}
              </v-btn>
            </v-col>
          </v-row>

          <v-btn
            block
            class="mt-4"
            color="primary"
            variant="tonal"
            prepend-icon="mdi-pipe"
            @click="networkStore.selectObject('pipe', pipe)"
          >
            Открыть паспорт всей трубы
          </v-btn>
        </v-sheet>

        <v-card
          width="180"
          color="blue-lighten-5"
          border
          class="text-center"
          @click="networkStore.selectObject('vertex', secondVertex)"
        >
          <v-card-text>
            <v-icon icon="mdi-map-marker" size="32" class="mb-2" />

            <div class="font-weight-bold">
              {{ secondVertex.name }}
            </div>

            <v-chip size="small" color="success" variant="tonal" class="mt-2">
              {{ secondVertex.condition }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>