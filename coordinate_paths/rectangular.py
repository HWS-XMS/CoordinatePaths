from coordinate_paths import base
from coordinate_paths.base import PrimaryAxis, _inclusive_walk, _serpentine_raster
import decimal
import random


class RectangularPath(base.Path):

	def __init__(
		self,
		start_xy 			: tuple[decimal.Decimal, decimal.Decimal],
		end_xy 				: tuple[decimal.Decimal, decimal.Decimal],
		step_size_x 		: decimal.Decimal,
		step_size_y 		: decimal.Decimal,
		start_at_index		: int 			= 1,
		random 				: bool 			= False,
		primary_axis		: PrimaryAxis	= PrimaryAxis.Y,
	):
		"""
		:param start_xy: First corner of the scan. The order start→end
		                 defines the scan direction; coordinates are NOT
		                 sorted internally.
		:param end_xy:   Opposite corner. **Both** start_xy and end_xy are
		                 included in the scan, even when the step does not
		                 divide the range evenly.
		:param step_size_x / step_size_y: Step magnitude, must be > 0.
		:param primary_axis: ``PrimaryAxis.X`` row-major, ``PrimaryAxis.Y``
		                     column-major (default).
		"""
		self.__start_xy 		= start_xy
		self.__end_xy 			= end_xy
		self.__step_size_x 		= step_size_x
		self.__step_size_y 		= step_size_y
		self.__start_at_index 	= start_at_index
		self.__random 			= random
		super().__init__('Rectangular Path', primary_axis=primary_axis)
		self.__coordinates 		= None

	@property
	def coordinates(self) -> list[tuple[decimal.Decimal, decimal.Decimal]]:
		if self.__coordinates is None:
			xs = _inclusive_walk(self.__start_xy[0], self.__end_xy[0], self.__step_size_x)
			ys = _inclusive_walk(self.__start_xy[1], self.__end_xy[1], self.__step_size_y)
			coords = _serpentine_raster(xs, ys, self._primary_axis)
			self.__coordinates = coords[self.__start_at_index - 1:]
		if self.__random:
			random.shuffle(self.__coordinates)
		return self.__coordinates


if __name__ == "__main__":
	path = RectangularPath(
		start_xy=(decimal.Decimal('0'), decimal.Decimal('0')),
		end_xy=(decimal.Decimal('4'), decimal.Decimal('3')),
		step_size_x=decimal.Decimal('0.1'),
		step_size_y=decimal.Decimal('0.1'),
		start_at_index=10,
	)
	path.plot()
