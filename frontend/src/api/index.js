import axios from 'axios'

const api = axios.create({
  baseURL: 'https://cellknowledge.com.cn/pmmdb/',
  timeout: 10000,
})

// 化合物搜索
export const searchCompoundByName = (name) =>
  api.get('/api/search/compound/name', { params: { name } })

export const searchCompoundByCas = (cas) =>
  api.get('/api/search/compound/cas', { params: { cas } })

export const searchBySmiles = (querySmiles) =>
  api.get('/api/search/compound/smiles', { params: { querySmiles } })

// 真菌搜索
export const searchFungusByName = (name) =>
  api.get('/api/search/fungus/name', { params: { name } })

export const searchFungusByGenus = (genus) =>
  api.get('/api/search/fungus/genus', { params: { genus } })

export const searchFungusByFamily = (family) =>
  api.get('/api/search/fungus/family', { params: { family } })

// 获取详情
export const getFungusDetail = (id) =>
  api.get(`/api/fungus/${id}`)

export const getCompoundDetail = (id) =>
  api.get(`/api/compound/${id}`)

// 列表浏览
export const listFungi = (page = 1) =>
  api.get('/api/fungi', { params: { page } })

export const listCompounds = (page = 1) =>
  api.get('/api/compounds', { params: { page } })

// 提交和统计
export const submitData = (data) =>
  api.post('/api/submit', data)

export const getStatistics = () =>
  api.get('/api/statistics')

export default api