import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Shop Minimalist Fine Art Prints | Mathematical Art From $45 — Geometry of Feeling",
  description:
    "Browse 170+ minimalist fine art prints derived from mathematical equations. Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
  openGraph: {
    title:
      "Shop Minimalist Fine Art Prints | Mathematical Art From $45 — Geometry of Feeling",
    description:
      "Browse 170+ minimalist fine art prints derived from mathematical equations. Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
    images: [{ url: "/prints/connection/connection_pendulum.jpg", width: 1680, height: 1155 }],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/prints/connection/connection_pendulum.jpg"],
  },
};

export default function ShopLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
