import { defineStore } from 'pinia'

import {
  getVertices,
  getPipes,
  getPipeParts,
} from '../api/networkApi'

export const useNetworkStore = defineStore('networkStore', {
  state: () => ({
    selectedObject: null,

    vertices: [],
    pipes: [],
    pipeParts: [],

    isLoading: false,
    error: null,
  }),

  actions: {
    async loadNetworkData() {
      this.isLoading = true
      this.error = null

      try {
        const [vertices, pipes, pipeParts] = await Promise.all([
          getVertices(),
          getPipes(),
          getPipeParts(),
        ])

        this.vertices = vertices
        this.pipes = pipes
        this.pipeParts = pipeParts
      } catch (error) {
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },

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