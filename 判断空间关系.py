import arcpy

def check_overlap(raster_extent, target_extent):
    """
    判断栅格与目标范围是否重叠
    :param raster_extent: 栅格的Extent对象
    :param target_extent: 目标范围的四元组(min_lat, min_lon, max_lat, max_lon)
    :return: 如果重叠返回True，否则返回False
    """
    # 提取栅格的经纬度范围
    raster_min_lat = raster_extent[0]
    raster_min_lon = raster_extent[1]
    
    raster_max_lat = raster_extent[2]
    raster_max_lon = raster_extent[3]

    # 提取目标范围的经纬度
    min_lat, min_lon, max_lat, max_lon = target_extent

    # 判断目标范围是否与栅格范围有重叠
    if (raster_min_lat <= max_lat and raster_max_lat >= min_lat and
        raster_min_lon <= max_lon and raster_max_lon >= min_lon):
        return True  # 目标范围完全包含栅格范围
    else:
        return False  # 目标范围未完全包含栅格范围