const API_URL = 'http://127.0.0.1:8000'

export async function getVertices() {
  const response = await fetch(`${API_URL}/vertices/`)

  if (!response.ok) {
    throw new Error('Ошибка при загрузке вершин')
  }

  return response.json()
}

export async function getPipes() {
  const response = await fetch(`${API_URL}/pipes/`)

  if (!response.ok) {
    throw new Error('Ошибка при загрузке труб')
  }

  return response.json()
}

export async function getPipeParts() {
  const response = await fetch(`${API_URL}/pipe-parts/`)

  if (!response.ok) {
    throw new Error('Ошибка при загрузке частей труб')
  }

  return response.json()
}