<script setup>
import {
  onMounted,
  onBeforeUnmount,
  ref,
  watch,
} from 'vue'

import Map from 'ol/Map'
import View from 'ol/View'

import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'

import OSM from 'ol/source/OSM'
import VectorSource from 'ol/source/Vector'

import GeoJSON from 'ol/format/GeoJSON'

import Select from 'ol/interaction/Select'
import { click } from 'ol/events/condition'

import {
  Style,
  Stroke,
  Fill,
  Circle as CircleStyle,
} from 'ol/style'

import 'ol/ol.css'

import { useNetworkStore } from '@/stores/networkStore'


const networkStore = useNetworkStore()

const mapElement = ref(null)

let map = null
let vectorSource = null
let vectorLayer = null
let selectInteraction = null


// -----------------------------
// СТИЛИ ОБЪЕКТОВ
// -----------------------------

function getFeatureStyle(feature) {
  const objectType = feature.get('object_type')


  // Скважина / вершина
  if (objectType === 'vertex') {
    return new Style({
      image: new CircleStyle({
        radius: 9,

        fill: new Fill({
          color: '#43a047',
        }),

        stroke: new Stroke({
          color: '#ffffff',
          width: 2,
        }),
      }),
    })
  }


  // Труба
  if (objectType === 'pipe') {
    return new Style({
      stroke: new Stroke({
        color: '#555555',
        width: 7,
      }),
    })
  }


  // Часть трубы
  if (objectType === 'pipe_part') {
    return new Style({
      stroke: new Stroke({
        color: '#2196f3',
        width: 3,
        lineDash: [10, 8],
      }),
    })
  }


  return new Style({
    stroke: new Stroke({
      color: '#999999',
      width: 2,
    }),
  })
}


// -----------------------------
// ЗАГРУЗКА GEOJSON НА КАРТУ
// -----------------------------

function renderNetwork() {
  if (!vectorSource) {
    return
  }

  vectorSource.clear()


  if (!networkStore.networkGeoJson) {
    return
  }


  const features = new GeoJSON().readFeatures(
    networkStore.networkGeoJson,
    {
      dataProjection: 'EPSG:4326',
      featureProjection: 'EPSG:3857',
    }
  )


  vectorSource.addFeatures(features)


  if (features.length > 0 && map) {
    map.getView().fit(
      vectorSource.getExtent(),
      {
        padding: [70, 70, 70, 70],
        maxZoom: 16,
        duration: 400,
      }
    )
  }
}


// -----------------------------
// СОЗДАНИЕ КАРТЫ
// -----------------------------

onMounted(() => {
  vectorSource = new VectorSource()


  vectorLayer = new VectorLayer({
    source: vectorSource,
    style: getFeatureStyle,
  })


  map = new Map({
    target: mapElement.value,

    layers: [

      // Обычная карта OpenStreetMap
      new TileLayer({
        source: new OSM(),
      }),

      // Наши трубы и скважины
      vectorLayer,
    ],

    view: new View({
      center: [0, 0],
      zoom: 2,
    }),
  })


  // -----------------------------
  // ВЫБОР ОБЪЕКТА МЫШКОЙ
  // -----------------------------

  selectInteraction = new Select({
    condition: click,

    layers: [
      vectorLayer,
    ],

    hitTolerance: 8,
  })


  map.addInteraction(
    selectInteraction
  )


  selectInteraction.on(
    'select',
    (event) => {
      const feature =
        event.selected[0]


      if (!feature) {
        networkStore.clearSelectedObject()
        return
      }


      const properties =
        feature.getProperties()


      const {
        geometry,
        object_type,
        ...data
      } = properties


      let type = object_type


      // Наш ObjectPassportPanel
      // уже использует такое имя
      if (object_type === 'pipe_part') {
        type = 'pipePart'
      }


      networkStore.selectObject(
        type,
        data
      )
    }
  )


  renderNetwork()
})


// -----------------------------
// ЕСЛИ GEOJSON ЗАГРУЗИЛСЯ
// ПОСЛЕ СОЗДАНИЯ КАРТЫ
// -----------------------------

watch(
  () => networkStore.networkGeoJson,

  () => {
    renderNetwork()
  },

  {
    deep: true,
  }
)


// -----------------------------
// УНИЧТОЖЕНИЕ КАРТЫ
// -----------------------------

onBeforeUnmount(() => {
  if (map) {
    map.setTarget(undefined)
    map = null
  }
})
</script>


<template>
  <v-card class="pa-4">
    <v-card-title>
      Карта трубопроводной сети
    </v-card-title>


    <div
      v-if="networkStore.isLoading"
      class="state-message"
    >
      Загрузка сети...
    </div>


    <div
      v-else-if="networkStore.error"
      class="state-message error-message"
    >
      {{ networkStore.error }}
    </div>


    <div
      ref="mapElement"
      class="network-map"
    />
  </v-card>
</template>


<style scoped>
.network-map {
  width: 100%;
  height: 600px;

  border: 1px solid #dddddd;
  border-radius: 8px;

  overflow: hidden;
}

.state-message {
  padding: 20px;
  text-align: center;
  color: #666666;
}

.error-message {
  color: #d32f2f;
}
</style>