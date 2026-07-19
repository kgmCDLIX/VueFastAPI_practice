<script setup>
import MapEditor from '../components/map/MapEditor.vue'
import ObjectPassportPanel from '../components/passport/ObjectPassportPanel.vue'
</script>

<template>
  <v-container fluid class="pa-6">
    <v-row>
      <v-col cols="12">
        <v-card variant="flat" class="pa-4">
          <v-card-title class="text-h4">
            Редактор трубопроводной сети
          </v-card-title>

          <v-card-subtitle>
            Прототип интерфейса для просмотра скважин, труб и частей труб.
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <MapEditor />
      </v-col>

      <v-col cols="12" md="4">
        <ObjectPassportPanel />
      </v-col>
    </v-row>
  </v-container>
</template>