import arcpy
import os
import Projection as Pro
import Raster as R
import 判断空间关系 as relation
import Read as read
import Feature as F
import shutil
# # 输入栅格文件路径
# raster_path = r'G:\FAB\N30\N030E110_Proj.tif'
# shp_path = r"E:\毕业论文\研究生毕业论文\基本数据\山体范围\高山区1度渔网.shp"

# # 获取栅格四个角的投影坐标
# corners = R.get_raster_extent(raster_path)
# print("Raster corners in projected coordinate system:")
# for i, corner in enumerate(corners, 1):
#     print(f"Corner {i}: {corner}")
    
# Fextent = F.get_feature_extents(shp_path)
    
# for extent in Fextent:
    
#     input_spatial_ref = arcpy.SpatialReference(54017) 
#     output_spatial_ref = arcpy.SpatialReference(4326)
#     corners = Pro.project_extent(corners, input_spatial_ref, output_spatial_ref)
    
#     a = relation.check_overlap(corners, extent)
#     print(a)
    

# fishnet_fc = r"E:\毕业论文\研究生毕业论文\基本数据\山体范围\01度高山区渔网.shp"  # 替换为渔网要素类名称
# F.calculate_lower_left_coordinates(fishnet_fc)

# fishnet_fc = r"E:\毕业论文\研究生毕业论文\基本数据\山体范围\01度高山区渔网.shp"  # 替换为渔网要素类名称
# F.generate_location_index(fishnet_fc)
feature_class = r"E:\毕业论文\研究生毕业论文\基本数据\山体范围\01度高山区渔网.shp"
folder = r"D:\一度FABDEM\Clip"
new_folder = r"D:\一度FABDEM\Clip1"
suffix = ".tif"
with arcpy.da.SearchCursor(feature_class, ["location","SHAPE@"]) as cursor:
    for row in cursor:
        Feature_extent = []
        geometry = row[1]
        # 获取要素的extent
        extent = geometry.extent
        Feature_extent.append((
                extent.YMin,
                extent.XMin,
                extent.YMax,
                extent.XMax
        ))
        # 获取要素的几何对象
        Loc = row[0]
        RasterFolder = folder + "\\" + Loc[:4] + Loc[5:9]
        NewRasterFolder = new_folder + "\\" + Loc
        if not os.path.exists(NewRasterFolder):
            os.makedirs(NewRasterFolder)
        try:
            Rasters = read.list_files_by_suffix(RasterFolder,suffix)
            for raster in Rasters:
                raster_extent = R.get_raster_extent(raster)    
                if relation.check_overlap(raster_extent,Feature_extent[0]):
                    shutil.move(raster, NewRasterFolder)
                    print(f'file:{raster}已移动！')
        except:
            print(f"文件夹{RasterFolder}")
            
    



     