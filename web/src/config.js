const STORAGE_KEY = "app_server_config"

export async function loadServerConfig() {
  // 优先读取 localStorage（用户可在 app 内修改）
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      return JSON.parse(saved)
    } catch {
      // ignore
    }
  }

  // 读取 public/server-config.json 默认配置
  try {
    const res = await fetch("/server-config.json")
    const cfg = await res.json()
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cfg))
    return cfg
  } catch {
    // 兜底
    const fallback = { serverUrl: "http://127.0.0.1:18765" }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(fallback))
    return fallback
  }
}

export function saveServerConfig(cfg) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cfg))
  return cfg
}
