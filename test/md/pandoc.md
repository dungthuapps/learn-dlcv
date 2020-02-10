---
title: How to learn pandoc and markdown
output:
  pdf_document:
    path: build/build.pdf
    includes:
      in_header: ./tikz-preamble.tex
    filter: ./dot2tex-filter.py
pandoc_args:
  - "--toc"
  #   - "--standalone"
  #   - "--include-in-header=./tikz-preamble.tex"
  - "--include-in-header=./tikz-preamble.tex"
  - "--filter=./dot2tex-filter.py"
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
  label="X_5"
  caption="My graph"

  C [texlbl="$C_x$"]
  A -> B -> C;
  A -> C;
}
```

Notice:

- currently filter failed
- find the way to render (1) katex -> (2) dot (viz.js)

## Alternative with dot2tex (ugly)

1. use dot2tex -> convert to tex
1. copy from \begin{tickzpicture} ... \end{tickzpicture} to $$...$$
1. use pandoc to generate pdf/rendering
