import type { Metadata } from "next";
import { allPieces } from "@/data/series";

export const metadata: Metadata = {
  title:
    "Shop Minimalist Fine Art Prints | Mathematical Art From $45 — Geometry of Feeling",
  alternates: { canonical: "/shop" },
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

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

export default function ShopLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: "All Fine Art Prints — Geometry of Feeling",
    numberOfItems: allPieces.length,
    itemListElement: allPieces.map((p, i) => ({
      "@type": "ListItem",
      position: i + 1,
      url: `${baseUrl}/piece/${p.id}`,
      name: p.title,
    })),
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {children}
    </>
  );
}
