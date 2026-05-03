import { createApp } from "vue"
import { createPinia } from "pinia"
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import * as ElementPlusIconsVue from "@element-plus/icons-vue"

import App from "./App.vue"
import router from "./router"
import "./styles/global.css"
import { loadServerConfig } from "./config"
import { updateBaseURL } from "./api"

async function bootstrap() {
  // 先加载服务端配置，再挂载 app
  const config = await loadServerConfig()
  window.__APP_CONFIG = config
  updateBaseURL()

  const app = createApp(App)
  for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
  app.use(createPinia())
  app.use(router)
  app.use(ElementPlus, { locale: undefined })
  app.mount("#app")
}

bootstrap()
