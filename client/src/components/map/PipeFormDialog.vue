<script setup>
import {
  computed,
  ref,
  watch,
} from 'vue'

import { useNetworkStore } from '../../stores/networkStore'


const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },

  pipe: {
    type: Object,
    default: null,
  },
})


const emit = defineEmits([
  'update:modelValue',
])


const networkStore =
  useNetworkStore()


const isSaving =
  ref(false)

const errorMessage =
  ref('')


const form = ref({
  name: '',
  diameter: null,
  material: '',
  condition: '',

  vertex_start_id: null,
  vertex_end_id: null,
})


const dialogOpen = computed({
  get() {
    return props.modelValue
  },

  set(value) {
    emit(
      'update:modelValue',
      value
    )
  },
})


const isEdit = computed(() => {
  return Boolean(
    props.pipe?.id
  )
})


const dialogTitle = computed(() => {
  return isEdit.value
    ? 'Редактирование трубы'
    : 'Добавление трубы'
})


const vertexOptions = computed(() => {
  return networkStore.vertices.map(
    vertex => ({
      title:
        `${vertex.name} (ID: ${vertex.id})`,

      value:
        vertex.id,
    })
  )
})


function resetForm() {
  errorMessage.value = ''

  if (props.pipe) {

    form.value = {
      name:
        props.pipe.name ?? '',

      diameter:
        props.pipe.diameter ?? null,

      material:
        props.pipe.material ?? '',

      condition:
        props.pipe.condition ?? '',

      vertex_start_id:
        props.pipe.vertex_start_id ?? null,

      vertex_end_id:
        props.pipe.vertex_end_id ?? null,
    }

    return
  }


  form.value = {
    name: '',
    diameter: null,
    material: '',
    condition: '',

    vertex_start_id: null,
    vertex_end_id: null,
  }
}


watch(
  () => props.modelValue,

  (opened) => {
    if (opened) {
      resetForm()
    }
  }
)


function closeDialog() {
  dialogOpen.value = false
}


async function savePipe() {

  errorMessage.value = ''


  if (!form.value.name.trim()) {
    errorMessage.value =
      'Укажите название трубы'

    return
  }


  if (
    form.value.vertex_start_id === null ||
    form.value.vertex_end_id === null
  ) {
    errorMessage.value =
      'Выберите начало и конец трубы'

    return
  }


  if (
    form.value.vertex_start_id ===
    form.value.vertex_end_id
  ) {
    errorMessage.value =
      'Начало и конец трубы должны отличаться'

    return
  }


  const payload = {
    name:
      form.value.name.trim(),

    diameter:
      form.value.diameter === '' ||
      form.value.diameter === null
        ? null
        : String(
            form.value.diameter
          ).trim(),

    material:
      form.value.material.trim()
        || null,

    condition:
      form.value.condition.trim()
        || null,

    vertex_start_id:
      Number(
        form.value.vertex_start_id
      ),

    vertex_end_id:
      Number(
        form.value.vertex_end_id
      ),
  }


  isSaving.value = true


  try {

    if (isEdit.value) {

      await networkStore.updatePipe(
        props.pipe.id,
        payload
      )

    } else {

      await networkStore.createPipe(
        payload
      )
    }


    closeDialog()

  } catch (error) {

    errorMessage.value =
      error.message

  } finally {

    isSaving.value = false
  }
}
</script>


<template>
  <v-dialog
    v-model="dialogOpen"
    max-width="650"
  >

    <v-card>

      <v-card-title>
        {{ dialogTitle }}
      </v-card-title>


      <v-card-text>

        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ errorMessage }}
        </v-alert>


        <v-text-field
          v-model="form.name"
          label="Название трубы"
          variant="outlined"
        />


        <v-text-field
          v-model="form.diameter"
          label="Диаметр"
          type="number"
          variant="outlined"
        />


        <v-text-field
          v-model="form.material"
          label="Материал"
          variant="outlined"
        />


        <v-text-field
          v-model="form.condition"
          label="Состояние"
          variant="outlined"
        />


        <v-select
          v-model="form.vertex_start_id"
          :items="vertexOptions"
          item-title="title"
          item-value="value"
          label="Начало трубы"
          variant="outlined"
        />


        <v-select
          v-model="form.vertex_end_id"
          :items="vertexOptions"
          item-title="title"
          item-value="value"
          label="Конец трубы"
          variant="outlined"
        />

      </v-card-text>


      <v-card-actions>

        <v-spacer />


        <v-btn
          variant="text"
          :disabled="isSaving"
          @click="closeDialog"
        >
          Отмена
        </v-btn>


        <v-btn
          color="primary"
          variant="flat"
          :loading="isSaving"
          @click="savePipe"
        >
          {{
            isEdit
              ? 'Сохранить'
              : 'Добавить'
          }}
        </v-btn>

      </v-card-actions>

    </v-card>

  </v-dialog>
</template>