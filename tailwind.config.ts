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
        muted: "#9A9A98",
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
        body: ["14px", { lineHeight: "1.8", fontWeight: "300" }],
        caption: ["11px", { letterSpacing: "0.08em", fontWeight: "300" }],
      },
      maxWidth: {
        content: "1200px",
      },
    },
  },
  plugins: [],
};
export default config;
