export interface PrintSize {
  id: string;
  label: string;
  dimensions: string;
  priceCents: number;
  prodigiSku: string;
}

export const PRINT_SIZES: PrintSize[] = [
  {
    id: "12x8",
    label: '12" × 8"',
    dimensions: "12x8",
    priceCents: 4500,
    prodigiSku: "GLOBAL-HGE-8X12",
  },
  {
    id: "24x16",
    label: '24" × 16"',
    dimensions: "24x16",
    priceCents: 9500,
    prodigiSku: "GLOBAL-HGE-16X24",
  },
  {
    id: "36x24",
    label: '36" × 24"',
    dimensions: "36x24",
    priceCents: 17500,
    prodigiSku: "GLOBAL-HGE-24X36",
  },
  {
    id: "48x32",
    label: '48" × 32"',
    dimensions: "48x32",
    priceCents: 29500,
    prodigiSku: "GLOBAL-HGE-32X48",
  },
];

const LARGE_FORMAT_PIECE_IDS = new Set([
  "grief-void",
  "awe-eclipse",
  "comprehending-gravity",
  "peace-horizon",
  "connection-magnetic",
  "belonging-nest",
  "belonging-home",
  "belonging-warmth",
  "belonging-held",
  "peace-field-guardian",
  "desire-pursuit",
]);

export function getAvailableSizes(pieceId: string): PrintSize[] {
  if (LARGE_FORMAT_PIECE_IDS.has(pieceId)) return PRINT_SIZES;
  return PRINT_SIZES.filter((s) => s.id !== "48x32");
}

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
