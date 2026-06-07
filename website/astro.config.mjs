// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// ---------------------------------------------------------------------------
// Hosting configuration
//
// This is currently set up for a GitHub Pages *project* site, served at
//   https://corydolphin.github.io/flask-cors
// which works with zero DNS setup.
//
// To move it onto a personal/custom domain (e.g. flask-cors.corydolphin.com):
//   1. Set `site` to the full custom URL and DELETE the `base` line below.
//   2. Add a `website/public/CNAME` file containing just the bare hostname.
//   3. Point a CNAME DNS record at corydolphin.github.io.
// ---------------------------------------------------------------------------
export default defineConfig({
  site: "https://corydolphin.github.io",
  base: "/flask-cors",

  integrations: [
    starlight({
      title: "Flask-CORS",
      description:
        "A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.",
      logo: {
        src: "./src/assets/logo.svg",
        replacesTitle: false,
      },
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/corydolphin/flask-cors",
        },
      ],
      editLink: {
        baseUrl:
          "https://github.com/corydolphin/flask-cors/edit/main/website/",
      },
      sidebar: [
        {
          label: "Start Here",
          items: [
            { label: "Overview", link: "/" },
            { label: "Getting Started", link: "/getting-started/" },
          ],
        },
        {
          label: "API Reference",
          items: [
            { label: "CORS (extension)", link: "/api/extension/" },
            { label: "cross_origin (decorator)", link: "/api/decorator/" },
          ],
        },
        {
          label: "Examples",
          items: [
            { label: "Extension", link: "/examples/extension/" },
            { label: "Decorator", link: "/examples/decorator/" },
            { label: "Blueprints", link: "/examples/blueprints/" },
          ],
        },
      ],
    }),
  ],
});
