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

export const metadata: Metadata = {
  title: "Geometry of Feeling — Mathematical Fine Art",
  description:
    "Mathematical fine art for people who think precisely and feel deeply. Every piece begins with a human emotion and asks: what mathematical function has the same shape as this feeling?",
  keywords: [
    "mathematical fine art prints",
    "equation art prints",
    "mathematics and emotion art",
    "minimalist mathematical art",
    "geometry of feeling",
    "abstract math art",
    "scientific art prints",
  ],
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
