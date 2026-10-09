<script setup>
import {
  computed,
  ref,
} from 'vue'

import { useNetworkStore } from '../../stores/networkStore'
import PipeFormDialog from '../map/PipeFormDialog.vue'


const networkStore =
  useNetworkStore()


const pipeDialogOpen =
  ref(false)

const dialogPipe =
  ref(null)


const title = computed(() => {
  if (!networkStore.selectedObject) {
    return 'Паспорт объекта'
  }

  const titles = {
    vertex: 'Паспорт скважины',
    pipe: 'Паспорт трубы',
    pipePart: 'Паспорт части трубы',
    pipe_part: 'Паспорт части трубы',
  }

  return (
    titles[
      networkStore.selectedObject.type
    ]
    || 'Паспорт объекта'
  )
})


const isPipeSelected = computed(() => {
  return (
    networkStore.selectedObject?.type === 'pipe'
  )
})


const fieldLabels = {
  name: 'Название',
  diameter: 'Диаметр',
  material: 'Материал',
  condition: 'Состояние',

  vertex_start_id: 'Начало трубы',
  vertex_end_id: 'Конец трубы',

  pipe_id: 'Труба',
}


const objectFields = computed(() => {
  if (!networkStore.selectedObject) {
    return []
  }

  return Object
    .entries(
      networkStore.selectedObject.data
    )

    .filter(
      ([key]) =>
        key !== 'id' &&
        key !== 'name'
    )

    .map(
      ([key, value]) => ({
        key,

        label:
          fieldLabels[key]
          ?? key,

        value:
          formatValue(
            key,
            value
          ),
      })
    )
})


function formatValue(
  key,
  value
) {
  if (
    value === null ||
    value === undefined ||
    value === ''
  ) {
    return '—'
  }

  if (
    key === 'vertex_start_id' ||
    key === 'vertex_end_id'
  ) {
    const vertex =
      networkStore.vertices.find(
        item =>
          item.id === value
      )

    if (vertex) {
      return (
        `${vertex.name} `
        +
        `(ID: ${vertex.id})`
      )
    }
  }

  return value
}


function openCreatePipe() {
  dialogPipe.value = null
  pipeDialogOpen.value = true
}


function openEditPipe() {
  if (!isPipeSelected.value) {
    return
  }

  dialogPipe.value = {
    ...networkStore.selectedObject.data,
  }

  pipeDialogOpen.value = true
}
</script>


<template>
  <v-card min-height="560">

    <v-card-title>
      {{ title }}
    </v-card-title>


    <v-card-subtitle
      v-if="networkStore.selectedObject"
    >
      {{
        networkStore
          .selectedObject
          .data
          .name
      }}
    </v-card-subtitle>


    <v-card-text>

      <template
        v-if="networkStore.selectedObject"
      >
        <v-list lines="two">

          <v-list-item
            v-for="field in objectFields"
            :key="field.key"
          >
            <v-list-item-title>
              {{ field.label }}
            </v-list-item-title>

            <v-list-item-subtitle>
              {{ field.value }}
            </v-list-item-subtitle>
          </v-list-item>

        </v-list>
      </template>


      <v-alert
        v-else
        type="info"
        variant="tonal"
        title="Объект не выбран"
        text="Выберите скважину, трубу или часть трубы на карте."
      />

    </v-card-text>


    <v-divider />


    <v-card-actions class="pa-4">

      <div class="passport-actions">

        <!--
          Если выбрана труба,
          показываем редактирование
        -->
        <v-btn
          v-if="isPipeSelected"
          block
          color="primary"
          variant="flat"
          prepend-icon="mdi-pencil"
          @click="openEditPipe"
        >
          Редактировать трубу
        </v-btn>


        <!--
          Если труба не выбрана,
          показываем добавление
        -->
        <v-btn
          v-else
          block
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          @click="openCreatePipe"
        >
          Добавить трубу
        </v-btn>


        <v-btn
          v-if="networkStore.selectedObject"
          block
          color="error"
          variant="tonal"
          prepend-icon="mdi-close"
          @click="
            networkStore.clearSelectedObject()
          "
        >
          Закрыть паспорт
        </v-btn>

      </div>

    </v-card-actions>


    <PipeFormDialog
      v-model="pipeDialogOpen"
      :pipe="dialogPipe"
    />

  </v-card>
</template>


<style scoped>
.passport-actions {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 10px;
}

</style>