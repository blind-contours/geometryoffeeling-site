import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const baseUrl =
    process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: ["/api/", "/success"] },
      // Explicitly allow AI search bots
      { userAgent: "OAI-SearchBot", allow: "/" },
      { userAgent: "ChatGPT-User", allow: "/" },
      { userAgent: "ClaudeBot", allow: "/" },
      { userAgent: "PerplexityBot", allow: "/" },
      { userAgent: "Applebot", allow: "/" },
      // Block AI training-only bots
      { userAgent: "GPTBot", disallow: "/" },
      { userAgent: "Google-Extended", disallow: "/" },
      { userAgent: "anthropic-ai", disallow: "/" },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  };
}
