import decimal
from matplotlib import pyplot as plt

class Path(object):

	def __init__(self, description: str):
		self.__description 		= description
		self.__context 			= decimal.getcontext()
		self.__context.prec 	= 4

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