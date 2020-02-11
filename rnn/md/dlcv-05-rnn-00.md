---
output: pdf_document
export_on_save:
  pandoc: false
---

# Overview RNN

```dot {}
digraph G {
    # Global
    node [shape=plaintext]

    # define nodes
    h [textlbl="$h_t = f_w(h_{t-1}, x_t)$" label="hidden_layer"]
    fnn [label="standard feed forward nn", shape=box, style=filled]
    aenn [label="auto encoder-decoder layers"]
    seq [label="Sequence Models"]
    str [label="RNN Structure"]
    virtue [label="virtue-propagation"]
    nrnn [label="multi layer rnn"]
    # Top
    rnn -> seq
    rnn -> str

    # Models
    node [shape=box]
    seq -> "one-to-one"
    seq -> "1-n"
    seq -> "n-n"
    seq -> "n-1"

    # Application Example
    node [shape=plaintext]

    "one-to-one"-> classification [label=ex]
    classification -> "1 tensor image - 1 class"

    # Structure
    str -> h
    h -> fnn [label="unfolded, same W" fontcolor=red]
    fnn -> fnn [label="backprop" fontcolor=blue]
    h -> aenn [label="ex: 2 layers, 2 W", style=dotted]
    aenn -> "encoder: n-1"
    aenn -> "decoder: 1-n"
    str -> virtue [style="dotted"]
    virtue -> "already-deep" [label="unfolded -> n steps"
                              style=dotted]

    # multi-layer rnn
    str -> nrnn [label="complex rnn"]
    nrnn -> aenn [label=ex]


}
```

## Hidden Layer

$y_t = W_{hy} * h_t$

- $y_t = y_{t-1} + W * X_t = W_{hy}h_t$

$h_t = f_w(h_{t-1}, x_t)$

- ex: $h_t = \tanh(W_{hh} h_{t-1} + W_{xh} * X) = = tanh(W\begin{bmatrix}h_{t-1} \\ X\end{bmatrix})$

- Generally
  $ h_t^l = tanh(W_l\begin{bmatrix}h_t^{l-1} \\ h_t^{l}\end{bmatrix})$

```dot
digraph training_graph{

  node [shape=plaintext]

  # How to train
  tr [label=training]
  stdc [label="standard computational graph"]
  chunk [label="chunks~as~windows"]

  rnn -> tr
  tr -> stdc [label=unfold]
  stdc -> loss [label=compute]
  loss -> gradient [label="compute"]
  gradient -> stdc [label="backprop"]
  gradient -> problem
  problem -> "whole-data" [label="computing expensive", style=dotted]
  problem -> "truncated backprop" [label="solved by" style=dotted]
  "truncated backprop" -> chunk
  chunk -> forward [label="carry states"]
  chunk -> backprop [label="compute gradient for a window"]
}
```
