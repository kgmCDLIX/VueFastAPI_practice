import { defineStore } from 'pinia'

export const useNetworkStore = defineStore('networkStore', {
  state: () => ({
    selectedObject: null,

    vertices: [
      {
        id: 1,
        name: 'Скважина 101',
        type: 'Скважина',
        condition: 'Работает',
        depth: '2500 м',
      },
      {
        id: 2,
        name: 'Скважина 102',
        type: 'Скважина',
        condition: 'Работает',
        depth: '2300 м',
      },
    ],

    pipes: [
      {
        id: 1,
        name: 'Труба 1',
        condition: 'Исправна',
        diameter: '530 мм',
        material: 'Сталь',
        vertexStartId: 1,
        vertexEndId: 2,
      },
    ],

    pipeParts: [
      {
        id: 1,
        name: 'Часть трубы 1.1',
        condition: 'Исправна',
        length: '50 м',
        pipeId: 1,
      },
      {
        id: 2,
        name: 'Часть трубы 1.2',
        condition: 'Требует осмотра',
        length: '70 м',
        pipeId: 1,
      },
    ],
  }),

  actions: {
    selectObject(type, data) {
      this.selectedObject = {
        type,
        data,
      }
    },

    clearSelectedObject() {
      this.selectedObject = null
    },
  },
})