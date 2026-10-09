const API_URL = 'http://127.0.0.1:8000'

function getApiErrorMessage(errorData, fallback) {
  const detail = errorData?.detail

  if (!detail) {
    return fallback
  }

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail
      .map(error => {
        const location = Array.isArray(error.loc)
          ? error.loc
              .filter(item => item !== 'body')
              .join('.')
          : ''

        const message =
          error.msg ?? 'Ошибка данных'

        return location
          ? `${location}: ${message}`
          : message
      })
      .join('; ')
  }

  if (typeof detail === 'object') {
    return JSON.stringify(detail)
  }

  return String(detail)
}

async function request(url, errorMessage) {
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(errorMessage)
  }

  return response.json()
}

export function getVertices() {
  return request(`${API_URL}/vertices/`, 'Ошибка при загрузке вершин')
}

export function getPipes() {
  return request(`${API_URL}/pipes/`, 'Ошибка при загрузке труб')
}

export function getPipeParts() {
  return request(`${API_URL}/pipe-parts/`, 'Ошибка при загрузке частей труб')
}

export async function getNetworkGeoJson() {
  const response = await fetch(
    'http://127.0.0.1:8000/geo/network'
  )

  if (!response.ok) {
    throw new Error('Не удалось загрузить геометрию сети')
  }

  return response.json()
}

export async function createPipe(data) {
  const response = await fetch(
    `${API_URL}/pipes/`,
    {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify(data),
    }
  )

  if (!response.ok) {
    const errorData = await response.json()

    console.error(
      'CREATE PIPE ERROR:',
      errorData
    )

    throw new Error(
      getApiErrorMessage(
        errorData,
        'Не удалось создать трубу'
      )
    )
  }

  return response.json()
}


export async function updatePipe(
  pipeId,
  data
) {
  const response = await fetch(
    `${API_URL}/pipes/${pipeId}`,
    {
      method: 'PATCH',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify(data),
    }
  )

  if (!response.ok) {
    const errorData = await response.json()

    console.error(
      'UPDATE PIPE ERROR:',
      errorData
    )

    throw new Error(
      getApiErrorMessage(
        errorData,
        'Не удалось изменить трубу'
      )
    )
  }

  return response.json()
}