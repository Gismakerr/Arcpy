import arcpy

def get_feature_extents(feature_class):
    """
    获取要素类中所有要素的矩形范围（extent）。
    :param feature_class: 输入的要素类路径
    :return: 包含每个要素的extent的列表，每个extent是一个字典
    """
    # 创建空列表存储每个要素的extent
    extents = []

    # 使用搜索游标遍历要素
    with arcpy.da.SearchCursor(feature_class, ["SHAPE@"]) as cursor:
        for row in cursor:
            # 获取要素的几何对象
            geometry = row[0]

            # 获取要素的extent
            extent = geometry.extent
            extents.append((
                 extent.YMin,
                 extent.XMin,
                 extent.YMax,
                 extent.XMax
            ))
    return extents

def calculate_lower_left_coordinates(fishnet_fc, x_field="Min_X", y_field="Min_Y"):
    """
    计算渔网要素类中所有要素的左下角坐标（保留小数点后一位），并存储到指定字段中。

    参数：
        fishnet_fc (str): 渔网要素类的路径或名称。
        x_field (str): 存储左下角 X 坐标的字段名称，默认值为 "LowerLeft_X"。
        y_field (str): 存储左下角 Y 坐标的字段名称，默认值为 "LowerLeft_Y"。
    """
    # 检查要素类是否存在
    if not arcpy.Exists(fishnet_fc):
        raise FileNotFoundError(f"要素类 {fishnet_fc} 不存在！")
    
    # 检查并添加字段
    if not arcpy.ListFields(fishnet_fc, x_field):
        arcpy.AddField_management(fishnet_fc, x_field, "DOUBLE")
        print(f"字段 {x_field} 已添加。")
    if not arcpy.ListFields(fishnet_fc, y_field):
        arcpy.AddField_management(fishnet_fc, y_field, "DOUBLE")
        print(f"字段 {y_field} 已添加。")
    
    # 遍历要素类，计算并更新左下角坐标
    with arcpy.da.UpdateCursor(fishnet_fc, ["SHAPE@", x_field, y_field]) as cursor:
        for row in cursor:
            shape = row[0]  # 获取几何
            if shape:
                extent = shape.extent  # 获取几何边界
                lower_left_x = round(extent.XMin, 1)  # 保留小数点后一位
                lower_left_y = round(extent.YMin, 1)  # 保留小数点后一位
                
                # 更新字段值
                row[1] = lower_left_x
                row[2] = lower_left_y
                cursor.updateRow(row)
                print(f"更新要素左下角坐标: ({lower_left_x}, {lower_left_y})")
    
    print("所有要素的左下角坐标计算完成！")

def generate_location_index(fishnet_fc, x_field="Min_X", y_field="Min_Y", index_field="Location"):
    """
    根据渔网要素类中的左下角坐标生成位置索引，并存储到指定字段中。
    格式：N0604W0758，表示北纬60.4度、西经75.8度。

    参数：
        fishnet_fc (str): 渔网要素类的路径或名称。
        x_field (str): 存储左下角 X 坐标的字段名称，默认值为 "Min_X"。
        y_field (str): 存储左下角 Y 坐标的字段名称，默认值为 "Min_Y"。
        index_field (str): 用于存储生成的位置索引的字段名称，默认值为 "Location_Index"。
    """
    # 检查要素类是否存在
    if not arcpy.Exists(fishnet_fc):
        raise FileNotFoundError(f"要素类 {fishnet_fc} 不存在！")

    # 检查并添加位置索引字段
    if not arcpy.ListFields(fishnet_fc, index_field):
        arcpy.AddField_management(fishnet_fc, index_field, "TEXT", field_length=40)
        print(f"字段 {index_field} 已添加。")
    
    # 遍历要素类，根据坐标生成位置索引
    with arcpy.da.UpdateCursor(fishnet_fc, [x_field, y_field, index_field]) as cursor:
        for row in cursor:
            min_x = row[0]
            min_y = row[1]
            
            if min_x is not None and min_y is not None:
                # 解析纬度
                lat_prefix = "N" if min_y >= 0 else "S"
                lat_abs = abs(min_y)
                lat_index = f"{lat_prefix}{int(lat_abs):03d}{int(round((lat_abs - int(lat_abs)) * 10)):01d}"
                
                # 解析经度
                lon_prefix = "E" if min_x >= 0 else "W"
                lon_abs = abs(min_x)
                lon_index = f"{lon_prefix}{int(lon_abs):03d}{int(round((lon_abs - int(lon_abs)) * 10)):01d}"
                
                # 生成位置索引
                location_index = f"{lat_index}{lon_index}"
                row[2] = location_index  # 更新索引字段
                cursor.updateRow(row)
                print(f"生成位置索引: {location_index}")
    
    print("位置索引生成完成！")