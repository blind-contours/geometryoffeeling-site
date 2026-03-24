import type { Metadata } from "next";
import { IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Footer from "@/components/Footer";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  variable: "--font-mono",
});

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

const defaultTitle = "Geometry of Feeling — Mathematical Fine Art";
const defaultDescription =
  "Mathematical fine art for people who think precisely and feel deeply. Every piece begins with a human emotion and asks: what mathematical function has the same shape as this feeling?";
const defaultOgImage = "/prints/awe/awe_singularity.jpg";

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: defaultTitle,
  description: defaultDescription,
  keywords: [
    "mathematical fine art prints",
    "equation art prints",
    "mathematics and emotion art",
    "minimalist mathematical art",
    "geometry of feeling",
    "abstract math art",
    "scientific art prints",
  ],
  openGraph: {
    title: defaultTitle,
    description: defaultDescription,
    siteName: "Geometry of Feeling",
    images: [{ url: defaultOgImage, width: 1680, height: 1155 }],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: defaultTitle,
    description: defaultDescription,
    images: [defaultOgImage],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${ibmPlexMono.variable} font-mono antialiased`}>
        <Navigation />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
