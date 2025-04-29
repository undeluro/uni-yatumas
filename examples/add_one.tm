# Adds 1 to a binary number
right
right + 1 |> right + 1 |> R
right + 0 |> right + 0 |> R
right + _ |> carrying + _ |> L
carrying + 1 |> carrying + 0 |> L
carrying + 0 |> done + 1 |> L
carrying + _ |> done + 1 |> L  