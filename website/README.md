# Flask-CORS documentation site

A modern documentation site for Flask-CORS, built with
[Astro Starlight](https://starlight.astro.build/).

## Local development

```sh
cd website
npm install
npm run dev      # start a local dev server at localhost:4321
npm run build    # build the production site into ./dist
npm run preview  # preview the production build locally
```

## Content

All pages live in `src/content/docs/` as Markdown / MDX:

- `index.mdx` — landing page
- `getting-started.md` — install + quickstart
- `api/` — hand-written API reference for `CORS` and `cross_origin`
- `examples/` — usage examples

The site navigation is configured in `astro.config.mjs`.

## Deployment

The site is built and deployed to GitHub Pages automatically by
`.github/workflows/docs.yml` on every push to `main`.

By default it publishes to the GitHub Pages *project* URL
(`https://corydolphin.github.io/flask-cors`). See the comment at the top of
`astro.config.mjs` for how to switch to a custom domain.
