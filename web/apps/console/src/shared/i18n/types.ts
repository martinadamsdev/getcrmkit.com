import type zh from "../../../messages/zh.json"

export type Locale = "zh" | "en"
export type MessageKey = keyof typeof zh
export type Messages = Record<MessageKey, string>
