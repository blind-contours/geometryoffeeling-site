import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Shop — Geometry of Feeling",
  description:
    "Museum-grade fine art prints on Hahnemuhle German Etching 310gsm. Free shipping on every order.",
  openGraph: {
    title: "Shop — Geometry of Feeling",
    description:
      "Museum-grade fine art prints on Hahnemuhle German Etching 310gsm. Free shipping on every order.",
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
