const API_URL = 'http://127.0.0.1:8000'

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