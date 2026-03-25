export interface PrintSize {
  id: string;
  label: string;
  dimensions: string;
  priceCents: number;
  prodigiSku: string;
}

export const PRINT_SIZES: PrintSize[] = [
  {
    id: "10x8",
    label: '10" × 8"',
    dimensions: "10x8",
    priceCents: 4500,
    prodigiSku: "GLOBAL-HPR-8X10",
  },
  {
    id: "20x16",
    label: '20" × 16"',
    dimensions: "20x16",
    priceCents: 9500,
    prodigiSku: "GLOBAL-HPR-16X20",
  },
  {
    id: "36x24",
    label: '36" × 24"',
    dimensions: "36x24",
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
