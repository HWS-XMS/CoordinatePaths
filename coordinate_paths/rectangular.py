from coordinate_paths import base
import decimal
import tqdm
import numpy as np
import time
import random

class RectangularPath(base.Path):

	def __init__(
		self,
		start_xy 			: tuple[decimal.Decimal, decimal.Decimal],
		end_xy 				: tuple[decimal.Decimal, decimal.Decimal],
		step_size_x 		: decimal.Decimal,
		step_size_y 		: decimal.Decimal,
		start_at_index		: int 	= 1,
		random 				: bool 	= False,
		percent 			: int 	= 100
	):
		self.__start_xy 		= start_xy
		self.__end_xy 			= end_xy
		self.__step_size_x 		= step_size_x
		self.__step_size_y 		= step_size_y
		self.__start_at_index 	= start_at_index
		super(RectangularPath, self).__init__('Rectangular Path')
		self.__coordinates 		= None
		self.__random 			= random

	@property
	def coordinates(self) -> list[tuple[decimal.Decimal, decimal.Decimal]]:
		if self.__coordinates is None:
			coordinates 	= []
			x_coords 		= np.arange(min(self.__start_xy[0], self.__end_xy[0]), max(self.__start_xy[0], self.__end_xy[0]), self.__step_size_x)
			y_coords 		= np.arange(min(self.__start_xy[1], self.__end_xy[1]), max(self.__start_xy[1], self.__end_xy[1]), self.__step_size_x)

			y_forward 		= True
			for x_coord in x_coords:
				for y_coord in y_coords if y_forward else y_coords[::-1]:
					coordinates.append( (x_coord, y_coord))
				y_forward = not y_forward

			self.__coordinates = coordinates[self.__start_at_index-1:]
		if self.__random:
			random.shuffle(self.__coordinates)
		return self.__coordinates

if __name__ == "__main__":
	path = RectangularPath(
		start_xy=(decimal.Decimal('0'), decimal.Decimal('0')),
		end_xy=(decimal.Decimal('4'), decimal.Decimal('3')),
		step_size_x=decimal.Decimal('0.1'),
		step_size_y=decimal.Decimal('0.1'),
		start_at_index	= 10
	)
	path.plot()