"""
Example usage of CoordinatePaths library
Demonstrates RectangularPath, CircularPath, and PolygonPath
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from coordinate_paths import RectangularPath, CircularPath, PolygonPath
import decimal
import numpy as np
import matplotlib.pyplot as plt


def create_star_vertices(center_x: float, center_y: float, outer_radius: float, inner_radius: float, points: int = 5):
	"""
	Create vertices for a star polygon.

	:param center_x: X coordinate of star center
	:param center_y: Y coordinate of star center
	:param outer_radius: Radius to outer points
	:param inner_radius: Radius to inner points
	:param points: Number of points on the star (default 5)
	:return: List of (x, y) vertices
	"""
	vertices = []
	angle_step = 2 * np.pi / points

	for i in range(points):
		# Outer point
		angle_outer = i * angle_step - np.pi / 2  # Start from top
		x_outer = center_x + outer_radius * np.cos(angle_outer)
		y_outer = center_y + outer_radius * np.sin(angle_outer)
		vertices.append((decimal.Decimal(str(round(x_outer, 4))), decimal.Decimal(str(round(y_outer, 4)))))

		# Inner point
		angle_inner = (i + 0.5) * angle_step - np.pi / 2
		x_inner = center_x + inner_radius * np.cos(angle_inner)
		y_inner = center_y + inner_radius * np.sin(angle_inner)
		vertices.append((decimal.Decimal(str(round(x_inner, 4))), decimal.Decimal(str(round(y_inner, 4)))))

	return vertices


def main():
	# Create figure with 3 subplots
	fig, axes = plt.subplots(1, 3, figsize=(15, 5))

	# ========== 1. Rectangular Path ==========
	print("Creating Rectangular Path...")
	rect_path = RectangularPath(
		start_xy=(decimal.Decimal('0'), decimal.Decimal('0')),
		end_xy=(decimal.Decimal('10'), decimal.Decimal('8')),
		step_size_x=decimal.Decimal('0.5'),
		step_size_y=decimal.Decimal('0.5')
	)

	print(f"  Total points: {len(rect_path.coordinates)}")

	# Plot rectangular path
	coords = rect_path.coordinates
	x_vals = [float(c[0]) for c in coords]
	y_vals = [float(c[1]) for c in coords]

	axes[0].plot(x_vals, y_vals, 'o-', markersize=2, linewidth=0.5)
	axes[0].set_aspect('equal')
	axes[0].set_title(f'Rectangular Path\n({len(coords)} points)')
	axes[0].set_xlabel('X (mm)')
	axes[0].set_ylabel('Y (mm)')
	axes[0].grid(True, alpha=0.3)
	axes[0].invert_xaxis()

	# ========== 2. Circular Path ==========
	print("\nCreating Circular Path...")
	circular_path = CircularPath(
		center_xy=(decimal.Decimal('10'), decimal.Decimal('10')),
		radius=decimal.Decimal('5'),
		step_size=decimal.Decimal('0.5')
	)

	print(f"  Total points: {len(circular_path.coordinates)}")

	# Plot circular path
	coords = circular_path.coordinates
	x_vals = [float(c[0]) for c in coords]
	y_vals = [float(c[1]) for c in coords]

	axes[1].plot(x_vals, y_vals, 'o-', markersize=2, linewidth=0.5)
	axes[1].set_aspect('equal')
	axes[1].set_title(f'Circular Path\n({len(coords)} points)')
	axes[1].set_xlabel('X (mm)')
	axes[1].set_ylabel('Y (mm)')
	axes[1].grid(True, alpha=0.3)
	axes[1].invert_xaxis()

	# ========== 3. Five-Pointed Star Polygon Path ==========
	print("\nCreating Five-Pointed Star Path...")

	# Generate star vertices
	star_vertices = create_star_vertices(
		center_x=10.0,
		center_y=10.0,
		outer_radius=5.0,
		inner_radius=2.0,
		points=5
	)

	star_path = PolygonPath(
		vertices=star_vertices,
		step_size=decimal.Decimal('0.2')
	)

	print(f"  Total points: {len(star_path.coordinates)}")

	# Plot star path
	coords = star_path.coordinates
	x_vals = [float(c[0]) for c in coords]
	y_vals = [float(c[1]) for c in coords]

	# Plot the star outline
	star_x = [float(v[0]) for v in star_vertices] + [float(star_vertices[0][0])]
	star_y = [float(v[1]) for v in star_vertices] + [float(star_vertices[0][1])]
	axes[2].plot(star_x, star_y, 'k-', linewidth=2, label='Star boundary')

	# Plot the scan points
	axes[2].plot(x_vals, y_vals, 'o-', markersize=2, linewidth=0.5, label='Scan path')
	axes[2].set_aspect('equal')
	axes[2].set_title(f'Five-Pointed Star Path\n({len(coords)} points)')
	axes[2].set_xlabel('X (mm)')
	axes[2].set_ylabel('Y (mm)')
	axes[2].grid(True, alpha=0.3)
	axes[2].legend()
	axes[2].invert_xaxis()

	# ========== Display ==========
	plt.tight_layout()
	plt.savefig('coordinate_paths_examples.png', dpi=150, bbox_inches='tight')
	print("Plot saved to 'coordinate_paths_examples.png'")


if __name__ == "__main__":
	main()
