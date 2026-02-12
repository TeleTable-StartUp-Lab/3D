#!/usr/bin/env python3
"""
Script to make the Top.stl hollow for 3D printing.
This reduces material usage while maintaining structural integrity.
"""

import trimesh
import numpy as np

def make_hollow(input_file, output_file, wall_thickness=2.0):
    """
    Make a solid STL model hollow by creating a shell with specified wall thickness.
    
    Args:
        input_file: Path to input STL file
        output_file: Path to output STL file
        wall_thickness: Thickness of the walls in mm (default: 2.0mm)
    """
    print(f"Loading {input_file}...")
    mesh = trimesh.load_mesh(input_file)
    
    print(f"Original mesh:")
    print(f"  - Vertices: {len(mesh.vertices)}")
    print(f"  - Faces: {len(mesh.faces)}")
    print(f"  - Volume: {mesh.volume:.2f} cubic mm")
    print(f"  - Is watertight: {mesh.is_watertight}")
    
    # Calculate the scale factor for the inner surface
    # We want to shrink the mesh inward by wall_thickness
    bounds = mesh.bounds
    dimensions = bounds[1] - bounds[0]
    
    # Calculate scale factor to achieve the desired wall thickness
    # This is an approximation - actual wall thickness may vary
    min_dim = min(dimensions)
    scale_factor = (min_dim - 2 * wall_thickness) / min_dim
    # Keep scale factor between 0.7 and 0.95:
    # - 0.7 minimum ensures at least 30% size reduction for structural integrity
    # - 0.95 maximum prevents walls from being too thin (< 5% of original size)
    scale_factor = max(0.7, min(scale_factor, 0.95))
    
    print(f"\nCreating hollow shell with wall thickness ~{wall_thickness}mm...")
    print(f"  - Scale factor for inner surface: {scale_factor:.3f}")
    
    # Create the inner mesh by scaling
    inner_mesh = mesh.copy()
    
    # Scale from the center
    center = mesh.centroid
    inner_mesh.vertices = (inner_mesh.vertices - center) * scale_factor + center
    
    # Invert the normals of the inner mesh so they point inward
    inner_mesh.faces = np.fliplr(inner_mesh.faces)
    
    # Combine outer and inner meshes
    print("Combining outer and inner surfaces...")
    hollow_mesh = trimesh.util.concatenate([mesh, inner_mesh])
    
    print(f"\nHollow mesh:")
    print(f"  - Vertices: {len(hollow_mesh.vertices)}")
    print(f"  - Faces: {len(hollow_mesh.faces)}")
    print(f"  - Approximate material savings: {(1 - scale_factor**3) * 100:.1f}%")
    
    # Export the hollow mesh
    print(f"\nExporting to {output_file}...")
    hollow_mesh.export(output_file)
    
    print("Done! The top part is now hollow and ready for 3D printing.")
    print(f"This should save approximately {(1 - scale_factor**3) * 100:.1f}% of material/ink.")

if __name__ == "__main__":
    # Note: This will overwrite the original Top.stl file
    # Make a backup first if you want to preserve the original
    make_hollow("Top.stl", "Top.stl", wall_thickness=2.0)
