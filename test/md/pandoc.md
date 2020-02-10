---
title: How to learn pandoc and markdown
output:
  pdf_document:
    path: build/build.pdf
    include:
      in_header: ./tikz-preamble.tex
pandoc_args:
  - "--toc"
  - "--standalone"
  # - "--include-in-header=./tikz-preamble.tex"
  # - "--filter=./dot2tex-filter.py"
---

## Pandoc + Markdown + Latex + Graphviz

1. set in settings.json

   ```json
   "markdown-preview-enhanced.usePandocParser": true,
   ```

   **Notice**: it will replace default markdown-it parser

1. Example

```dot
digraph {
  label="my graph here"
  caption="My graph"

  C [texlbl="$C_x$"]
  A -> B -> C;
  A -> C;
}
```

Notice:

- currently doc2tex filter failed with pandoc -> need to rewrite
- find the way to render (1) katex -> (2) dot (viz.js)
- not good solution for markdown + katex-graph
