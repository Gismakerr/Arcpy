import arcpy 

def project_extent(input_extent, input_spatial_ref, output_spatial_ref):
    """
    将地理坐标系的 extent 投影到目标投影坐标系，并处理 180° 经线附近点的问题。
    
    :param input_extent: 输入的 extent 元组 (min_lat, min_lon, max_lat, max_lon)
    :param input_spatial_ref: 输入坐标系（地理坐标系），arcpy.SpatialReference 对象
    :param output_spatial_ref: 输出坐标系（投影坐标系），arcpy.SpatialReference 对象
    :return: 投影后的 extent 元组 (min_x, min_y, max_x, max_y)
    """
    min_lat, min_lon, max_lat, max_lon = input_extent

    # 处理经度超出范围问题
    points = [
        arcpy.Point(min_lon if min_lon <= 180 else min_lon - 360, min_lat),  # 左下角
        arcpy.Point(max_lon if max_lon <= 180 else max_lon - 360, min_lat),  # 右下角
        arcpy.Point(max_lon if max_lon <= 180 else max_lon - 360, max_lat),  # 右上角
        arcpy.Point(min_lon if min_lon <= 180 else min_lon - 360, max_lat),  # 左上角
    ]

    # 投影四个角点
    projected_points = []
    for pt in points:
        point_geometry = arcpy.PointGeometry(pt, input_spatial_ref)
        if not point_geometry:
            raise ValueError(f"无效点：{pt}")
        
        projected_geometry = point_geometry.projectAs(output_spatial_ref)
        if projected_geometry:
            projected_points.append(projected_geometry.firstPoint)
        else:
            raise ValueError(f"投影失败：{pt}")

    # 确保投影后的点不为空
    if not projected_points:
        raise ValueError("投影点为空，无法计算投影范围！")

    # 计算投影后范围
    min_x = min(pt.X for pt in projected_points if pt)
    min_y = min(pt.Y for pt in projected_points if pt)
    max_x = max(pt.X for pt in projected_points if pt)
    max_y = max(pt.Y for pt in projected_points if pt)

    return min_x, min_y, max_x, max_y

