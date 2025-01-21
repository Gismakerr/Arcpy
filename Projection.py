import arcpy 

# 将点从当前投影坐标系转换为地理坐标系（WGS84）
def project_point_to_geographic(points, input_spatial_ref, target_spatial_ref):
    """
    将给定的坐标点从当前坐标系转换为地理坐标系（如 WGS84）。
    :param points: 待转换的点列表 [(x1, y1), (x2, y2), ...]
    :param input_spatial_ref: 输入坐标系
    :param target_spatial_ref: 目标坐标系（例如 WGS84）
    :return: 返回转换后的点列表 [(longitude1, latitude1), (longitude2, latitude2), ...]
    """
    projected_points = []
    
    for point in points:
        # 创建点对象
        point_geom = arcpy.PointGeometry(arcpy.Point(point[0], point[1]), input_spatial_ref)
        
        # 投影转换
        projected_point = point_geom.projectAs(target_spatial_ref)
        
        # 获取转换后的坐标
        projected_points.append((projected_point.firstPoint.X, projected_point.firstPoint.Y))
    
    return projected_points


  

