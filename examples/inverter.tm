# Probably the simplest TM to understand
# Changes 0 to 1 and 1 to 0
start
start + 0 |> start + 1 |> R
start + 1 |> start + 0 |> R
start + _ |> H + _ |> R