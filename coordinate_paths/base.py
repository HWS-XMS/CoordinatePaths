import decimal
import enum

from matplotlib import pyplot as plt


class PrimaryAxis(enum.Enum):
	"""Inner-loop axis for raster scans.

	X — row-major:    outer loop over y, inner serpentine over x.
	Y — column-major: outer loop over x, inner serpentine over y.
	"""
	X = 'x'
	Y = 'y'


def _inclusive_walk(start, end, step):
	"""Generate values from ``start`` to ``end`` **inclusive of both endpoints**,
	step magnitude ``|step|``, direction taken from ``sign(end - start)``.

	The endpoint is always present exactly, even if ``step`` does not divide
	the range evenly (the last increment may be shorter than ``step``).

	Works for any comparable numeric type that supports ``+``, ``-`` and
	ordering (``int``, ``float``, ``decimal.Decimal``).
	"""
	if step <= 0:
		raise ValueError("step must be > 0")
	if start == end:
		return [start]
	out = []
	v = start
	if end > start:
		while v < end:
			out.append(v)
			v = v + step
	else:
		while v > end:
			out.append(v)
			v = v - step
	if out[-1] != end:
		out.append(end)
	return out


def _serpentine_raster(xs, ys, primary_axis: PrimaryAxis):
	"""Serpentine raster over the cartesian product of ``xs`` and ``ys``.

	primary_axis == X — row-major:    outer y, inner x (x serpentines).
	primary_axis == Y — column-major: outer x, inner y (y serpentines).
	"""
	out = []
	if primary_axis == PrimaryAxis.X:
		forward = True
		for y in ys:
			inner = xs if forward else list(reversed(xs))
			for x in inner:
				out.append((x, y))
			forward = not forward
	else:
		forward = True
		for x in xs:
			inner = ys if forward else list(reversed(ys))
			for y in inner:
				out.append((x, y))
			forward = not forward
	return out


class Path(object):

	def __init__(self, description: str, primary_axis: PrimaryAxis = PrimaryAxis.Y):
		"""
		:param primary_axis: ``PrimaryAxis.X`` for row-major,
		                     ``PrimaryAxis.Y`` for column-major (default).
		"""
		if not isinstance(primary_axis, PrimaryAxis):
			raise TypeError(
				f"primary_axis must be a PrimaryAxis, got {type(primary_axis).__name__}"
			)
		self.__description 		= description
		self.__context 			= decimal.getcontext()
		self.__context.prec 	= 4
		self._primary_axis 		= primary_axis

	@property
	def coordinates(self) -> list[tuple[decimal.Decimal, decimal.Decimal]]:
		pass

	def plot(self) -> None:
		coordinates = []
		for coord in self.coordinates:
			coordinates.append(coord)
		connectivity 	= {}
		for i in range(0, len(coordinates) - 1):
			connectivity[i] = i + 1
		x, y = zip(*coordinates)
		plt.plot(x, y, 'o')
		for k, v in connectivity.items():
			x, y = zip(coordinates[k], coordinates[v])
			plt.plot(x, y, 'r')
		plt.axis('equal')
		plt.gca().invert_xaxis()
		plt.show()

	def __iter__(self):
		self.__element_id = 0
		return self

	def __next__(self):
		if self.__element_id < len(self.coordinates):
			coordinate 			= self.coordinates[self.__element_id]
			self.__element_id 	= self.__element_id + 1
			return coordinate
		else:
			raise StopIteration

	def __len__(self):
		return len(self.coordinates)
