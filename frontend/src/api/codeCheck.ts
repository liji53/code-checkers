import axios from 'axios'
export type checkerItem = {
  value: string
  name: string
}

export const getLanguages = async () => {
  return await axios.get('/api/v1/code/languages')
}

export const getCheckers = async (params: object) => {
  return await axios.get('/api/v1/code/checkers', { params })
}

export const deleteFile = async (data: object) => {
  return await axios.post('/api/v1/code/clear', data)
}
