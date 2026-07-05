import { defineStore } from 'pinia'

export const usePipeStore = defineStore('pipeStore', {
  state: () => ({
    pipes: [
      {
        id: 1,
        name: 'Труба №1',
        length: '120 м',
        condition: 'Исправна'
      },
      {
        id: 2,
        name: 'Труба #2',
        length: '250 м',
        condition: 'Требует осмотра'
      }
    ],

    selectedPipe: null
  }),

  actions: {
    selectPipe(pipe) {
      this.selectedPipe = pipe
    },

    clearSelectedPipe() {
      this.selectedPipe = null
    }
  }
})