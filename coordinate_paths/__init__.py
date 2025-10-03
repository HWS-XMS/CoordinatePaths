"""
CoordinatePaths - Coordinate path generation for automated scanning systems

This package provides various path generation patterns for XYZ positioning systems.
"""

from coordinate_paths.base import Path
from coordinate_paths.rectangular import RectangularPath
from coordinate_paths.circular import CircularPath
from coordinate_paths.polygon import PolygonPath

__version__ = "1.0.0"
__all__ = ["Path", "RectangularPath", "CircularPath", "PolygonPath"]
