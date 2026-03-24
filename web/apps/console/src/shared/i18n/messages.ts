import zh from "../../../messages/zh.json"
import en from "../../../messages/en.json"
import type { Locale, Messages } from "./types"

const messages: Record<Locale, Messages> = { zh, en }

export function getMessages(locale: Locale): Messages {
  return messages[locale]
}
