from coordinate_paths import base
import decimal
import numpy as np


class CircularPath(base.Path):
	"""
	Generates a spiral scanning path from center outward.

	The path starts at the center point and spirals outward in concentric circles,
	with points spaced approximately by step_size on each circle.
	"""

	def __init__(
		self,
		center_xy: tuple[decimal.Decimal, decimal.Decimal],
		radius: decimal.Decimal,
		step_size: decimal.Decimal,
		start_at_index: int = 1
	):
		"""
		Initialize circular path.

		:param center_xy: Center coordinates (x, y) in mm
		:type center_xy: tuple[decimal.Decimal, decimal.Decimal]
		:param radius: Maximum radius from center in mm
		:type radius: decimal.Decimal
		:param step_size: Approximate distance between points in mm
		:type step_size: decimal.Decimal
		:param start_at_index: Index to start scanning from (1-indexed)
		:type start_at_index: int
		"""
		self.__center_xy = center_xy
		self.__radius = radius
		self.__step_size = step_size
		self.__start_at_index = start_at_index
		super(CircularPath, self).__init__('Circular Path')
		self.__coordinates = None

	@property
	def coordinates(self) -> list[tuple[decimal.Decimal, decimal.Decimal]]:
		"""
		Generate spiral path coordinates.

		:return: List of (x, y) coordinate tuples
		:rtype: list[tuple[decimal.Decimal, decimal.Decimal]]
		"""
		if self.__coordinates is None:
			coordinates = []

			# Start with center point
			coordinates.append((self.__center_xy[0], self.__center_xy[1]))

			# Generate concentric circles from center outward
			# Number of circles needed
			num_circles = int(float(self.__radius) / float(self.__step_size))

			for circle_idx in range(1, num_circles + 1):
				current_radius = float(self.__step_size) * circle_idx

				# Calculate number of points on this circle
				# Circumference = 2 * pi * r
				# Number of points = circumference / step_size
				circumference = 2 * np.pi * current_radius
				num_points = max(6, int(circumference / float(self.__step_size)))

				# Generate points evenly spaced around the circle
				angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

				for angle in angles:
					x = float(self.__center_xy[0]) + current_radius * np.cos(angle)
					y = float(self.__center_xy[1]) + current_radius * np.sin(angle)

					# Convert back to Decimal
					coordinates.append((
						decimal.Decimal(str(round(x, 4))),
						decimal.Decimal(str(round(y, 4)))
					))

			# Apply start_at_index offset
			self.__coordinates = coordinates[self.__start_at_index - 1:]

		return self.__coordinates


if __name__ == "__main__":
	# Test the circular path
	path = CircularPath(
		center_xy=(decimal.Decimal('10'), decimal.Decimal('10')),
		radius=decimal.Decimal('5'),
		step_size=decimal.Decimal('0.5')
	)

	print(f"Total points: {len(path.coordinates)}")
	print(f"First 10 points:")
	for i, coord in enumerate(path.coordinates[:10]):
		print(f"  {i+1}: ({coord[0]}, {coord[1]})")

	# Visualize the path
	path.plot()
