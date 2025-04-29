# The `3-state busy beaver` machine from https://turingmachine.io/.
#    - instead of `0` use empty symbol `_`
#    - instead of `1` use an  symbol `*`
A
A + _ |> B + * |> R 
A + * |> C + * |> L
B + _ |> A + * |> L
B + * |> B + * |> R
C + _ |> B + * |> L
C + * |> H + * |> L