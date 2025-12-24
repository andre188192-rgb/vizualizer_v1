# Architecture

## Coordinate Conventions

All transformations follow the CNC simulator convention:

- Vectors are homogeneous 4x1 column vectors.
- Multiplication is left-to-right.
- Transformations are named as `T_<to>_from_<from>`.

Example:

```
# p_mcs = T_mcs_from_tcp @ p_tcp
```

Renderers and material removal must consume `Pose` only. UI modules may not
translate axes directly or apply local axis inversions.
