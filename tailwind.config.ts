import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#FAFAF8",
        surface: "#F2F0EC",
        border: "#E0DDD8",
        primary: "#1A1A18",
        secondary: "#6A6A68",
        muted: "#767674",
      },
      fontFamily: {
        mono: [
          "IBM Plex Mono",
          "JetBrains Mono",
          "Courier New",
          "monospace",
        ],
      },
      fontSize: {
        headline: ["18px", { letterSpacing: "0.05em", fontWeight: "400" }],
        "headline-lg": ["22px", { letterSpacing: "0.04em", fontWeight: "400" }],
        body: ["16px", { lineHeight: "1.8", fontWeight: "400" }],
        caption: ["12px", { letterSpacing: "0.08em", fontWeight: "400" }],
      },
      maxWidth: {
        content: "1200px",
        gallery: "1800px",
      },
      spacing: {
        "gallery-gap": "20px",
      },
    },
  },
  plugins: [],
};
export default config;
