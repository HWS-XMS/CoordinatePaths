"""
Example usage of CoordinatePaths library.
Demonstrates RectangularPath, CircularPath, and PolygonPath at both
PrimaryAxis.Y (column-major, top row) and PrimaryAxis.X (row-major,
bottom row).
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from coordinate_paths import RectangularPath, CircularPath, PolygonPath, PrimaryAxis
import decimal
import numpy as np
import matplotlib.pyplot as plt


def star_vertices(center_x: float, center_y: float, outer_r: float,
                  inner_r: float, points: int = 5):
	"""Return Decimal vertices for a `points`-pointed star centred at
	(center_x, center_y)."""
	verts = []
	step = 2 * np.pi / points
	for i in range(points):
		a_outer = i * step - np.pi / 2
		verts.append((
			decimal.Decimal(str(round(center_x + outer_r * np.cos(a_outer), 4))),
			decimal.Decimal(str(round(center_y + outer_r * np.sin(a_outer), 4))),
		))
		a_inner = (i + 0.5) * step - np.pi / 2
		verts.append((
			decimal.Decimal(str(round(center_x + inner_r * np.cos(a_inner), 4))),
			decimal.Decimal(str(round(center_y + inner_r * np.sin(a_inner), 4))),
		))
	return verts


STAR = star_vertices(center_x=10.0, center_y=10.0, outer_r=5.0, inner_r=2.0)


def make_paths(primary_axis: PrimaryAxis):
	"""Construct the three example paths for a given primary axis.
	CircularPath has no primary_axis (spiral); we still return it so the
	figure layout is uniform."""
	rect = RectangularPath(
		start_xy=(decimal.Decimal('0'), decimal.Decimal('0')),
		end_xy=(decimal.Decimal('10'), decimal.Decimal('8')),
		step_size_x=decimal.Decimal('0.5'),
		step_size_y=decimal.Decimal('0.5'),
		primary_axis=primary_axis,
	)
	circ = CircularPath(
		center_xy=(decimal.Decimal('10'), decimal.Decimal('10')),
		radius=decimal.Decimal('5'),
		step_size=decimal.Decimal('0.5'),
	)
	poly = PolygonPath(
		vertices=STAR,
		step_size=decimal.Decimal('0.2'),
		primary_axis=primary_axis,
	)
	return rect, circ, poly


def draw(ax, coords, title, boundary=None):
	xs = [float(c[0]) for c in coords]
	ys = [float(c[1]) for c in coords]
	if boundary is not None:
		bx = [float(v[0]) for v in boundary] + [float(boundary[0][0])]
		by = [float(v[1]) for v in boundary] + [float(boundary[0][1])]
		ax.plot(bx, by, 'k-', linewidth=2, label='boundary')
	ax.plot(xs, ys, 'o-', markersize=2, linewidth=0.5, label='scan')
	ax.set_aspect('equal')
	ax.set_title(f'{title}\n({len(coords)} pts)')
	ax.set_xlabel('X (mm)')
	ax.set_ylabel('Y (mm)')
	ax.grid(True, alpha=0.3)
	ax.invert_xaxis()


def main():
	fig, axes = plt.subplots(2, 3, figsize=(15, 10))
	for row, axis in enumerate((PrimaryAxis.Y, PrimaryAxis.X)):
		rect, circ, poly = make_paths(axis)
		label = f'{axis.name}-major'
		print(f'{label}: rect={len(rect)}  circ={len(circ)}  poly={len(poly)}')
		draw(axes[row, 0], rect.coordinates, f'Rectangular ({label})')
		draw(axes[row, 1], circ.coordinates, f'Circular (spiral, n/a)')
		draw(axes[row, 2], poly.coordinates, f'Star polygon ({label})', boundary=STAR)
	plt.tight_layout()
	plt.savefig('coordinate_paths_examples.png', dpi=150, bbox_inches='tight')
	print("Plot saved to 'coordinate_paths_examples.png'")


if __name__ == "__main__":
	main()
