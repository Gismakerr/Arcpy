import arcpy
import Projection as Pro
import Raster as R
import 判断空间关系 as relation

# 输入栅格文件路径
raster_path = r'G:\FAB\N30\N030E110_Proj.tif'

# 获取栅格四个角的投影坐标
corners = R.get_raster_extent(raster_path)
print("Raster corners in projected coordinate system:")
for i, corner in enumerate(corners, 1):
    print(f"Corner {i}: {corner}")
    
a = relation.check_overlap(corners, corners)
print(a)

