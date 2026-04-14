import type { MetadataRoute } from "next";
import { series, allPieces } from "@/data/series";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl =
    process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";
  const lastmod = new Date().toISOString();

  const staticPages: MetadataRoute.Sitemap = [
    { url: baseUrl, changeFrequency: "weekly", priority: 1.0, lastModified: lastmod },
    { url: `${baseUrl}/shop`, changeFrequency: "weekly", priority: 0.9, lastModified: lastmod },
    { url: `${baseUrl}/series`, changeFrequency: "weekly", priority: 0.8, lastModified: lastmod },
    { url: `${baseUrl}/about`, changeFrequency: "monthly", priority: 0.6, lastModified: lastmod },
    { url: `${baseUrl}/printing`, changeFrequency: "monthly", priority: 0.5, lastModified: lastmod },
    { url: `${baseUrl}/license`, changeFrequency: "monthly", priority: 0.3, lastModified: lastmod },
    { url: `${baseUrl}/custom`, changeFrequency: "monthly", priority: 0.6, lastModified: lastmod },
    { url: `${baseUrl}/help`, changeFrequency: "monthly", priority: 0.5, lastModified: lastmod },
  ];

  const collectionPages: MetadataRoute.Sitemap = [
    "minimalist-prints",
    "mathematical-art",
    "gifts-for-stem-lovers",
    "art-about-emotion",
  ].map((slug) => ({
    url: `${baseUrl}/collections/${slug}`,
    changeFrequency: "weekly" as const,
    priority: 0.85,
    lastModified: lastmod,
  }));

  const seriesPages: MetadataRoute.Sitemap = series.map((s) => ({
    url: `${baseUrl}/series/${s.id}`,
    changeFrequency: "weekly",
    priority: 0.8,
    lastModified: lastmod,
  }));

  const piecePages: MetadataRoute.Sitemap = allPieces.map((p) => ({
    url: `${baseUrl}/piece/${p.id}`,
    changeFrequency: "monthly",
    priority: 0.7,
    lastModified: lastmod,
  }));

  return [...staticPages, ...collectionPages, ...seriesPages, ...piecePages];
}
