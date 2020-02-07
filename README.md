# Deep Learning for Computer Vision

Taking notes and review using vscode

## Requirement

- visual studio code
- Markdown Preview Enhanced
- Prettier
- Graphviz
- markdownlint
- markdown+Math

### Configuration

1. `sudo apt install graphviz latexmk pandoc pdf2svg texlive-latex-extra`
1. install package graphviz for latex

   1. Downloading [graphviz-latex]
   1. Extract and copy file `.sty` (if not please check make-file to generate new one)

   ```bash
   mkdir /usr/share/texlive/texmf-dist/tex/latex/graphics/
   cp graphviz.sty /usr/share/texlive/texmf-dist/tex/latex/graphics/

   or
   mkdir /usr/share/texmf/tex/latex/graphviz/
   cp graphviz.sty /usr/share/texmf/tex/latex/graphviz/
   ```

1. Configure pdflatex or latex by adding `-shell-escape` for pdflatex

   1. For Texstudio
      Configurations -> Commands -> add `-shell-escape` flag

   1. For vscode and [latex-workshop]

      - `latex-workshop.latex.tools` -> add `"-shell-escape"` under pdflatex or latexmk

      - **Notice**: sometime the name of graph should not be same with tex file.

   1. vscode + [Markdown Preview Enhanced][mpe] + pandoc:
      a. [latex-workshop-code-chunk]

      - `markdown-preview-enhanced.enableScriptExecution`: true
      - ` ```latex {cmd=true} ``` `

        ```latex
        \documentclass{standalone}
        \usepackage[pdf]{graphviz}

        \begin{document}
        \digraph[scale=0.5]{abc}{
            b [ shape=none label=abc ];

            a -> b -> c;

        }
        \end{document}
        ```

1. How to Graphviz with latex-label in node

   1. dot2tex
   1. dot2texi

[mpe]: https://github.com/shd101wyy/vscode-markdown-preview-enhanced
[graphviz-latex]: https://ctan.org/pkg/graphviz?lang=en
[latex-workshop]: https://github.com/James-Yu/LaTeX-Workshop
[latex-workshop-code-chunk]: https://github.com/shd101wyy/markdown-preview-enhanced/blob/master/docs/code-chunk.md
