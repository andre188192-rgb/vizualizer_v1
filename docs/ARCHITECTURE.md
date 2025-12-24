# Architecture

## Coordinate Transform Convention

All transforms follow the convention:

```
p_mcs = T_mcs_from_tcp @ p_tcp
```

Naming is explicit: `T_<to>_from_<from>`. Vectors are column vectors, and
matrix multiplication is left-to-right.

## OpenGL Interop

OpenGL expects column-major matrices. The `Pose.apply_to_gl()` method
transposes the NumPy row-major matrix before calling `glMultMatrixf`.
