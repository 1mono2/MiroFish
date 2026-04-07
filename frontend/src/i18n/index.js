import { createI18n } from 'vue-i18n'
import languages from '@locales/languages.json'
import en from '@locales/en.json'
import ja from '@locales/ja.json'
import zh from '@locales/zh.json'

const messages = { en, ja, zh }

const availableLocales = Object.keys(messages).map((key) => ({
  key,
  label: languages[key].label
}))

const savedLocale = localStorage.getItem('locale') || 'ja'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'ja',
  messages
})

export { availableLocales }
export default i18n
