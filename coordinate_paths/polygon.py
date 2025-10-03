from coordinate_paths import base
import decimal
import numpy as np


class PolygonPath(base.Path):
	"""
	Generates a raster scanning path within a polygonal area.

	The path scans the bounding box of the polygon in a snake-like pattern,
	including only points that fall inside the polygon boundary.
	"""

	def __init__(
		self,
		vertices: list[tuple[decimal.Decimal, decimal.Decimal]],
		step_size: decimal.Decimal,
		start_at_index: int = 1
	):
		"""
		Initialize polygon path.

		:param vertices: List of (x, y) vertices defining the polygon boundary
		:type vertices: list[tuple[decimal.Decimal, decimal.Decimal]]
		:param step_size: Distance between scan points in mm
		:type step_size: decimal.Decimal
		:param start_at_index: Index to start scanning from (1-indexed)
		:type start_at_index: int
		:raises ValueError: If fewer than 3 vertices are provided
		"""
		if len(vertices) < 3:
			raise ValueError("Polygon must have at least 3 vertices")

		self.__vertices = vertices
		self.__step_size = step_size
		self.__start_at_index = start_at_index
		super(PolygonPath, self).__init__('Polygon Path')
		self.__coordinates = None

	def __point_in_polygon(self, x: float, y: float) -> bool:
		"""
		Check if a point is inside the polygon using ray casting algorithm.

		:param x: X coordinate of point
		:type x: float
		:param y: Y coordinate of point
		:type y: float
		:return: True if point is inside polygon, False otherwise
		:rtype: bool
		"""
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
		"""
		Generate raster scan coordinates within polygon boundary.

		:return: List of (x, y) coordinate tuples
		:rtype: list[tuple[decimal.Decimal, decimal.Decimal]]
		"""
		if self.__coordinates is None:
			coordinates = []

			# Find bounding box of polygon
			x_coords = [float(v[0]) for v in self.__vertices]
			y_coords = [float(v[1]) for v in self.__vertices]

			min_x = min(x_coords)
			max_x = max(x_coords)
			min_y = min(y_coords)
			max_y = max(y_coords)

			# Generate raster scan pattern
			x_range = np.arange(min_x, max_x + float(self.__step_size), float(self.__step_size))
			y_range = np.arange(min_y, max_y + float(self.__step_size), float(self.__step_size))

			# Snake-like pattern
			y_forward = True
			for x in x_range:
				y_list = y_range if y_forward else y_range[::-1]
				for y in y_list:
					# Only include points inside the polygon
					if self.__point_in_polygon(x, y):
						coordinates.append((
							decimal.Decimal(str(round(x, 4))),
							decimal.Decimal(str(round(y, 4)))
						))
				y_forward = not y_forward

			# Apply start_at_index offset
			self.__coordinates = coordinates[self.__start_at_index - 1:]

		return self.__coordinates


if __name__ == "__main__":
	# Test the polygon path with a triangle
	import decimal

	path = PolygonPath(
		vertices=[
			(decimal.Decimal('0'), decimal.Decimal('0')),
			(decimal.Decimal('10'), decimal.Decimal('0')),
			(decimal.Decimal('5'), decimal.Decimal('8.66'))  # Equilateral triangle
		],
		step_size=decimal.Decimal('0.5')
	)

	print(f"Total points: {len(path.coordinates)}")
	print(f"First 10 points:")
	for i, coord in enumerate(path.coordinates[:10]):
		print(f"  {i+1}: ({coord[0]}, {coord[1]})")

	# Visualize the path
	path.plot()
