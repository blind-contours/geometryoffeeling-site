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
    // Aesthetic/decor intent
    "minimalist fine art prints",
    "abstract wall art",
    "modern art prints",
    "fine art prints for home",
    "calm art for living room",
    "contemporary fine art prints",
    "museum quality art prints",
    // Math/science discovery
    "mathematical art prints",
    "equation art",
    "generative art prints",
    // Gift intent
    "gifts for math lovers",
    "unique art gifts",
    // Emotion
    "abstract art about emotion",
    // Brand
    "geometry of feeling",
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

const organizationJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Geometry of Feeling",
  url: baseUrl,
  description:
    "Geometry of Feeling creates minimalist fine art prints derived from mathematical equations. Each museum-quality giclée print begins with a human emotion — grief, connection, awe, desire — and renders it through the mathematical function that shares its shape. Printed on Hahnemühle German Etching 310gsm. Equation-based generative art for collectors, homes, and offices.",
  brand: { "@type": "Brand", name: "Geometry of Feeling" },
};

const websiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Geometry of Feeling",
  url: baseUrl,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${ibmPlexMono.variable} font-mono antialiased`}>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationJsonLd),
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(websiteJsonLd),
          }}
        />
        <Navigation />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
