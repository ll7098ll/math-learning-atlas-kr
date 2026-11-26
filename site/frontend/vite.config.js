import { fileURLToPath, URL } from "node:url";
import { readFileSync } from "node:fs";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwind from "@tailwindcss/vite";

export default defineConfig({
  base: "./",
  plugins: [
    react(),
    tailwind(),
    {
      name: "atlas-page-shell",
      transformIndexHtml(html) {
        return html.replace(/<!-- atlas-(header|footer) -->/g, (_, landmark) =>
          readFileSync(new URL(`./compat/shell/${landmark}.html`, import.meta.url), "utf8").trim());
      },
    },
  ],
  resolve: { alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) } },
  build: {
    outDir: "../../tmp/curriculum-explorer-build",
    assetsDir: "explorer-assets",
    emptyOutDir: true,
  },
});
