# CoordinatePaths

A Python library for generating coordinate paths for automated scanning systems (XYZ stages, laser scanners, EM probes, etc.).

## Features

- **Rectangular Path**: Snake-like raster scanning pattern
- **Circular Path**: Spiral scanning from center outward
- **Polygon Path**: Raster scanning within arbitrary polygonal areas
- **Extensible**: Easy to add custom path patterns
- High-precision coordinates using `decimal.Decimal`
- Built-in visualization with matplotlib
- Iterator interface for easy scanning loops

## Installation

```bash
pip install coordinate-paths
```

Or install from source:

```bash
git clone git@github.com:HWS-XMS/CoordinatePaths.git
cd CoordinatePaths
pip install -e .
```

## Usage

### Rectangular Path

```python
from coordinate_paths import RectangularPath
import decimal

path = RectangularPath(
    start_xy=(decimal.Decimal('0'), decimal.Decimal('0')),
    end_xy=(decimal.Decimal('10'), decimal.Decimal('10')),
    step_size_x=decimal.Decimal('0.5'),
    step_size_y=decimal.Decimal('0.5')
)

# Iterate over coordinates
for x, y in path:
    print(f"Position: ({x}, {y})")

# Or access directly
print(f"Total points: {len(path.coordinates)}")
```

### Circular Path

```python
from coordinate_paths import CircularPath
import decimal

path = CircularPath(
    center_xy=(decimal.Decimal('10'), decimal.Decimal('10')),
    radius=decimal.Decimal('5'),
    step_size=decimal.Decimal('0.5')
)

# Visualize the path
path.plot()
```

## Path Patterns

### RectangularPath

Generates a snake-like scanning pattern:
```
END →→→#
    ↑  ↓
    ←←←←
    ↑  ↓
    →→→→
    ↑  ↓
    ←←←# START
```

Parameters:
- `start_xy`: Starting corner (x, y) coordinates
- `end_xy`: Ending corner (x, y) coordinates
- `step_size_x`: Step size in X direction
- `step_size_y`: Step size in Y direction
- `start_at_index`: Optional index to start from (default: 1)
- `random`: Randomize point order (default: False)

### CircularPath

Generates a spiral scanning pattern from center outward in concentric circles.

Parameters:
- `center_xy`: Center point (x, y) coordinates
- `radius`: Maximum radius from center
- `step_size`: Approximate distance between points
- `start_at_index`: Optional index to start from (default: 1)

### PolygonPath

Generates a raster scanning pattern within an arbitrary polygon defined by its vertices. Uses ray casting to determine which points fall inside the polygon boundary.

```python
from coordinate_paths import PolygonPath
import decimal

# Define a triangular scanning area
path = PolygonPath(
    vertices=[
        (decimal.Decimal('0'), decimal.Decimal('0')),
        (decimal.Decimal('10'), decimal.Decimal('0')),
        (decimal.Decimal('5'), decimal.Decimal('8.66'))
    ],
    step_size=decimal.Decimal('0.5')
)
```

Parameters:
- `vertices`: List of (x, y) points defining the polygon boundary (minimum 3 vertices)
- `step_size`: Distance between scan points
- `start_at_index`: Optional index to start from (default: 1)

## License

MIT License

## Author

Marvin Sass
