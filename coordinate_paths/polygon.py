from coordinate_paths import base
from coordinate_paths.base import PrimaryAxis, _inclusive_walk, _serpentine_raster
import decimal


class PolygonPath(base.Path):
	"""
	Generates a raster scanning path within a polygonal area.

	The path scans the bounding box of the polygon in a snake-like pattern,
	keeping only points that fall inside the polygon boundary.
	"""

	def __init__(
		self,
		vertices: list[tuple[decimal.Decimal, decimal.Decimal]],
		step_size: decimal.Decimal,
		start_at_index: int = 1,
		primary_axis: PrimaryAxis = PrimaryAxis.Y,
	):
		"""
		:param vertices: List of (x, y) vertices defining the polygon boundary.
		:param step_size: Distance between scan points (must be > 0).
		:param start_at_index: 1-indexed offset to start from (drops earlier points).
		:param primary_axis: ``PrimaryAxis.X`` row-major, ``PrimaryAxis.Y``
		                     column-major (default).
		:raises ValueError: If fewer than 3 vertices are provided.
		"""
		if len(vertices) < 3:
			raise ValueError("Polygon must have at least 3 vertices")

		self.__vertices = vertices
		self.__step_size = step_size
		self.__start_at_index = start_at_index
		super().__init__('Polygon Path', primary_axis=primary_axis)
		self.__coordinates = None

	def __point_in_polygon(self, x: float, y: float) -> bool:
		"""Ray-casting point-in-polygon test."""
		n = len(self.__vertices)
		inside = False

		p1x, p1y = float(self.__vertices[0][0]), float(self.__vertices[0][1])
		for i in range(1, n + 1):
			p2x, p2y = float(self.__vertices[i % n][0]), float(self.__vertices[i % n][1])

			if y > min(p1y, p2y):
				if y <= max(p1y, p2y):
					if x <= max(p1x, p2x):
						if p1y != p2y:
							xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
						if p1x == p2x or x <= xinters:
							inside = not inside
			p1x, p1y = p2x, p2y

		return inside

	@property
	def coordinates(self) -> list[tuple[decimal.Decimal, decimal.Decimal]]:
		if self.__coordinates is None:
			# Bounding box (in float for inside-test consistency).
			x_floats = [float(v[0]) for v in self.__vertices]
			y_floats = [float(v[1]) for v in self.__vertices]
			min_x, max_x = min(x_floats), max(x_floats)
			min_y, max_y = min(y_floats), max(y_floats)
			step = float(self.__step_size)

			xs = _inclusive_walk(min_x, max_x, step)
			ys = _inclusive_walk(min_y, max_y, step)

			raster = _serpentine_raster(xs, ys, self._primary_axis)
			coords = [
				(decimal.Decimal(str(round(x, 4))),
				 decimal.Decimal(str(round(y, 4))))
				for x, y in raster
				if self.__point_in_polygon(x, y)
			]
			self.__coordinates = coords[self.__start_at_index - 1:]
		return self.__coordinates


if __name__ == "__main__":
	path = PolygonPath(
		vertices=[
			(decimal.Decimal('0'), decimal.Decimal('0')),
			(decimal.Decimal('10'), decimal.Decimal('0')),
			(decimal.Decimal('5'), decimal.Decimal('8.66')),
		],
		step_size=decimal.Decimal('0.5'),
	)
	print(f"Total points: {len(path.coordinates)}")
	for i, coord in enumerate(path.coordinates[:10]):
		print(f"  {i+1}: ({coord[0]}, {coord[1]})")
	path.plot()
