import { defineStore } from 'pinia'

import {
  getVertices,
  getPipes,
  getPipeParts,
  getNetworkGeoJson,

  createPipe as createPipeRequest,
  updatePipe as updatePipeRequest,
} from '../api/networkApi'


export const useNetworkStore = defineStore(
  'networkStore',
  {
    state: () => ({
      selectedObject: null,

      vertices: [],
      pipes: [],
      pipeParts: [],

      networkGeoJson: null,

      isLoading: false,
      error: null,
    }),


    actions: {

      async loadNetworkData() {
        this.isLoading = true
        this.error = null

        try {
          const [
            vertices,
            pipes,
            pipeParts,
            networkGeoJson,
          ] = await Promise.all([
            getVertices(),
            getPipes(),
            getPipeParts(),
            getNetworkGeoJson(),
          ])

          this.vertices = vertices
          this.pipes = pipes
          this.pipeParts = pipeParts

          this.networkGeoJson =
            networkGeoJson

        } catch (error) {
          this.error = error.message

        } finally {
          this.isLoading = false
        }
      },


      async createPipe(data) {
        this.error = null

        try {
          const createdPipe =
            await createPipeRequest(data)

          await this.loadNetworkData()

          const freshPipe =
            this.pipes.find(
              pipe =>
                pipe.id === createdPipe.id
            )

          if (freshPipe) {
            this.selectObject(
              'pipe',
              freshPipe
            )
          }

          return createdPipe

        } catch (error) {
          this.error = error.message
          throw error
        }
      },


      async updatePipe(
        pipeId,
        data
      ) {
        this.error = null

        try {
          const updatedPipe =
            await updatePipeRequest(
              pipeId,
              data
            )

          await this.loadNetworkData()

          const freshPipe =
            this.pipes.find(
              pipe =>
                pipe.id === updatedPipe.id
            )

          if (freshPipe) {
            this.selectObject(
              'pipe',
              freshPipe
            )
          }

          return updatedPipe

        } catch (error) {
          this.error = error.message
          throw error
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
  }
)