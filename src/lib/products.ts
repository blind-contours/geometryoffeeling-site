export interface PrintSize {
  id: string;
  label: string;
  dimensions: string;
  priceCents: number;
  prodigiSku: string;
}

export const PRINT_SIZES: PrintSize[] = [
  {
    id: "8x10",
    label: '8" x 10"',
    dimensions: "8x10",
    priceCents: 4500,
    prodigiSku: "GLOBAL-HPR-8X10",
  },
  {
    id: "16x20",
    label: '16" x 20"',
    dimensions: "16x20",
    priceCents: 9500,
    prodigiSku: "GLOBAL-HPR-16X20",
  },
  {
    id: "24x36",
    label: '24" x 36"',
    dimensions: "24x36",
    priceCents: 17500,
    prodigiSku: "GLOBAL-HPR-24X36",
  },
];

export const SHIPPING_COUNTRIES = [
  "US",
  "CA",
  "GB",
  "DE",
  "FR",
  "IT",
  "ES",
  "NL",
  "AU",
  "JP",
  "SE",
  "NO",
  "DK",
  "FI",
  "AT",
  "BE",
  "CH",
  "IE",
  "PT",
  "NZ",
];

export function getSizeById(id: string): PrintSize | undefined {
  return PRINT_SIZES.find((s) => s.id === id);
}

export function getPriceForSize(id: string): number | undefined {
  return getSizeById(id)?.priceCents;
}
