# 3D Model #
*This repo includes the 3D models of the car chassis in STL format.*

View the model directly in GitHub or visit the link **https://www.viewstl.com/**.

## Files ##
- **Base.stl** - The base/bottom part of the car chassis
- **Top.stl** - The top part of the car chassis (hollow with ~2mm wall thickness for efficient 3D printing)

## 3D Printing Notes ##
The Top.stl model has been optimized for 3D printing by making it hollow with approximately 2mm wall thickness. This saves approximately **25.7% of material/ink** compared to a solid print while maintaining structural integrity.

To regenerate the hollow top part with a different wall thickness, use:
```bash
python3 make_hollow.py
```

You can modify the `wall_thickness` parameter in the script to adjust the wall thickness as needed.
