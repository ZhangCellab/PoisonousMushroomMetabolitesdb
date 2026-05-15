// Ketcher 结构编辑器配置
export const initializeKetcher = async (containerId) => {
  // 动态加载 Ketcher 库
  if (!window.Ketcher) {
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/ketcher-core@2.13.2/dist/ketcher.js'
    script.type = 'module'
    document.head.appendChild(script)
    
    await new Promise(resolve => {
      script.onload = resolve
    })
  }
  
  // 创建 Ketcher 实例
  const ketcher = await window.Ketcher.create({
    target: document.getElementById(containerId),
    settings: {
      appSettings: {
        showAtomIds: false,
        showValenceWarnings: true,
      }
    }
  })
  
  return ketcher
}

// 获取 SMILES
export const getSmilesFromKetcher = async (ketcher) => {
  try {
    return await ketcher.getSmiles()
  } catch (error) {
    console.error('Failed to obtain SMILES:', error)
    return null
  }
}

// 设置 SMILES
export const setSmilesToKetcher = async (ketcher, smiles) => {
  try {
    await ketcher.setMolecule(smiles)
  } catch (error) {
    console.error('Failed to set SMILES:', error)
  }
}