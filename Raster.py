import arcpy

# 获取栅格的四个角坐标
def get_raster_extent(raster_file):
    """
    获取栅格文件的经纬度四元组（min_lat, min_lon, max_lat, max_lon）
    :param raster_file: 栅格文件路径
    :return: 四元组(min_lat, min_lon, max_lat, max_lon)
    """
    # 获取栅格的Extent
    raster_extent = arcpy.Describe(raster_file).extent

    # 提取栅格的四个角的坐标
    min_y = raster_extent.YMin
    max_y = raster_extent.YMax
    min_x = raster_extent.XMin
    max_x = raster_extent.XMax

    return (min_y, min_x, max_y, max_x)