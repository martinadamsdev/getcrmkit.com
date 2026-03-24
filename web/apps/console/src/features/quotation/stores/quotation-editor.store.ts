import { create } from "zustand"

export type QuotationLineItem = {
  id: string
  productId: string
  productName: string
  material: string | null
  quantity: number
  costPrice: number
  costCurrency: string
  unitPrice: number
  sellingCurrency: string
  multiplier: number | null
  subtotal: number
  customizationIds: string[]
  customizationCost: number
  notes: string
  position: number
}

export type ProfitResult = {
  totalAmount: number
  totalCost: number
  totalProfit: number
  profitRate: number
  freight: number
  insurance: number
  grandTotal: number
}

type QuotationEditorState = {
  // Line items
  items: QuotationLineItem[]
  // Trade settings
  tradeTerm: string
  currency: string
  exchangeRate: number
  // Costs
  freight: number
  insurance: number
  otherCost: number
  // Profit
  optimisticProfit: ProfitResult | null
  serverProfit: ProfitResult | null
  // Meta
  isDirty: boolean
  isCalculating: boolean
  // Actions
  addItem: (item: QuotationLineItem) => void
  removeItem: (itemId: string) => void
  updateItem: (itemId: string, patch: Partial<QuotationLineItem>) => void
  setTradeTerm: (term: string) => void
  setCurrency: (currency: string) => void
  setExchangeRate: (rate: number) => void
  setFreight: (freight: number) => void
  setInsurance: (insurance: number) => void
  setOtherCost: (cost: number) => void
  recalculateOptimistic: () => void
  applyServerProfit: (result: ProfitResult) => void
  setIsCalculating: (v: boolean) => void
  loadQuotation: (data: {
    items: QuotationLineItem[]
    tradeTerm: string
    currency: string
    freight: number
    insurance: number
    otherCost: number
    exchangeRate: number
  }) => void
  reset: () => void
}

const initialState = {
  items: [] as QuotationLineItem[],
  tradeTerm: "FOB",
  currency: "USD",
  exchangeRate: 1.0,
  freight: 0,
  insurance: 0,
  otherCost: 0,
  optimisticProfit: null as ProfitResult | null,
  serverProfit: null as ProfitResult | null,
  isDirty: false,
  isCalculating: false,
}

export const useQuotationEditorStore = create<QuotationEditorState>(
  (set, get) => ({
    ...initialState,

    addItem: (item) =>
      set((s) => ({
        items: [...s.items, item],
        isDirty: true,
      })),

    removeItem: (itemId) =>
      set((s) => {
        const newItems = s.items.filter((i) => i.id !== itemId)
        return {
          items: newItems,
          isDirty: true,
          ...(newItems.length === 0
            ? { serverProfit: null, optimisticProfit: null }
            : {}),
        }
      }),

    updateItem: (itemId, patch) =>
      set((s) => ({
        items: s.items.map((i) =>
          i.id === itemId ? { ...i, ...patch } : i,
        ),
        isDirty: true,
      })),

    setTradeTerm: (term) => set({ tradeTerm: term, isDirty: true }),
    setCurrency: (currency) => set({ currency, isDirty: true }),
    setExchangeRate: (rate) => set({ exchangeRate: rate, isDirty: true }),
    setFreight: (freight) => set({ freight, isDirty: true }),
    setInsurance: (insurance) => set({ insurance, isDirty: true }),
    setOtherCost: (cost) => set({ otherCost: cost, isDirty: true }),

    recalculateOptimistic: () => {
      const { items, freight, insurance, otherCost } = get()
      const totalAmount = items.reduce((sum, i) => sum + i.subtotal, 0)
      const totalCost = items.reduce(
        (sum, i) => sum + i.costPrice * i.quantity + i.customizationCost,
        0,
      )
      const grandTotal = totalAmount + freight + insurance + otherCost
      const totalProfit = totalAmount - totalCost
      const profitRate = totalAmount > 0 ? totalProfit / totalAmount : 0

      set({
        optimisticProfit: {
          totalAmount,
          totalCost,
          totalProfit,
          profitRate,
          freight,
          insurance,
          grandTotal,
        },
      })
    },

    applyServerProfit: (result) => set({ serverProfit: result, isCalculating: false }),

    setIsCalculating: (v) => set({ isCalculating: v }),

    loadQuotation: (data) =>
      set({
        items: data.items,
        tradeTerm: data.tradeTerm,
        currency: data.currency,
        freight: data.freight,
        insurance: data.insurance,
        otherCost: data.otherCost,
        exchangeRate: data.exchangeRate,
        isDirty: false,
        isCalculating: false,
        serverProfit: null,
        optimisticProfit: null,
      }),

    reset: () => set({ ...initialState }),
  }),
)
