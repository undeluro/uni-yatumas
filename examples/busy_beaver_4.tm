# The `4-state busy beaver` machine
#    from https://turingmachine.io/.
#    - instead of `0` use empty symbol `_`
#    - instead of `1` use an  symbol `*`
#
A
A + _ |> B + * |> R
A + * |> B + * |> L
B + _ |> A + * |> L
B + * |> C + _ |> L
C + _ |> H + * |> R
C + * |> D + * |> L  
D + _ |> D + * |> R
D + * |> A + _ |> R