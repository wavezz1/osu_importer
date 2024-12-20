import bpy, mathutils


# initialize circle_sim_group node group
def circle_sim_group_node_group():
    circle_sim_group = bpy.data.node_groups.new(type='GeometryNodeTree', name="Circle Sim Group")

    circle_sim_group.color_tag = 'NONE'
    circle_sim_group.description = ""

    # circle_sim_group interface
    # Socket Circles
    circles_socket = circle_sim_group.interface.new_socket(name="Circles", in_out='OUTPUT',
                                                           socket_type='NodeSocketGeometry')
    circles_socket.attribute_domain = 'POINT'

    # Socket Circle Mesh
    circle_mesh_socket = circle_sim_group.interface.new_socket(name="Circle Mesh", in_out='OUTPUT',
                                                               socket_type='NodeSocketGeometry')
    circle_mesh_socket.attribute_domain = 'POINT'

    # Socket Geometry
    geometry_socket = circle_sim_group.interface.new_socket(name="Geometry", in_out='INPUT',
                                                            socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    # Socket Circle Material
    circle_material_socket = circle_sim_group.interface.new_socket(name="Circle Material", in_out='INPUT',
                                                                   socket_type='NodeSocketMaterial')
    circle_material_socket.attribute_domain = 'POINT'

    # Socket Y Offset
    y_offset_socket = circle_sim_group.interface.new_socket(name="Y Offset", in_out='INPUT',
                                                            socket_type='NodeSocketFloat')
    y_offset_socket.default_value = 0.0
    y_offset_socket.min_value = -10000.0
    y_offset_socket.max_value = 10000.0
    y_offset_socket.subtype = 'NONE'
    y_offset_socket.attribute_domain = 'POINT'

    # Socket Instance
    instance_socket = circle_sim_group.interface.new_socket(name="Instance", in_out='INPUT',
                                                            socket_type='NodeSocketGeometry')
    instance_socket.attribute_domain = 'POINT'

    # initialize circle_sim_group nodes
    # node Group Output
    group_output = circle_sim_group.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # node Group Input
    group_input = circle_sim_group.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True

    # node Realize Instances
    realize_instances = circle_sim_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # node Delete Geometry
    delete_geometry = circle_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    # node Named Attribute
    named_attribute = circle_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT'
    # Name
    named_attribute.inputs[0].default_value = "show"

    # node Boolean Math
    boolean_math = circle_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.hide = True
    boolean_math.operation = 'NOT'

    # node Delete Geometry.001
    delete_geometry_001 = circle_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.domain = 'POINT'
    delete_geometry_001.mode = 'ALL'

    # node Named Attribute.001
    named_attribute_001 = circle_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.data_type = 'BOOLEAN'
    # Name
    named_attribute_001.inputs[0].default_value = "was_hit"

    # node Instance on Points
    instance_on_points = circle_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.inputs[1].hide = True
    instance_on_points.inputs[3].hide = True
    instance_on_points.inputs[4].hide = True
    instance_on_points.inputs[5].hide = True
    instance_on_points.inputs[6].hide = True
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Mesh Circle
    mesh_circle = circle_sim_group.nodes.new("GeometryNodeMeshCircle")
    mesh_circle.name = "Mesh Circle"
    mesh_circle.fill_type = 'NGON'
    # Vertices
    mesh_circle.inputs[0].default_value = 32
    # Radius
    mesh_circle.inputs[1].default_value = 1.0

    # node Transform Geometry
    transform_geometry = circle_sim_group.nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.mode = 'COMPONENTS'
    transform_geometry.inputs[2].hide = True
    transform_geometry.inputs[4].hide = True
    # Translation
    transform_geometry.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry.inputs[2].default_value = (1.5707963705062866, 0.0, 0.0)

    # node Named Attribute.003
    named_attribute_003 = circle_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.data_type = 'FLOAT'
    # Name
    named_attribute_003.inputs[0].default_value = "cs"

    # node Attribute Statistic
    attribute_statistic = circle_sim_group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.data_type = 'FLOAT'
    attribute_statistic.domain = 'POINT'
    attribute_statistic.inputs[1].hide = True
    attribute_statistic.outputs[1].hide = True
    attribute_statistic.outputs[2].hide = True
    attribute_statistic.outputs[3].hide = True
    attribute_statistic.outputs[4].hide = True
    attribute_statistic.outputs[5].hide = True
    attribute_statistic.outputs[6].hide = True
    attribute_statistic.outputs[7].hide = True
    # Selection
    attribute_statistic.inputs[1].default_value = True

    # node Set Material
    set_material = circle_sim_group.nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    # Selection
    set_material.inputs[1].default_value = True

    # node Transform Geometry.001
    transform_geometry_001 = circle_sim_group.nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.mode = 'COMPONENTS'
    transform_geometry_001.inputs[1].hide = True
    transform_geometry_001.inputs[2].hide = True
    transform_geometry_001.inputs[4].hide = True
    # Translation
    transform_geometry_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_001.inputs[2].default_value = (1.5707963705062866, 0.0, 0.0)

    # node Attribute Statistic.001
    attribute_statistic_001 = circle_sim_group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.data_type = 'FLOAT'
    attribute_statistic_001.domain = 'POINT'
    attribute_statistic_001.inputs[1].hide = True
    attribute_statistic_001.outputs[1].hide = True
    attribute_statistic_001.outputs[2].hide = True
    attribute_statistic_001.outputs[3].hide = True
    attribute_statistic_001.outputs[4].hide = True
    attribute_statistic_001.outputs[5].hide = True
    attribute_statistic_001.outputs[6].hide = True
    attribute_statistic_001.outputs[7].hide = True
    # Selection
    attribute_statistic_001.inputs[1].default_value = True

    # node Reroute
    reroute = circle_sim_group.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    # node Reroute.001
    reroute_001 = circle_sim_group.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    # node Combine XYZ
    combine_xyz = circle_sim_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    combine_xyz.inputs[0].hide = True
    combine_xyz.inputs[2].hide = True
    # X
    combine_xyz.inputs[0].default_value = 0.0
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # node UV Unwrap
    uv_unwrap = circle_sim_group.nodes.new("GeometryNodeUVUnwrap")
    uv_unwrap.name = "UV Unwrap"
    uv_unwrap.method = 'ANGLE_BASED'
    uv_unwrap.inputs[0].hide = True
    uv_unwrap.inputs[2].hide = True
    uv_unwrap.inputs[3].hide = True
    # Selection
    uv_unwrap.inputs[0].default_value = True
    # Margin
    uv_unwrap.inputs[2].default_value = 0.0010000000474974513
    # Fill Holes
    uv_unwrap.inputs[3].default_value = True

    # node Boolean
    boolean = circle_sim_group.nodes.new("FunctionNodeInputBool")
    boolean.name = "Boolean"
    boolean.boolean = True

    # node Pack UV Islands
    pack_uv_islands = circle_sim_group.nodes.new("GeometryNodeUVPackIslands")
    pack_uv_islands.name = "Pack UV Islands"
    pack_uv_islands.inputs[1].hide = True
    pack_uv_islands.inputs[2].hide = True
    pack_uv_islands.inputs[3].hide = True
    # Selection
    pack_uv_islands.inputs[1].default_value = True
    # Margin
    pack_uv_islands.inputs[2].default_value = 0.0010000000474974513
    # Rotate
    pack_uv_islands.inputs[3].default_value = True

    # node Reroute.002
    reroute_002 = circle_sim_group.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    # node Store Named Attribute
    store_named_attribute = circle_sim_group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT_VECTOR'
    store_named_attribute.domain = 'CORNER'
    store_named_attribute.inputs[1].hide = True
    store_named_attribute.inputs[2].hide = True
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "UVMap"

    # node Reroute.003
    reroute_003 = circle_sim_group.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    # node Reroute.004
    reroute_004 = circle_sim_group.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    # node Reroute.007
    reroute_007 = circle_sim_group.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    # node Reroute.008
    reroute_008 = circle_sim_group.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    # node Group Input.001
    group_input_001 = circle_sim_group.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True

    # node Group Input.002
    group_input_002 = circle_sim_group.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True

    # node Reroute.010
    reroute_010 = circle_sim_group.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    # node Reroute.011
    reroute_011 = circle_sim_group.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    # node Reroute.012
    reroute_012 = circle_sim_group.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    # node Reroute.013
    reroute_013 = circle_sim_group.nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    # node Reroute.009
    reroute_009 = circle_sim_group.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    # node Reroute.014
    reroute_014 = circle_sim_group.nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    # node Group Input.003
    group_input_003 = circle_sim_group.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"

    # node Reroute.005
    reroute_005 = circle_sim_group.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    # node Instance on Points.001
    instance_on_points_001 = circle_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = True
    # Rotation
    instance_on_points_001.inputs[5].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    instance_on_points_001.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Named Attribute.002
    named_attribute_002 = circle_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.data_type = 'INT'
    # Name
    named_attribute_002.inputs[0].default_value = "combo"

    # node Math.001
    math_001 = circle_sim_group.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'SUBTRACT'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 1.0

    # node Join Geometry
    join_geometry = circle_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    # node Frame
    frame = circle_sim_group.nodes.new("NodeFrame")
    frame.label = "Instance Combo"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # node Set Position
    set_position = circle_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Viewer
    viewer = circle_sim_group.nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.data_type = 'FLOAT'
    viewer.domain = 'AUTO'
    # Value
    viewer.inputs[1].default_value = 0.0

    # node Set Position.001
    set_position_001 = circle_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    set_position_001.inputs[3].default_value = (0.0, -0.029999999329447746, 0.0)

    # Set parents
    group_input_003.parent = frame
    instance_on_points_001.parent = frame
    named_attribute_002.parent = frame
    math_001.parent = frame
    set_position_001.parent = frame

    # Set locations
    group_output.location = (1900.0, -40.0)
    group_input.location = (-1000.0, -80.0)
    realize_instances.location = (-840.0, -80.0)
    delete_geometry.location = (-660.0, -80.0)
    named_attribute.location = (-660.0, -280.0)
    boolean_math.location = (-660.0, -240.0)
    delete_geometry_001.location = (-480.0, -80.0)
    named_attribute_001.location = (-480.0, -240.0)
    instance_on_points.location = (1060.0, 120.0)
    mesh_circle.location = (-320.0, -240.0)
    transform_geometry.location = (820.0, 20.0)
    named_attribute_003.location = (0.0, -580.0)
    attribute_statistic.location = (180.0, -120.0)
    set_material.location = (1220.0, 120.0)
    transform_geometry_001.location = (820.0, -380.0)
    attribute_statistic_001.location = (180.0, -480.0)
    reroute.location = (-680.0, -120.0)
    reroute_001.location = (-680.0, -600.0)
    combine_xyz.location = (1680.0, -20.0)
    uv_unwrap.location = (-160.0, -480.0)
    boolean.location = (-160.0, -580.0)
    pack_uv_islands.location = (-160.0, -400.0)
    reroute_002.location = (40.0, -280.0)
    store_named_attribute.location = (-160.0, -240.0)
    reroute_003.location = (40.0, -60.0)
    reroute_004.location = (40.0, -460.0)
    reroute_007.location = (1420.0, -100.0)
    reroute_008.location = (1122.260009765625, -420.0)
    group_input_001.location = (1680.0, -120.0)
    group_input_002.location = (1220.0, -20.0)
    reroute_010.location = (160.0, -620.0)
    reroute_011.location = (160.0, -260.0)
    reroute_012.location = (-240.0, -120.0)
    reroute_013.location = (-240.0, 60.0)
    reroute_009.location = (-680.0, -180.0)
    reroute_014.location = (-240.0, -200.0)
    group_input_003.location = (980.0, 520.0)
    reroute_005.location = (942.3284301757812, 60.0)
    instance_on_points_001.location = (1180.0, 520.0)
    named_attribute_002.location = (800.0, 360.0)
    math_001.location = (980.0, 360.0)
    join_geometry.location = (1540.0, 140.0)
    frame.location = (0.0, 0.0)
    set_position.location = (1700.0, 140.0)
    viewer.location = (1720.0, 246.0)
    set_position_001.location = (1340.0, 520.0)

    # Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    realize_instances.width, realize_instances.height = 140.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    boolean_math.width, boolean_math.height = 140.0, 100.0
    delete_geometry_001.width, delete_geometry_001.height = 140.0, 100.0
    named_attribute_001.width, named_attribute_001.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    mesh_circle.width, mesh_circle.height = 140.0, 100.0
    transform_geometry.width, transform_geometry.height = 140.0, 100.0
    named_attribute_003.width, named_attribute_003.height = 140.0, 100.0
    attribute_statistic.width, attribute_statistic.height = 140.0, 100.0
    set_material.width, set_material.height = 140.0, 100.0
    transform_geometry_001.width, transform_geometry_001.height = 140.0, 100.0
    attribute_statistic_001.width, attribute_statistic_001.height = 140.0, 100.0
    reroute.width, reroute.height = 100.0, 100.0
    reroute_001.width, reroute_001.height = 100.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    uv_unwrap.width, uv_unwrap.height = 140.0, 100.0
    boolean.width, boolean.height = 140.0, 100.0
    pack_uv_islands.width, pack_uv_islands.height = 140.0, 100.0
    reroute_002.width, reroute_002.height = 100.0, 100.0
    store_named_attribute.width, store_named_attribute.height = 140.0, 100.0
    reroute_003.width, reroute_003.height = 100.0, 100.0
    reroute_004.width, reroute_004.height = 100.0, 100.0
    reroute_007.width, reroute_007.height = 100.0, 100.0
    reroute_008.width, reroute_008.height = 100.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    reroute_010.width, reroute_010.height = 100.0, 100.0
    reroute_011.width, reroute_011.height = 100.0, 100.0
    reroute_012.width, reroute_012.height = 100.0, 100.0
    reroute_013.width, reroute_013.height = 100.0, 100.0
    reroute_009.width, reroute_009.height = 100.0, 100.0
    reroute_014.width, reroute_014.height = 100.0, 100.0
    group_input_003.width, group_input_003.height = 140.0, 100.0
    reroute_005.width, reroute_005.height = 100.0, 100.0
    instance_on_points_001.width, instance_on_points_001.height = 140.0, 100.0
    named_attribute_002.width, named_attribute_002.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    frame.width, frame.height = 740.0, 397.0
    set_position.width, set_position.height = 140.0, 100.0
    viewer.width, viewer.height = 140.0, 100.0
    set_position_001.width, set_position_001.height = 140.0, 100.0

    # initialize circle_sim_group links
    # named_attribute.Attribute -> boolean_math.Boolean
    circle_sim_group.links.new(named_attribute.outputs[0], boolean_math.inputs[0])
    # group_input.Geometry -> realize_instances.Geometry
    circle_sim_group.links.new(group_input.outputs[0], realize_instances.inputs[0])
    # reroute_009.Output -> delete_geometry.Geometry
    circle_sim_group.links.new(reroute_009.outputs[0], delete_geometry.inputs[0])
    # delete_geometry.Geometry -> delete_geometry_001.Geometry
    circle_sim_group.links.new(delete_geometry.outputs[0], delete_geometry_001.inputs[0])
    # named_attribute_001.Attribute -> delete_geometry_001.Selection
    circle_sim_group.links.new(named_attribute_001.outputs[0], delete_geometry_001.inputs[1])
    # reroute_005.Output -> instance_on_points.Points
    circle_sim_group.links.new(reroute_005.outputs[0], instance_on_points.inputs[0])
    # set_position.Geometry -> group_output.Circles
    circle_sim_group.links.new(set_position.outputs[0], group_output.inputs[0])
    # reroute_003.Output -> transform_geometry.Geometry
    circle_sim_group.links.new(reroute_003.outputs[0], transform_geometry.inputs[0])
    # transform_geometry.Geometry -> instance_on_points.Instance
    circle_sim_group.links.new(transform_geometry.outputs[0], instance_on_points.inputs[2])
    # reroute_014.Output -> attribute_statistic.Geometry
    circle_sim_group.links.new(reroute_014.outputs[0], attribute_statistic.inputs[0])
    # reroute_011.Output -> attribute_statistic.Attribute
    circle_sim_group.links.new(reroute_011.outputs[0], attribute_statistic.inputs[2])
    # instance_on_points.Instances -> set_material.Geometry
    circle_sim_group.links.new(instance_on_points.outputs[0], set_material.inputs[0])
    # reroute_004.Output -> transform_geometry_001.Geometry
    circle_sim_group.links.new(reroute_004.outputs[0], transform_geometry_001.inputs[0])
    # reroute_001.Output -> attribute_statistic_001.Geometry
    circle_sim_group.links.new(reroute_001.outputs[0], attribute_statistic_001.inputs[0])
    # reroute_010.Output -> attribute_statistic_001.Attribute
    circle_sim_group.links.new(reroute_010.outputs[0], attribute_statistic_001.inputs[2])
    # reroute_007.Output -> group_output.Circle Mesh
    circle_sim_group.links.new(reroute_007.outputs[0], group_output.inputs[1])
    # realize_instances.Geometry -> reroute.Input
    circle_sim_group.links.new(realize_instances.outputs[0], reroute.inputs[0])
    # reroute_009.Output -> reroute_001.Input
    circle_sim_group.links.new(reroute_009.outputs[0], reroute_001.inputs[0])
    # boolean.Boolean -> uv_unwrap.Seam
    circle_sim_group.links.new(boolean.outputs[0], uv_unwrap.inputs[1])
    # uv_unwrap.UV -> pack_uv_islands.UV
    circle_sim_group.links.new(uv_unwrap.outputs[0], pack_uv_islands.inputs[0])
    # store_named_attribute.Geometry -> reroute_002.Input
    circle_sim_group.links.new(store_named_attribute.outputs[0], reroute_002.inputs[0])
    # mesh_circle.Mesh -> store_named_attribute.Geometry
    circle_sim_group.links.new(mesh_circle.outputs[0], store_named_attribute.inputs[0])
    # pack_uv_islands.UV -> store_named_attribute.Value
    circle_sim_group.links.new(pack_uv_islands.outputs[0], store_named_attribute.inputs[3])
    # reroute_002.Output -> reroute_003.Input
    circle_sim_group.links.new(reroute_002.outputs[0], reroute_003.inputs[0])
    # reroute_002.Output -> reroute_004.Input
    circle_sim_group.links.new(reroute_002.outputs[0], reroute_004.inputs[0])
    # reroute_008.Output -> reroute_007.Input
    circle_sim_group.links.new(reroute_008.outputs[0], reroute_007.inputs[0])
    # transform_geometry_001.Geometry -> reroute_008.Input
    circle_sim_group.links.new(transform_geometry_001.outputs[0], reroute_008.inputs[0])
    # group_input_001.Y Offset -> combine_xyz.Y
    circle_sim_group.links.new(group_input_001.outputs[2], combine_xyz.inputs[1])
    # group_input_002.Circle Material -> set_material.Material
    circle_sim_group.links.new(group_input_002.outputs[1], set_material.inputs[2])
    # named_attribute_003.Attribute -> reroute_010.Input
    circle_sim_group.links.new(named_attribute_003.outputs[0], reroute_010.inputs[0])
    # reroute_010.Output -> reroute_011.Input
    circle_sim_group.links.new(reroute_010.outputs[0], reroute_011.inputs[0])
    # delete_geometry_001.Geometry -> reroute_012.Input
    circle_sim_group.links.new(delete_geometry_001.outputs[0], reroute_012.inputs[0])
    # reroute_012.Output -> reroute_013.Input
    circle_sim_group.links.new(reroute_012.outputs[0], reroute_013.inputs[0])
    # boolean_math.Boolean -> delete_geometry.Selection
    circle_sim_group.links.new(boolean_math.outputs[0], delete_geometry.inputs[1])
    # reroute.Output -> reroute_009.Input
    circle_sim_group.links.new(reroute.outputs[0], reroute_009.inputs[0])
    # reroute_012.Output -> reroute_014.Input
    circle_sim_group.links.new(reroute_012.outputs[0], reroute_014.inputs[0])
    # reroute_013.Output -> reroute_005.Input
    circle_sim_group.links.new(reroute_013.outputs[0], reroute_005.inputs[0])
    # reroute_005.Output -> instance_on_points_001.Points
    circle_sim_group.links.new(reroute_005.outputs[0], instance_on_points_001.inputs[0])
    # group_input_003.Instance -> instance_on_points_001.Instance
    circle_sim_group.links.new(group_input_003.outputs[3], instance_on_points_001.inputs[2])
    # named_attribute_002.Attribute -> math_001.Value
    circle_sim_group.links.new(named_attribute_002.outputs[0], math_001.inputs[0])
    # math_001.Value -> instance_on_points_001.Instance Index
    circle_sim_group.links.new(math_001.outputs[0], instance_on_points_001.inputs[4])
    # set_material.Geometry -> join_geometry.Geometry
    circle_sim_group.links.new(set_material.outputs[0], join_geometry.inputs[0])
    # join_geometry.Geometry -> set_position.Geometry
    circle_sim_group.links.new(join_geometry.outputs[0], set_position.inputs[0])
    # combine_xyz.Vector -> set_position.Offset
    circle_sim_group.links.new(combine_xyz.outputs[0], set_position.inputs[3])
    # join_geometry.Geometry -> viewer.Geometry
    circle_sim_group.links.new(join_geometry.outputs[0], viewer.inputs[0])
    # instance_on_points_001.Instances -> set_position_001.Geometry
    circle_sim_group.links.new(instance_on_points_001.outputs[0], set_position_001.inputs[0])
    # attribute_statistic_001.Mean -> transform_geometry_001.Scale
    circle_sim_group.links.new(attribute_statistic_001.outputs[0], transform_geometry_001.inputs[3])
    # attribute_statistic.Mean -> transform_geometry.Scale
    circle_sim_group.links.new(attribute_statistic.outputs[0], transform_geometry.inputs[3])
    # set_position_001.Geometry -> join_geometry.Geometry
    circle_sim_group.links.new(set_position_001.outputs[0], join_geometry.inputs[0])
    return circle_sim_group

# initialize slider_sim_group node group
def slider_sim_group_node_group():
    slider_sim_group = bpy.data.node_groups.new(type='GeometryNodeTree', name="Slider Sim Group")

    slider_sim_group.color_tag = 'NONE'
    slider_sim_group.description = ""

    # slider_sim_group interface
    # Socket Geometry
    geometry_socket_1 = slider_sim_group.interface.new_socket(name="Geometry", in_out='OUTPUT',
                                                              socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    # Socket Geometry
    geometry_socket_2 = slider_sim_group.interface.new_socket(name="Geometry", in_out='INPUT',
                                                              socket_type='NodeSocketGeometry')
    geometry_socket_2.attribute_domain = 'POINT'

    # Socket Circle Mesh
    circle_mesh_socket_1 = slider_sim_group.interface.new_socket(name="Circle Mesh", in_out='INPUT',
                                                                 socket_type='NodeSocketGeometry')
    circle_mesh_socket_1.attribute_domain = 'POINT'

    # Socket Slider Head/Tail
    slider_head_tail_socket = slider_sim_group.interface.new_socket(name="Slider Head/Tail", in_out='INPUT',
                                                                    socket_type='NodeSocketGeometry')
    slider_head_tail_socket.attribute_domain = 'POINT'

    # Socket Slider Material
    slider_material_socket = slider_sim_group.interface.new_socket(name="Slider Material", in_out='INPUT',
                                                                   socket_type='NodeSocketMaterial')
    slider_material_socket.attribute_domain = 'POINT'

    # Socket Enable Slider Balls
    enable_slider_balls_socket = slider_sim_group.interface.new_socket(name="Enable Slider Balls", in_out='INPUT',
                                                                       socket_type='NodeSocketBool')
    enable_slider_balls_socket.default_value = True
    enable_slider_balls_socket.attribute_domain = 'POINT'

    # Socket Slider Balls
    slider_balls_socket = slider_sim_group.interface.new_socket(name="Slider Balls", in_out='INPUT',
                                                                socket_type='NodeSocketCollection')
    slider_balls_socket.attribute_domain = 'POINT'

    # Socket Slider Balls Material
    slider_balls_material_socket = slider_sim_group.interface.new_socket(name="Slider Balls Material", in_out='INPUT',
                                                                         socket_type='NodeSocketMaterial')
    slider_balls_material_socket.attribute_domain = 'POINT'

    # Socket Slider Head/Tail Material
    slider_head_tail_material_socket = slider_sim_group.interface.new_socket(name="Slider Head/Tail Material",
                                                                             in_out='INPUT',
                                                                             socket_type='NodeSocketMaterial')
    slider_head_tail_material_socket.attribute_domain = 'POINT'

    # Socket Instance
    instance_socket_1 = slider_sim_group.interface.new_socket(name="Instance", in_out='INPUT',
                                                              socket_type='NodeSocketGeometry')
    instance_socket_1.attribute_domain = 'POINT'

    # initialize slider_sim_group nodes
    # node Group Output
    group_output_1 = slider_sim_group.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True

    # node Group Input
    group_input_1 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_1.name = "Group Input"
    group_input_1.outputs[1].hide = True
    group_input_1.outputs[2].hide = True
    group_input_1.outputs[3].hide = True
    group_input_1.outputs[4].hide = True
    group_input_1.outputs[5].hide = True
    group_input_1.outputs[6].hide = True
    group_input_1.outputs[7].hide = True
    group_input_1.outputs[8].hide = True
    group_input_1.outputs[9].hide = True

    # node Realize Instances
    realize_instances_1 = slider_sim_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_1.name = "Realize Instances"
    # Selection
    realize_instances_1.inputs[1].default_value = True
    # Realize All
    realize_instances_1.inputs[2].default_value = True
    # Depth
    realize_instances_1.inputs[3].default_value = 0

    # node Delete Geometry
    delete_geometry_1 = slider_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_1.name = "Delete Geometry"
    delete_geometry_1.domain = 'CURVE'
    delete_geometry_1.mode = 'ALL'

    # node Named Attribute
    named_attribute_1 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_1.name = "Named Attribute"
    named_attribute_1.data_type = 'FLOAT'
    # Name
    named_attribute_1.inputs[0].default_value = "show"

    # node Boolean Math
    boolean_math_1 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_1.name = "Boolean Math"
    boolean_math_1.hide = True
    boolean_math_1.operation = 'NOT'

    # node Curve to Mesh
    curve_to_mesh = slider_sim_group.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.inputs[2].hide = True
    # Fill Caps
    curve_to_mesh.inputs[2].default_value = False

    # node Frame
    frame_1 = slider_sim_group.nodes.new("NodeFrame")
    frame_1.label = "Init Splines"
    frame_1.name = "Frame"
    frame_1.label_size = 20
    frame_1.shrink = True

    # node Frame.003
    frame_003 = slider_sim_group.nodes.new("NodeFrame")
    frame_003.label = "Instance Head and Tail on Slider"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    # node Set Curve Radius
    set_curve_radius = slider_sim_group.nodes.new("GeometryNodeSetCurveRadius")
    set_curve_radius.name = "Set Curve Radius"
    set_curve_radius.inputs[1].hide = True
    # Selection
    set_curve_radius.inputs[1].default_value = True

    # node Reroute.001
    reroute_001_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_001_1.name = "Reroute.001"
    # node Delete Geometry.001
    delete_geometry_001_1 = slider_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001_1.name = "Delete Geometry.001"
    delete_geometry_001_1.domain = 'CURVE'
    delete_geometry_001_1.mode = 'ALL'

    # node Named Attribute.001
    named_attribute_001_1 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001_1.name = "Named Attribute.001"
    named_attribute_001_1.data_type = 'BOOLEAN'
    # Name
    named_attribute_001_1.inputs[0].default_value = "was_completed"

    # node Reroute.002
    reroute_002_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_002_1.name = "Reroute.002"
    # node Set Material
    set_material_1 = slider_sim_group.nodes.new("GeometryNodeSetMaterial")
    set_material_1.name = "Set Material"
    # Selection
    set_material_1.inputs[1].default_value = True

    # node Collection Info
    collection_info = slider_sim_group.nodes.new("GeometryNodeCollectionInfo")
    collection_info.name = "Collection Info"
    collection_info.transform_space = 'ORIGINAL'
    collection_info.inputs[1].hide = True
    collection_info.inputs[2].hide = True
    # Separate Children
    collection_info.inputs[1].default_value = False
    # Reset Children
    collection_info.inputs[2].default_value = False

    # node Realize Instances.001
    realize_instances_001 = slider_sim_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.inputs[1].hide = True
    realize_instances_001.inputs[2].hide = True
    realize_instances_001.inputs[3].hide = True
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0

    # node Delete Geometry.002
    delete_geometry_002 = slider_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.domain = 'POINT'
    delete_geometry_002.mode = 'ALL'

    # node Named Attribute.002
    named_attribute_002_1 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002_1.name = "Named Attribute.002"
    named_attribute_002_1.data_type = 'FLOAT'
    # Name
    named_attribute_002_1.inputs[0].default_value = "show"

    # node Boolean Math.001
    boolean_math_001 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.hide = True
    boolean_math_001.operation = 'NOT'

    # node Delete Geometry.003
    delete_geometry_003 = slider_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.name = "Delete Geometry.003"
    delete_geometry_003.domain = 'POINT'
    delete_geometry_003.mode = 'ALL'

    # node Named Attribute.005
    named_attribute_005 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.name = "Named Attribute.005"
    named_attribute_005.data_type = 'BOOLEAN'
    # Name
    named_attribute_005.inputs[0].default_value = "was_completed"

    # node Switch
    switch = slider_sim_group.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    # node Instance on Points
    instance_on_points_1 = slider_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_1.name = "Instance on Points"
    instance_on_points_1.inputs[1].hide = True
    instance_on_points_1.inputs[3].hide = True
    instance_on_points_1.inputs[4].hide = True
    instance_on_points_1.inputs[5].hide = True
    instance_on_points_1.inputs[6].hide = True
    # Selection
    instance_on_points_1.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_1.inputs[3].default_value = False
    # Instance Index
    instance_on_points_1.inputs[4].default_value = 0
    # Rotation
    instance_on_points_1.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_1.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Set Position
    set_position_1 = slider_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_1.name = "Set Position"
    # Selection
    set_position_1.inputs[1].default_value = True
    # Position
    set_position_1.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    set_position_1.inputs[3].default_value = (0.0, 0.019999999552965164, 0.0)

    # node Set Position.002
    set_position_002 = slider_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Position
    set_position_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    set_position_002.inputs[3].default_value = (0.0, 0.03999999910593033, 0.0)

    # node Group Input.001
    group_input_001_1 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_001_1.name = "Group Input.001"
    group_input_001_1.outputs[0].hide = True
    group_input_001_1.outputs[1].hide = True
    group_input_001_1.outputs[2].hide = True
    group_input_001_1.outputs[3].hide = True
    group_input_001_1.outputs[4].hide = True
    group_input_001_1.outputs[5].hide = True
    group_input_001_1.outputs[6].hide = True
    group_input_001_1.outputs[8].hide = True
    group_input_001_1.outputs[9].hide = True

    # node Group Input.004
    group_input_004 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[9].hide = True

    # node Group Input.005
    group_input_005 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[1].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[5].hide = True
    group_input_005.outputs[6].hide = True
    group_input_005.outputs[7].hide = True
    group_input_005.outputs[8].hide = True
    group_input_005.outputs[9].hide = True

    # node Group Input.009
    group_input_009 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_009.name = "Group Input.009"
    group_input_009.outputs[0].hide = True
    group_input_009.outputs[2].hide = True
    group_input_009.outputs[3].hide = True
    group_input_009.outputs[4].hide = True
    group_input_009.outputs[5].hide = True
    group_input_009.outputs[6].hide = True
    group_input_009.outputs[7].hide = True
    group_input_009.outputs[8].hide = True
    group_input_009.outputs[9].hide = True

    # node Group Input.010
    group_input_010 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_010.name = "Group Input.010"
    group_input_010.outputs[0].hide = True
    group_input_010.outputs[1].hide = True
    group_input_010.outputs[2].hide = True
    group_input_010.outputs[4].hide = True
    group_input_010.outputs[5].hide = True
    group_input_010.outputs[6].hide = True
    group_input_010.outputs[7].hide = True
    group_input_010.outputs[8].hide = True
    group_input_010.outputs[9].hide = True

    # node Frame.002
    frame_002 = slider_sim_group.nodes.new("NodeFrame")
    frame_002.label = "Instance Slider Balls"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    # node Set Material.005
    set_material_005 = slider_sim_group.nodes.new("GeometryNodeSetMaterial")
    set_material_005.name = "Set Material.005"
    # Selection
    set_material_005.inputs[1].default_value = True

    # node Group Input.008
    group_input_008 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_008.name = "Group Input.008"
    group_input_008.outputs[0].hide = True
    group_input_008.outputs[1].hide = True
    group_input_008.outputs[2].hide = True
    group_input_008.outputs[3].hide = True
    group_input_008.outputs[4].hide = True
    group_input_008.outputs[5].hide = True
    group_input_008.outputs[7].hide = True
    group_input_008.outputs[8].hide = True
    group_input_008.outputs[9].hide = True

    # node Join Geometry.002
    join_geometry_002 = slider_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"

    # node Join Geometry.003
    join_geometry_003 = slider_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"

    # node Reroute.013
    reroute_013_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_013_1.name = "Reroute.013"
    # node Reroute.016
    reroute_016 = slider_sim_group.nodes.new("NodeReroute")
    reroute_016.name = "Reroute.016"
    # node Set Spline Type
    set_spline_type = slider_sim_group.nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.spline_type = 'NURBS'
    # Selection
    set_spline_type.inputs[1].default_value = True

    # node Join Geometry
    join_geometry_1 = slider_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_1.name = "Join Geometry"

    # node Mesh Line
    mesh_line = slider_sim_group.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'END_POINTS'
    # Count
    mesh_line.inputs[0].default_value = 2
    # Start Location
    mesh_line.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    mesh_line.inputs[3].default_value = (0.0, 1.0, 0.0)

    # node Mesh Line.001
    mesh_line_001 = slider_sim_group.nodes.new("GeometryNodeMeshLine")
    mesh_line_001.name = "Mesh Line.001"
    mesh_line_001.count_mode = 'TOTAL'
    mesh_line_001.mode = 'END_POINTS'
    # Count
    mesh_line_001.inputs[0].default_value = 2
    # Start Location
    mesh_line_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    mesh_line_001.inputs[3].default_value = (0.0, -1.0, 0.0)

    # node Mesh to Curve.001
    mesh_to_curve_001 = slider_sim_group.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True

    # node Resample Curve
    resample_curve = slider_sim_group.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.mode = 'COUNT'
    # Selection
    resample_curve.inputs[1].default_value = True
    # Count
    resample_curve.inputs[2].default_value = 3

    # node Reroute.007
    reroute_007_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_007_1.name = "Reroute.007"
    # node Reroute.008
    reroute_008_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_008_1.name = "Reroute.008"
    # node Named Attribute.006
    named_attribute_006 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_006.name = "Named Attribute.006"
    named_attribute_006.data_type = 'FLOAT'
    # Name
    named_attribute_006.inputs[0].default_value = "cs"

    # node Attribute Statistic.002
    attribute_statistic_002 = slider_sim_group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_002.name = "Attribute Statistic.002"
    attribute_statistic_002.data_type = 'FLOAT'
    attribute_statistic_002.domain = 'POINT'
    attribute_statistic_002.inputs[1].hide = True
    attribute_statistic_002.outputs[1].hide = True
    attribute_statistic_002.outputs[2].hide = True
    attribute_statistic_002.outputs[3].hide = True
    attribute_statistic_002.outputs[4].hide = True
    attribute_statistic_002.outputs[5].hide = True
    attribute_statistic_002.outputs[6].hide = True
    attribute_statistic_002.outputs[7].hide = True
    # Selection
    attribute_statistic_002.inputs[1].default_value = True

    # node Reroute.009
    reroute_009_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_009_1.name = "Reroute.009"
    # node Instance on Points.001
    instance_on_points_001_1 = slider_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001_1.name = "Instance on Points.001"
    instance_on_points_001_1.inputs[3].hide = True
    instance_on_points_001_1.inputs[5].hide = True
    instance_on_points_001_1.inputs[6].hide = True
    # Pick Instance
    instance_on_points_001_1.inputs[3].default_value = True
    # Rotation
    instance_on_points_001_1.inputs[5].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    instance_on_points_001_1.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Named Attribute.004
    named_attribute_004 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.name = "Named Attribute.004"
    named_attribute_004.data_type = 'INT'
    # Name
    named_attribute_004.inputs[0].default_value = "combo"

    # node Math.001
    math_001_1 = slider_sim_group.nodes.new("ShaderNodeMath")
    math_001_1.name = "Math.001"
    math_001_1.operation = 'SUBTRACT'
    math_001_1.use_clamp = False
    # Value_001
    math_001_1.inputs[1].default_value = 1.0

    # node Join Geometry.001
    join_geometry_001 = slider_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"

    # node Group Input.012
    group_input_012 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_012.name = "Group Input.012"
    group_input_012.outputs[0].hide = True
    group_input_012.outputs[1].hide = True
    group_input_012.outputs[2].hide = True
    group_input_012.outputs[3].hide = True
    group_input_012.outputs[4].hide = True
    group_input_012.outputs[5].hide = True
    group_input_012.outputs[6].hide = True
    group_input_012.outputs[7].hide = True
    group_input_012.outputs[9].hide = True

    # node Reroute.010
    reroute_010_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_010_1.name = "Reroute.010"
    # node Reroute.011
    reroute_011_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_011_1.name = "Reroute.011"
    # node Reroute.014
    reroute_014_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_014_1.name = "Reroute.014"
    # node Frame.006
    frame_006 = slider_sim_group.nodes.new("NodeFrame")
    frame_006.label = "Combo"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True

    # node Set Material.002
    set_material_002 = slider_sim_group.nodes.new("GeometryNodeSetMaterial")
    set_material_002.name = "Set Material.002"
    # Selection
    set_material_002.inputs[1].default_value = True

    # node Store Named Attribute.003
    store_named_attribute_003 = slider_sim_group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'FLOAT'
    store_named_attribute_003.domain = 'POINT'
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "Distance"

    # node Geometry Proximity
    geometry_proximity = slider_sim_group.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'POINTS'
    # Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Curve to Mesh.001
    curve_to_mesh_001 = slider_sim_group.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.inputs[2].hide = True
    # Fill Caps
    curve_to_mesh_001.inputs[2].default_value = False

    # node Mesh Island
    mesh_island = slider_sim_group.nodes.new("GeometryNodeInputMeshIsland")
    mesh_island.name = "Mesh Island"

    # node Frame.001
    frame_001 = slider_sim_group.nodes.new("NodeFrame")
    frame_001.label = "Slider Path"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # node Merge by Distance
    merge_by_distance = slider_sim_group.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.mode = 'ALL'
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Distance
    merge_by_distance.inputs[2].default_value = 0.0010000000474974513

    # node Instance on Points.002
    instance_on_points_002 = slider_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Rotation
    instance_on_points_002.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_002.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Endpoint Selection
    endpoint_selection = slider_sim_group.nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.name = "Endpoint Selection"
    # Start Size
    endpoint_selection.inputs[0].default_value = 1
    # End Size
    endpoint_selection.inputs[1].default_value = 1

    # node Group Input.011
    group_input_011 = slider_sim_group.nodes.new("NodeGroupInput")
    group_input_011.name = "Group Input.011"
    group_input_011.outputs[0].hide = True
    group_input_011.outputs[2].hide = True
    group_input_011.outputs[3].hide = True
    group_input_011.outputs[4].hide = True
    group_input_011.outputs[5].hide = True
    group_input_011.outputs[6].hide = True
    group_input_011.outputs[7].hide = True
    group_input_011.outputs[8].hide = True
    group_input_011.outputs[9].hide = True

    # node Endpoint Selection.001
    endpoint_selection_001 = slider_sim_group.nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.name = "Endpoint Selection.001"
    # Start Size
    endpoint_selection_001.inputs[0].default_value = 1
    # End Size
    endpoint_selection_001.inputs[1].default_value = 0

    # node Store Named Attribute
    store_named_attribute_1 = slider_sim_group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_1.name = "Store Named Attribute"
    store_named_attribute_1.data_type = 'BOOLEAN'
    store_named_attribute_1.domain = 'INSTANCE'
    # Name
    store_named_attribute_1.inputs[2].default_value = "head"
    # Value
    store_named_attribute_1.inputs[3].default_value = True

    # node Store Named Attribute.001
    store_named_attribute_001 = slider_sim_group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'BOOLEAN'
    store_named_attribute_001.domain = 'INSTANCE'
    # Name
    store_named_attribute_001.inputs[2].default_value = "tail"
    # Value
    store_named_attribute_001.inputs[3].default_value = True

    # node Index.001
    index_001 = slider_sim_group.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"

    # node Math.004
    math_004 = slider_sim_group.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'FLOORED_MODULO'
    math_004.use_clamp = False
    # Value_001
    math_004.inputs[1].default_value = 2.0

    # node Compare
    compare = slider_sim_group.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    # B
    compare.inputs[1].default_value = 1.0
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513

    # node Compare.001
    compare_001 = slider_sim_group.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'FLOAT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'EQUAL'
    # B
    compare_001.inputs[1].default_value = 0.0
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513

    # node Set Position.001
    set_position_001_1 = slider_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_001_1.name = "Set Position.001"
    # Position
    set_position_001_1.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    set_position_001_1.inputs[3].default_value = (0.0, 0.029999999329447746, 0.0)

    # node Named Attribute.003
    named_attribute_003_1 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003_1.name = "Named Attribute.003"
    named_attribute_003_1.data_type = 'BOOLEAN'
    # Name
    named_attribute_003_1.inputs[0].default_value = "head"

    # node Set Position.003
    set_position_003 = slider_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    # Position
    set_position_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    set_position_003.inputs[3].default_value = (0.0, 0.04999999701976776, 0.0)

    # node Named Attribute.007
    named_attribute_007 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_007.name = "Named Attribute.007"
    named_attribute_007.data_type = 'BOOLEAN'
    # Name
    named_attribute_007.inputs[0].default_value = "tail"

    # node Reroute
    reroute_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_1.name = "Reroute"
    # node Reroute.003
    reroute_003_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_003_1.name = "Reroute.003"
    # node Reroute.004
    reroute_004_1 = slider_sim_group.nodes.new("NodeReroute")
    reroute_004_1.name = "Reroute.004"
    # node Split to Instances
    split_to_instances = slider_sim_group.nodes.new("GeometryNodeSplitToInstances")
    split_to_instances.name = "Split to Instances"
    split_to_instances.domain = 'POINT'
    # Selection
    split_to_instances.inputs[1].default_value = True

    # node Mesh Island.001
    mesh_island_001 = slider_sim_group.nodes.new("GeometryNodeInputMeshIsland")
    mesh_island_001.name = "Mesh Island.001"

    # node Store Named Attribute.002
    store_named_attribute_002 = slider_sim_group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'INT'
    store_named_attribute_002.domain = 'INSTANCE'
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "combo"

    # node Sample Index
    sample_index = slider_sim_group.nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.clamp = False
    sample_index.data_type = 'INT'
    sample_index.domain = 'CURVE'

    # node Index
    index = slider_sim_group.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # node Named Attribute.008
    named_attribute_008 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_008.name = "Named Attribute.008"
    named_attribute_008.data_type = 'INT'
    # Name
    named_attribute_008.inputs[0].default_value = "combo"

    # node Instance on Points.003
    instance_on_points_003 = slider_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Rotation
    instance_on_points_003.inputs[5].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    instance_on_points_003.inputs[6].default_value = (0.20000000298023224, 0.20000000298023224, 0.20000000298023224)

    # node Mesh Circle
    mesh_circle_1 = slider_sim_group.nodes.new("GeometryNodeMeshCircle")
    mesh_circle_1.name = "Mesh Circle"
    mesh_circle_1.fill_type = 'NGON'
    # Vertices
    mesh_circle_1.inputs[0].default_value = 3
    # Radius
    mesh_circle_1.inputs[1].default_value = 1.0

    # node Join Geometry.005
    join_geometry_005 = slider_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"

    # node Named Attribute.009
    named_attribute_009 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_009.name = "Named Attribute.009"
    named_attribute_009.data_type = 'INT'
    # Name
    named_attribute_009.inputs[0].default_value = "repeat_count"

    # node Named Attribute.010
    named_attribute_010 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_010.name = "Named Attribute.010"
    named_attribute_010.data_type = 'INT'
    # Name
    named_attribute_010.inputs[0].default_value = "repeat_counter"

    # node Compare.002
    compare_002 = slider_sim_group.nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.data_type = 'INT'
    compare_002.mode = 'ELEMENT'
    compare_002.operation = 'GREATER_THAN'
    # B_INT
    compare_002.inputs[3].default_value = 1

    # node Compare.003
    compare_003 = slider_sim_group.nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.data_type = 'INT'
    compare_003.mode = 'ELEMENT'
    compare_003.operation = 'LESS_THAN'

    # node Math.003
    math_003 = slider_sim_group.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'ADD'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 1.0

    # node Boolean Math.002
    boolean_math_002 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.operation = 'AND'

    # node Math.008
    math_008 = slider_sim_group.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'FLOORED_MODULO'
    math_008.use_clamp = False
    # Value_001
    math_008.inputs[1].default_value = 2.0

    # node Compare.004
    compare_004 = slider_sim_group.nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.data_type = 'FLOAT'
    compare_004.mode = 'ELEMENT'
    compare_004.operation = 'EQUAL'
    # B
    compare_004.inputs[1].default_value = 0.0
    # Epsilon
    compare_004.inputs[12].default_value = 0.0010000000474974513

    # node Instances to Points
    instances_to_points = slider_sim_group.nodes.new("GeometryNodeInstancesToPoints")
    instances_to_points.name = "Instances to Points"
    # Selection
    instances_to_points.inputs[1].default_value = True
    # Position
    instances_to_points.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Radius
    instances_to_points.inputs[3].default_value = 0.05000000074505806

    # node Named Attribute.011
    named_attribute_011 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_011.name = "Named Attribute.011"
    named_attribute_011.data_type = 'BOOLEAN'
    # Name
    named_attribute_011.inputs[0].default_value = "tail"

    # node Boolean Math.003
    boolean_math_003 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.operation = 'AND'

    # node Boolean Math.004
    boolean_math_004 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.operation = 'AND'

    # node Instance on Points.004
    instance_on_points_004 = slider_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Rotation
    instance_on_points_004.inputs[5].default_value = (1.5707963705062866, 3.1415927410125732, 0.0)
    # Scale
    instance_on_points_004.inputs[6].default_value = (0.20000000298023224, 0.20000000298023224, 0.20000000298023224)

    # node Boolean Math.005
    boolean_math_005 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.operation = 'AND'

    # node Named Attribute.012
    named_attribute_012 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_012.name = "Named Attribute.012"
    named_attribute_012.data_type = 'BOOLEAN'
    # Name
    named_attribute_012.inputs[0].default_value = "head"

    # node Boolean Math.006
    boolean_math_006 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_006.name = "Boolean Math.006"
    boolean_math_006.operation = 'AND'

    # node Boolean Math.007
    boolean_math_007 = slider_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_007.name = "Boolean Math.007"
    boolean_math_007.operation = 'NOT'

    # node Join Geometry.004
    join_geometry_004 = slider_sim_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"

    # node Set Position.004
    set_position_004 = slider_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    # Selection
    set_position_004.inputs[1].default_value = True
    # Position
    set_position_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    set_position_004.inputs[3].default_value = (0.0, -0.05000000074505806, 0.0)

    # node Frame.004
    frame_004 = slider_sim_group.nodes.new("NodeFrame")
    frame_004.label = "Reverse Arrows"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    # node Set Material.001
    set_material_001 = slider_sim_group.nodes.new("GeometryNodeSetMaterial")
    set_material_001.name = "Set Material.001"
    # Selection
    set_material_001.inputs[1].default_value = True
    if "Material" in bpy.data.materials:
        set_material_001.inputs[2].default_value = bpy.data.materials["Material"]

    # node Delete Geometry.004
    delete_geometry_004 = slider_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.name = "Delete Geometry.004"
    delete_geometry_004.domain = 'INSTANCE'
    delete_geometry_004.mode = 'ALL'

    # node Named Attribute.013
    named_attribute_013 = slider_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_013.name = "Named Attribute.013"
    named_attribute_013.data_type = 'BOOLEAN'
    # Name
    named_attribute_013.inputs[0].default_value = "was_hit"

    # Set parents
    group_input_1.parent = frame_1
    realize_instances_1.parent = frame_1
    delete_geometry_1.parent = frame_1
    named_attribute_1.parent = frame_1
    boolean_math_1.parent = frame_1
    curve_to_mesh.parent = frame_001
    set_curve_radius.parent = frame_001
    delete_geometry_001_1.parent = frame_1
    named_attribute_001_1.parent = frame_1
    set_material_1.parent = frame_001
    collection_info.parent = frame_002
    realize_instances_001.parent = frame_002
    delete_geometry_002.parent = frame_002
    named_attribute_002_1.parent = frame_002
    boolean_math_001.parent = frame_002
    delete_geometry_003.parent = frame_002
    named_attribute_005.parent = frame_002
    switch.parent = frame_002
    instance_on_points_1.parent = frame_002
    set_position_1.parent = frame_002
    set_position_002.parent = frame_001
    group_input_001_1.parent = frame_003
    group_input_004.parent = frame_002
    group_input_005.parent = frame_002
    group_input_009.parent = frame_003
    group_input_010.parent = frame_001
    set_material_005.parent = frame_002
    group_input_008.parent = frame_002
    set_spline_type.parent = frame_1
    join_geometry_1.parent = frame_001
    mesh_line.parent = frame_001
    mesh_line_001.parent = frame_001
    mesh_to_curve_001.parent = frame_001
    resample_curve.parent = frame_001
    named_attribute_006.parent = frame_001
    attribute_statistic_002.parent = frame_001
    instance_on_points_001_1.parent = frame_006
    named_attribute_004.parent = frame_006
    math_001_1.parent = frame_006
    join_geometry_001.parent = frame_006
    group_input_012.parent = frame_006
    set_material_002.parent = frame_003
    store_named_attribute_003.parent = frame_001
    geometry_proximity.parent = frame_001
    curve_to_mesh_001.parent = frame_001
    mesh_island.parent = frame_001
    merge_by_distance.parent = frame_001
    instance_on_points_002.parent = frame_003
    endpoint_selection.parent = frame_003
    group_input_011.parent = frame_002
    endpoint_selection_001.parent = frame_006
    store_named_attribute_1.parent = frame_003
    store_named_attribute_001.parent = frame_003
    index_001.parent = frame_003
    math_004.parent = frame_003
    compare.parent = frame_003
    compare_001.parent = frame_003
    set_position_001_1.parent = frame_003
    named_attribute_003_1.parent = frame_003
    set_position_003.parent = frame_003
    named_attribute_007.parent = frame_003
    reroute_004_1.parent = frame_006
    split_to_instances.parent = frame_001
    mesh_island_001.parent = frame_001
    store_named_attribute_002.parent = frame_001
    sample_index.parent = frame_001
    named_attribute_008.parent = frame_001
    instance_on_points_003.parent = frame_004
    mesh_circle_1.parent = frame_004
    named_attribute_009.parent = frame_004
    named_attribute_010.parent = frame_004
    compare_002.parent = frame_004
    compare_003.parent = frame_004
    math_003.parent = frame_004
    boolean_math_002.parent = frame_004
    math_008.parent = frame_004
    compare_004.parent = frame_004
    instances_to_points.parent = frame_004
    named_attribute_011.parent = frame_004
    boolean_math_003.parent = frame_004
    boolean_math_004.parent = frame_004
    instance_on_points_004.parent = frame_004
    boolean_math_005.parent = frame_004
    named_attribute_012.parent = frame_004
    boolean_math_006.parent = frame_004
    boolean_math_007.parent = frame_004
    join_geometry_004.parent = frame_004
    set_position_004.parent = frame_004
    set_material_001.parent = frame_004
    delete_geometry_004.parent = frame_006
    named_attribute_013.parent = frame_006

    # Set locations
    group_output_1.location = (5633.376953125, -380.0)
    group_input_1.location = (-682.0, -40.0)
    realize_instances_1.location = (-522.0, -40.0)
    delete_geometry_1.location = (-362.0, -40.0)
    named_attribute_1.location = (-362.0, -220.0)
    boolean_math_1.location = (-362.0, -180.0)
    curve_to_mesh.location = (2790.0, 280.0)
    frame_1.location = (1812.0, -20.0)
    frame_003.location = (204.9776611328125, -311.0)
    set_curve_radius.location = (2470.0, 600.0)
    reroute_001_1.location = (2040.0, -100.0)
    delete_geometry_001_1.location = (-202.0, -40.0)
    named_attribute_001_1.location = (-202.0, -180.0)
    reroute_002_1.location = (2040.0, 540.0)
    set_material_1.location = (3649.99951171875, 280.0)
    collection_info.location = (1050.0, -660.0)
    realize_instances_001.location = (1210.0, -660.0)
    delete_geometry_002.location = (1360.0, -660.0)
    named_attribute_002_1.location = (1360.0, -860.0)
    boolean_math_001.location = (1360.0, -820.0)
    delete_geometry_003.location = (1510.0, -660.0)
    named_attribute_005.location = (1510.0, -820.0)
    switch.location = (2180.0, -660.0)
    instance_on_points_1.location = (1680.0, -660.0)
    set_position_1.location = (2020.0, -660.0)
    set_position_002.location = (3110.0, 280.0)
    group_input_001_1.location = (2680.0, -249.0)
    group_input_004.location = (1050.0, -780.0)
    group_input_005.location = (2180.0, -820.0)
    group_input_009.location = (1720.0, -309.0)
    group_input_010.location = (3650.0, 140.0)
    frame_002.location = (2340.0, -260.0)
    set_material_005.location = (1860.0, -660.0)
    group_input_008.location = (1860.0, -800.0)
    join_geometry_002.location = (5013.37646484375, -240.0)
    join_geometry_003.location = (5433.37646484375, -260.0)
    reroute_013_1.location = (4539.99951171875, 240.0)
    reroute_016.location = (4573.376953125, -320.0)
    set_spline_type.location = (-42.0, -40.0)
    join_geometry_1.location = (2270.0, 0.0)
    mesh_line.location = (2090.0, 340.0)
    mesh_line_001.location = (2090.0, 40.0)
    mesh_to_curve_001.location = (2430.0, 160.0)
    resample_curve.location = (2590.0, 160.0)
    reroute_007_1.location = (4720.0, -960.0)
    reroute_008_1.location = (4720.0, -340.0)
    named_attribute_006.location = (1770.0, 300.0)
    attribute_statistic_002.location = (1770.0, 460.0)
    reroute_009_1.location = (2040.0, 340.0)
    instance_on_points_001_1.location = (3540.0, -440.0)
    named_attribute_004.location = (3220.0, -620.0)
    math_001_1.location = (3380.0, -620.0)
    join_geometry_001.location = (3918.7529296875, -400.0)
    group_input_012.location = (3540.0, -600.0)
    reroute_010_1.location = (4539.99951171875, -280.0)
    reroute_011_1.location = (4573.376953125, -460.0)
    reroute_014_1.location = (2040.0, -340.0)
    frame_006.location = (364.62493896484375, -20.0)
    set_material_002.location = (2680.0, -109.0)
    store_named_attribute_003.location = (2950.0, 280.0)
    geometry_proximity.location = (2790.0, 600.0)
    curve_to_mesh_001.location = (2630.0, 600.0)
    mesh_island.location = (2630.0, 480.0)
    frame_001.location = (370.0, 0.0)
    merge_by_distance.location = (2270.0, 160.0)
    instance_on_points_002.location = (1880.0, -109.0)
    endpoint_selection.location = (1720.0, -189.0)
    group_input_011.location = (1680.0, -780.0)
    endpoint_selection_001.location = (3380.0, -520.0)
    store_named_attribute_1.location = (2040.0, -109.0)
    store_named_attribute_001.location = (2200.0, -109.0)
    index_001.location = (2040.0, -649.0)
    math_004.location = (2040.0, -489.0)
    compare.location = (2200.0, -309.0)
    compare_001.location = (2040.0, -309.0)
    set_position_001_1.location = (2360.0, -109.0)
    named_attribute_003_1.location = (2360.0, -329.0)
    set_position_003.location = (2520.0, -109.0)
    named_attribute_007.location = (2520.0, -329.0)
    reroute_1.location = (2040.0, -480.0)
    reroute_003_1.location = (3600.0, -340.0)
    reroute_004_1.location = (3460.0, -500.0)
    split_to_instances.location = (3289.999755859375, 320.0)
    mesh_island_001.location = (3290.0, 140.0)
    store_named_attribute_002.location = (3469.999755859375, 320.0)
    sample_index.location = (3290.0, 0.0)
    index.location = (3660.0, -200.0)
    named_attribute_008.location = (2950.0, -80.0)
    instance_on_points_003.location = (2620.0, -1360.0)
    mesh_circle_1.location = (1740.0, -1760.0)
    join_geometry_005.location = (3419.6357421875, -427.7689514160156)
    named_attribute_009.location = (1780.0, -2020.0)
    named_attribute_010.location = (1920.0, -1580.0)
    compare_002.location = (2140.0, -1860.0)
    compare_003.location = (2140.0, -2020.0)
    math_003.location = (1980.0, -2020.0)
    boolean_math_002.location = (2300.0, -1860.0)
    math_008.location = (2140.0, -1580.0)
    compare_004.location = (2300.0, -1580.0)
    instances_to_points.location = (2000.0, -1260.0)
    named_attribute_011.location = (2140.0, -1440.0)
    boolean_math_003.location = (2300.0, -1440.0)
    boolean_math_004.location = (2460.0, -1440.0)
    instance_on_points_004.location = (2620.0, -1780.0)
    boolean_math_005.location = (2460.0, -1860.0)
    named_attribute_012.location = (2140.0, -2200.0)
    boolean_math_006.location = (2300.0, -2200.0)
    boolean_math_007.location = (2140.0, -2340.0)
    join_geometry_004.location = (2900.0, -1620.0)
    set_position_004.location = (3060.0, -1620.0)
    frame_004.location = (0.0, 0.0)
    set_material_001.location = (3215.583740234375, -1622.894287109375)
    delete_geometry_004.location = (3739.12744140625, -465.70562744140625)
    named_attribute_013.location = (3731.46630859375, -621.7461547851562)

    # Set dimensions
    group_output_1.width, group_output_1.height = 140.0, 100.0
    group_input_1.width, group_input_1.height = 140.0, 100.0
    realize_instances_1.width, realize_instances_1.height = 140.0, 100.0
    delete_geometry_1.width, delete_geometry_1.height = 140.0, 100.0
    named_attribute_1.width, named_attribute_1.height = 140.0, 100.0
    boolean_math_1.width, boolean_math_1.height = 140.0, 100.0
    curve_to_mesh.width, curve_to_mesh.height = 140.0, 100.0
    frame_1.width, frame_1.height = 840.0, 371.0
    frame_003.width, frame_003.height = 1160.0001220703125, 660.0
    set_curve_radius.width, set_curve_radius.height = 140.0, 100.0
    reroute_001_1.width, reroute_001_1.height = 100.0, 100.0
    delete_geometry_001_1.width, delete_geometry_001_1.height = 140.0, 100.0
    named_attribute_001_1.width, named_attribute_001_1.height = 140.0, 100.0
    reroute_002_1.width, reroute_002_1.height = 100.0, 100.0
    set_material_1.width, set_material_1.height = 140.0, 100.0
    collection_info.width, collection_info.height = 140.0, 100.0
    realize_instances_001.width, realize_instances_001.height = 140.0, 100.0
    delete_geometry_002.width, delete_geometry_002.height = 140.0, 100.0
    named_attribute_002_1.width, named_attribute_002_1.height = 140.0, 100.0
    boolean_math_001.width, boolean_math_001.height = 140.0, 100.0
    delete_geometry_003.width, delete_geometry_003.height = 140.0, 100.0
    named_attribute_005.width, named_attribute_005.height = 140.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    instance_on_points_1.width, instance_on_points_1.height = 140.0, 100.0
    set_position_1.width, set_position_1.height = 140.0, 100.0
    set_position_002.width, set_position_002.height = 140.0, 100.0
    group_input_001_1.width, group_input_001_1.height = 140.0, 100.0
    group_input_004.width, group_input_004.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 140.0, 100.0
    group_input_009.width, group_input_009.height = 140.0, 100.0
    group_input_010.width, group_input_010.height = 140.0, 100.0
    frame_002.width, frame_002.height = 1330.0, 391.0
    set_material_005.width, set_material_005.height = 140.0, 100.0
    group_input_008.width, group_input_008.height = 140.0, 100.0
    join_geometry_002.width, join_geometry_002.height = 140.0, 100.0
    join_geometry_003.width, join_geometry_003.height = 140.0, 100.0
    reroute_013_1.width, reroute_013_1.height = 100.0, 100.0
    reroute_016.width, reroute_016.height = 100.0, 100.0
    set_spline_type.width, set_spline_type.height = 140.0, 100.0
    join_geometry_1.width, join_geometry_1.height = 140.0, 100.0
    mesh_line.width, mesh_line.height = 140.0, 100.0
    mesh_line_001.width, mesh_line_001.height = 140.0, 100.0
    mesh_to_curve_001.width, mesh_to_curve_001.height = 140.0, 100.0
    resample_curve.width, resample_curve.height = 140.0, 100.0
    reroute_007_1.width, reroute_007_1.height = 100.0, 100.0
    reroute_008_1.width, reroute_008_1.height = 100.0, 100.0
    named_attribute_006.width, named_attribute_006.height = 140.0, 100.0
    attribute_statistic_002.width, attribute_statistic_002.height = 140.0, 100.0
    reroute_009_1.width, reroute_009_1.height = 100.0, 100.0
    instance_on_points_001_1.width, instance_on_points_001_1.height = 140.0, 100.0
    named_attribute_004.width, named_attribute_004.height = 140.0, 100.0
    math_001_1.width, math_001_1.height = 140.0, 100.0
    join_geometry_001.width, join_geometry_001.height = 140.0, 100.0
    group_input_012.width, group_input_012.height = 140.0, 100.0
    reroute_010_1.width, reroute_010_1.height = 100.0, 100.0
    reroute_011_1.width, reroute_011_1.height = 100.0, 100.0
    reroute_014_1.width, reroute_014_1.height = 100.0, 100.0
    frame_006.width, frame_006.height = 898.0, 438.0
    set_material_002.width, set_material_002.height = 140.0, 100.0
    store_named_attribute_003.width, store_named_attribute_003.height = 140.0, 100.0
    geometry_proximity.width, geometry_proximity.height = 140.0, 100.0
    curve_to_mesh_001.width, curve_to_mesh_001.height = 140.0, 100.0
    mesh_island.width, mesh_island.height = 140.0, 100.0
    frame_001.width, frame_001.height = 2080.0, 918.0
    merge_by_distance.width, merge_by_distance.height = 140.0, 100.0
    instance_on_points_002.width, instance_on_points_002.height = 140.0, 100.0
    endpoint_selection.width, endpoint_selection.height = 140.0, 100.0
    group_input_011.width, group_input_011.height = 140.0, 100.0
    endpoint_selection_001.width, endpoint_selection_001.height = 140.0, 100.0
    store_named_attribute_1.width, store_named_attribute_1.height = 140.0, 100.0
    store_named_attribute_001.width, store_named_attribute_001.height = 140.0, 100.0
    index_001.width, index_001.height = 140.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    compare_001.width, compare_001.height = 140.0, 100.0
    set_position_001_1.width, set_position_001_1.height = 140.0, 100.0
    named_attribute_003_1.width, named_attribute_003_1.height = 140.0, 100.0
    set_position_003.width, set_position_003.height = 140.0, 100.0
    named_attribute_007.width, named_attribute_007.height = 140.0, 100.0
    reroute_1.width, reroute_1.height = 100.0, 100.0
    reroute_003_1.width, reroute_003_1.height = 100.0, 100.0
    reroute_004_1.width, reroute_004_1.height = 100.0, 100.0
    split_to_instances.width, split_to_instances.height = 140.0, 100.0
    mesh_island_001.width, mesh_island_001.height = 140.0, 100.0
    store_named_attribute_002.width, store_named_attribute_002.height = 140.0, 100.0
    sample_index.width, sample_index.height = 140.0, 100.0
    index.width, index.height = 140.0, 100.0
    named_attribute_008.width, named_attribute_008.height = 140.0, 100.0
    instance_on_points_003.width, instance_on_points_003.height = 140.0, 100.0
    mesh_circle_1.width, mesh_circle_1.height = 140.0, 100.0
    join_geometry_005.width, join_geometry_005.height = 140.0, 100.0
    named_attribute_009.width, named_attribute_009.height = 183.69873046875, 100.0
    named_attribute_010.width, named_attribute_010.height = 209.681640625, 100.0
    compare_002.width, compare_002.height = 140.0, 100.0
    compare_003.width, compare_003.height = 140.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    boolean_math_002.width, boolean_math_002.height = 140.0, 100.0
    math_008.width, math_008.height = 140.0, 100.0
    compare_004.width, compare_004.height = 140.0, 100.0
    instances_to_points.width, instances_to_points.height = 140.0, 100.0
    named_attribute_011.width, named_attribute_011.height = 140.0, 100.0
    boolean_math_003.width, boolean_math_003.height = 140.0, 100.0
    boolean_math_004.width, boolean_math_004.height = 140.0, 100.0
    instance_on_points_004.width, instance_on_points_004.height = 140.0, 100.0
    boolean_math_005.width, boolean_math_005.height = 140.0, 100.0
    named_attribute_012.width, named_attribute_012.height = 140.0, 100.0
    boolean_math_006.width, boolean_math_006.height = 140.0, 100.0
    boolean_math_007.width, boolean_math_007.height = 140.0, 100.0
    join_geometry_004.width, join_geometry_004.height = 140.0, 100.0
    set_position_004.width, set_position_004.height = 140.0, 100.0
    frame_004.width, frame_004.height = 1676.0, 1251.0
    set_material_001.width, set_material_001.height = 140.0, 100.0
    delete_geometry_004.width, delete_geometry_004.height = 140.0, 100.0
    named_attribute_013.width, named_attribute_013.height = 140.0, 100.0

    # initialize slider_sim_group links
    # boolean_math_1.Boolean -> delete_geometry_1.Selection
    slider_sim_group.links.new(boolean_math_1.outputs[0], delete_geometry_1.inputs[1])
    # named_attribute_1.Attribute -> boolean_math_1.Boolean
    slider_sim_group.links.new(named_attribute_1.outputs[0], boolean_math_1.inputs[0])
    # group_input_1.Geometry -> realize_instances_1.Geometry
    slider_sim_group.links.new(group_input_1.outputs[0], realize_instances_1.inputs[0])
    # join_geometry_003.Geometry -> group_output_1.Geometry
    slider_sim_group.links.new(join_geometry_003.outputs[0], group_output_1.inputs[0])
    # reroute_002_1.Output -> set_curve_radius.Curve
    slider_sim_group.links.new(reroute_002_1.outputs[0], set_curve_radius.inputs[0])
    # delete_geometry_1.Geometry -> delete_geometry_001_1.Geometry
    slider_sim_group.links.new(delete_geometry_1.outputs[0], delete_geometry_001_1.inputs[0])
    # named_attribute_001_1.Attribute -> delete_geometry_001_1.Selection
    slider_sim_group.links.new(named_attribute_001_1.outputs[0], delete_geometry_001_1.inputs[1])
    # reroute_009_1.Output -> reroute_002_1.Input
    slider_sim_group.links.new(reroute_009_1.outputs[0], reroute_002_1.inputs[0])
    # store_named_attribute_002.Geometry -> set_material_1.Geometry
    slider_sim_group.links.new(store_named_attribute_002.outputs[0], set_material_1.inputs[0])
    # set_spline_type.Curve -> reroute_001_1.Input
    slider_sim_group.links.new(set_spline_type.outputs[0], reroute_001_1.inputs[0])
    # boolean_math_001.Boolean -> delete_geometry_002.Selection
    slider_sim_group.links.new(boolean_math_001.outputs[0], delete_geometry_002.inputs[1])
    # named_attribute_002_1.Attribute -> boolean_math_001.Boolean
    slider_sim_group.links.new(named_attribute_002_1.outputs[0], boolean_math_001.inputs[0])
    # realize_instances_001.Geometry -> delete_geometry_002.Geometry
    slider_sim_group.links.new(realize_instances_001.outputs[0], delete_geometry_002.inputs[0])
    # delete_geometry_002.Geometry -> delete_geometry_003.Geometry
    slider_sim_group.links.new(delete_geometry_002.outputs[0], delete_geometry_003.inputs[0])
    # named_attribute_005.Attribute -> delete_geometry_003.Selection
    slider_sim_group.links.new(named_attribute_005.outputs[0], delete_geometry_003.inputs[1])
    # set_position_1.Geometry -> switch.True
    slider_sim_group.links.new(set_position_1.outputs[0], switch.inputs[2])
    # collection_info.Instances -> realize_instances_001.Geometry
    slider_sim_group.links.new(collection_info.outputs[0], realize_instances_001.inputs[0])
    # delete_geometry_003.Geometry -> instance_on_points_1.Points
    slider_sim_group.links.new(delete_geometry_003.outputs[0], instance_on_points_1.inputs[0])
    # set_material_005.Geometry -> set_position_1.Geometry
    slider_sim_group.links.new(set_material_005.outputs[0], set_position_1.inputs[0])
    # store_named_attribute_003.Geometry -> set_position_002.Geometry
    slider_sim_group.links.new(store_named_attribute_003.outputs[0], set_position_002.inputs[0])
    # group_input_004.Slider Balls -> collection_info.Collection
    slider_sim_group.links.new(group_input_004.outputs[5], collection_info.inputs[0])
    # group_input_005.Enable Slider Balls -> switch.Switch
    slider_sim_group.links.new(group_input_005.outputs[4], switch.inputs[0])
    # group_input_010.Slider Material -> set_material_1.Material
    slider_sim_group.links.new(group_input_010.outputs[3], set_material_1.inputs[2])
    # instance_on_points_1.Instances -> set_material_005.Geometry
    slider_sim_group.links.new(instance_on_points_1.outputs[0], set_material_005.inputs[0])
    # group_input_008.Slider Balls Material -> set_material_005.Material
    slider_sim_group.links.new(group_input_008.outputs[6], set_material_005.inputs[2])
    # reroute_016.Output -> join_geometry_002.Geometry
    slider_sim_group.links.new(reroute_016.outputs[0], join_geometry_002.inputs[0])
    # reroute_008_1.Output -> join_geometry_003.Geometry
    slider_sim_group.links.new(reroute_008_1.outputs[0], join_geometry_003.inputs[0])
    # set_material_1.Geometry -> reroute_013_1.Input
    slider_sim_group.links.new(set_material_1.outputs[0], reroute_013_1.inputs[0])
    # reroute_011_1.Output -> reroute_016.Input
    slider_sim_group.links.new(reroute_011_1.outputs[0], reroute_016.inputs[0])
    # realize_instances_1.Geometry -> delete_geometry_1.Geometry
    slider_sim_group.links.new(realize_instances_1.outputs[0], delete_geometry_1.inputs[0])
    # set_curve_radius.Curve -> curve_to_mesh.Curve
    slider_sim_group.links.new(set_curve_radius.outputs[0], curve_to_mesh.inputs[0])
    # delete_geometry_001_1.Geometry -> set_spline_type.Curve
    slider_sim_group.links.new(delete_geometry_001_1.outputs[0], set_spline_type.inputs[0])
    # mesh_line.Mesh -> join_geometry_1.Geometry
    slider_sim_group.links.new(mesh_line.outputs[0], join_geometry_1.inputs[0])
    # merge_by_distance.Geometry -> mesh_to_curve_001.Mesh
    slider_sim_group.links.new(merge_by_distance.outputs[0], mesh_to_curve_001.inputs[0])
    # mesh_to_curve_001.Curve -> resample_curve.Curve
    slider_sim_group.links.new(mesh_to_curve_001.outputs[0], resample_curve.inputs[0])
    # resample_curve.Curve -> curve_to_mesh.Profile Curve
    slider_sim_group.links.new(resample_curve.outputs[0], curve_to_mesh.inputs[1])
    # switch.Output -> reroute_007_1.Input
    slider_sim_group.links.new(switch.outputs[0], reroute_007_1.inputs[0])
    # reroute_007_1.Output -> reroute_008_1.Input
    slider_sim_group.links.new(reroute_007_1.outputs[0], reroute_008_1.inputs[0])
    # named_attribute_006.Attribute -> attribute_statistic_002.Attribute
    slider_sim_group.links.new(named_attribute_006.outputs[0], attribute_statistic_002.inputs[2])
    # reroute_001_1.Output -> reroute_009_1.Input
    slider_sim_group.links.new(reroute_001_1.outputs[0], reroute_009_1.inputs[0])
    # reroute_009_1.Output -> attribute_statistic_002.Geometry
    slider_sim_group.links.new(reroute_009_1.outputs[0], attribute_statistic_002.inputs[0])
    # named_attribute_004.Attribute -> math_001_1.Value
    slider_sim_group.links.new(named_attribute_004.outputs[0], math_001_1.inputs[0])
    # math_001_1.Value -> instance_on_points_001_1.Instance Index
    slider_sim_group.links.new(math_001_1.outputs[0], instance_on_points_001_1.inputs[4])
    # group_input_012.Instance -> instance_on_points_001_1.Instance
    slider_sim_group.links.new(group_input_012.outputs[8], instance_on_points_001_1.inputs[2])
    # delete_geometry_004.Geometry -> join_geometry_001.Geometry
    slider_sim_group.links.new(delete_geometry_004.outputs[0], join_geometry_001.inputs[0])
    # reroute_013_1.Output -> reroute_010_1.Input
    slider_sim_group.links.new(reroute_013_1.outputs[0], reroute_010_1.inputs[0])
    # join_geometry_001.Geometry -> reroute_011_1.Input
    slider_sim_group.links.new(join_geometry_001.outputs[0], reroute_011_1.inputs[0])
    # reroute_001_1.Output -> reroute_014_1.Input
    slider_sim_group.links.new(reroute_001_1.outputs[0], reroute_014_1.inputs[0])
    # set_position_003.Geometry -> set_material_002.Geometry
    slider_sim_group.links.new(set_position_003.outputs[0], set_material_002.inputs[0])
    # group_input_001_1.Slider Head/Tail Material -> set_material_002.Material
    slider_sim_group.links.new(group_input_001_1.outputs[7], set_material_002.inputs[2])
    # curve_to_mesh.Mesh -> store_named_attribute_003.Geometry
    slider_sim_group.links.new(curve_to_mesh.outputs[0], store_named_attribute_003.inputs[0])
    # geometry_proximity.Distance -> store_named_attribute_003.Value
    slider_sim_group.links.new(geometry_proximity.outputs[1], store_named_attribute_003.inputs[3])
    # set_curve_radius.Curve -> curve_to_mesh_001.Curve
    slider_sim_group.links.new(set_curve_radius.outputs[0], curve_to_mesh_001.inputs[0])
    # curve_to_mesh_001.Mesh -> geometry_proximity.Geometry
    slider_sim_group.links.new(curve_to_mesh_001.outputs[0], geometry_proximity.inputs[0])
    # mesh_island.Island Index -> geometry_proximity.Sample Group ID
    slider_sim_group.links.new(mesh_island.outputs[0], geometry_proximity.inputs[3])
    # mesh_island.Island Index -> geometry_proximity.Group ID
    slider_sim_group.links.new(mesh_island.outputs[0], geometry_proximity.inputs[1])
    # join_geometry_1.Geometry -> merge_by_distance.Geometry
    slider_sim_group.links.new(join_geometry_1.outputs[0], merge_by_distance.inputs[0])
    # group_input_009.Circle Mesh -> instance_on_points_002.Instance
    slider_sim_group.links.new(group_input_009.outputs[1], instance_on_points_002.inputs[2])
    # reroute_1.Output -> instance_on_points_002.Points
    slider_sim_group.links.new(reroute_1.outputs[0], instance_on_points_002.inputs[0])
    # endpoint_selection.Selection -> instance_on_points_002.Selection
    slider_sim_group.links.new(endpoint_selection.outputs[0], instance_on_points_002.inputs[1])
    # group_input_011.Circle Mesh -> instance_on_points_1.Instance
    slider_sim_group.links.new(group_input_011.outputs[1], instance_on_points_1.inputs[2])
    # reroute_004_1.Output -> instance_on_points_001_1.Points
    slider_sim_group.links.new(reroute_004_1.outputs[0], instance_on_points_001_1.inputs[0])
    # endpoint_selection_001.Selection -> instance_on_points_001_1.Selection
    slider_sim_group.links.new(endpoint_selection_001.outputs[0], instance_on_points_001_1.inputs[1])
    # instance_on_points_002.Instances -> store_named_attribute_1.Geometry
    slider_sim_group.links.new(instance_on_points_002.outputs[0], store_named_attribute_1.inputs[0])
    # store_named_attribute_1.Geometry -> store_named_attribute_001.Geometry
    slider_sim_group.links.new(store_named_attribute_1.outputs[0], store_named_attribute_001.inputs[0])
    # index_001.Index -> math_004.Value
    slider_sim_group.links.new(index_001.outputs[0], math_004.inputs[0])
    # math_004.Value -> compare.A
    slider_sim_group.links.new(math_004.outputs[0], compare.inputs[0])
    # math_004.Value -> compare_001.A
    slider_sim_group.links.new(math_004.outputs[0], compare_001.inputs[0])
    # compare_001.Result -> store_named_attribute_1.Selection
    slider_sim_group.links.new(compare_001.outputs[0], store_named_attribute_1.inputs[1])
    # compare.Result -> store_named_attribute_001.Selection
    slider_sim_group.links.new(compare.outputs[0], store_named_attribute_001.inputs[1])
    # store_named_attribute_001.Geometry -> set_position_001_1.Geometry
    slider_sim_group.links.new(store_named_attribute_001.outputs[0], set_position_001_1.inputs[0])
    # named_attribute_003_1.Attribute -> set_position_001_1.Selection
    slider_sim_group.links.new(named_attribute_003_1.outputs[0], set_position_001_1.inputs[1])
    # set_position_001_1.Geometry -> set_position_003.Geometry
    slider_sim_group.links.new(set_position_001_1.outputs[0], set_position_003.inputs[0])
    # named_attribute_007.Attribute -> set_position_003.Selection
    slider_sim_group.links.new(named_attribute_007.outputs[0], set_position_003.inputs[1])
    # reroute_014_1.Output -> reroute_1.Input
    slider_sim_group.links.new(reroute_014_1.outputs[0], reroute_1.inputs[0])
    # reroute_014_1.Output -> reroute_003_1.Input
    slider_sim_group.links.new(reroute_014_1.outputs[0], reroute_003_1.inputs[0])
    # reroute_003_1.Output -> reroute_004_1.Input
    slider_sim_group.links.new(reroute_003_1.outputs[0], reroute_004_1.inputs[0])
    # set_position_002.Geometry -> split_to_instances.Geometry
    slider_sim_group.links.new(set_position_002.outputs[0], split_to_instances.inputs[0])
    # mesh_island_001.Island Index -> split_to_instances.Group ID
    slider_sim_group.links.new(mesh_island_001.outputs[0], split_to_instances.inputs[2])
    # split_to_instances.Instances -> store_named_attribute_002.Geometry
    slider_sim_group.links.new(split_to_instances.outputs[0], store_named_attribute_002.inputs[0])
    # reroute_003_1.Output -> sample_index.Geometry
    slider_sim_group.links.new(reroute_003_1.outputs[0], sample_index.inputs[0])
    # index.Index -> sample_index.Index
    slider_sim_group.links.new(index.outputs[0], sample_index.inputs[2])
    # named_attribute_008.Attribute -> sample_index.Value
    slider_sim_group.links.new(named_attribute_008.outputs[0], sample_index.inputs[1])
    # sample_index.Value -> store_named_attribute_002.Value
    slider_sim_group.links.new(sample_index.outputs[0], store_named_attribute_002.inputs[3])
    # mesh_circle_1.Mesh -> instance_on_points_003.Instance
    slider_sim_group.links.new(mesh_circle_1.outputs[0], instance_on_points_003.inputs[2])
    # named_attribute_010.Attribute -> compare_002.A
    slider_sim_group.links.new(named_attribute_010.outputs[0], compare_002.inputs[2])
    # named_attribute_010.Attribute -> compare_003.A
    slider_sim_group.links.new(named_attribute_010.outputs[0], compare_003.inputs[2])
    # named_attribute_009.Attribute -> math_003.Value
    slider_sim_group.links.new(named_attribute_009.outputs[0], math_003.inputs[0])
    # compare_002.Result -> boolean_math_002.Boolean
    slider_sim_group.links.new(compare_002.outputs[0], boolean_math_002.inputs[0])
    # compare_003.Result -> boolean_math_002.Boolean
    slider_sim_group.links.new(compare_003.outputs[0], boolean_math_002.inputs[1])
    # math_003.Value -> compare_003.B
    slider_sim_group.links.new(math_003.outputs[0], compare_003.inputs[3])
    # named_attribute_010.Attribute -> math_008.Value
    slider_sim_group.links.new(named_attribute_010.outputs[0], math_008.inputs[0])
    # math_008.Value -> compare_004.A
    slider_sim_group.links.new(math_008.outputs[0], compare_004.inputs[0])
    # store_named_attribute_001.Geometry -> instances_to_points.Instances
    slider_sim_group.links.new(store_named_attribute_001.outputs[0], instances_to_points.inputs[0])
    # instances_to_points.Points -> instance_on_points_003.Points
    slider_sim_group.links.new(instances_to_points.outputs[0], instance_on_points_003.inputs[0])
    # named_attribute_011.Attribute -> boolean_math_003.Boolean
    slider_sim_group.links.new(named_attribute_011.outputs[0], boolean_math_003.inputs[0])
    # compare_004.Result -> boolean_math_003.Boolean
    slider_sim_group.links.new(compare_004.outputs[0], boolean_math_003.inputs[1])
    # boolean_math_002.Boolean -> boolean_math_004.Boolean
    slider_sim_group.links.new(boolean_math_002.outputs[0], boolean_math_004.inputs[0])
    # boolean_math_003.Boolean -> boolean_math_004.Boolean
    slider_sim_group.links.new(boolean_math_003.outputs[0], boolean_math_004.inputs[1])
    # instances_to_points.Points -> instance_on_points_004.Points
    slider_sim_group.links.new(instances_to_points.outputs[0], instance_on_points_004.inputs[0])
    # boolean_math_002.Boolean -> boolean_math_005.Boolean
    slider_sim_group.links.new(boolean_math_002.outputs[0], boolean_math_005.inputs[0])
    # named_attribute_012.Attribute -> boolean_math_006.Boolean
    slider_sim_group.links.new(named_attribute_012.outputs[0], boolean_math_006.inputs[0])
    # compare_004.Result -> boolean_math_007.Boolean
    slider_sim_group.links.new(compare_004.outputs[0], boolean_math_007.inputs[0])
    # boolean_math_007.Boolean -> boolean_math_006.Boolean
    slider_sim_group.links.new(boolean_math_007.outputs[0], boolean_math_006.inputs[1])
    # boolean_math_006.Boolean -> boolean_math_005.Boolean
    slider_sim_group.links.new(boolean_math_006.outputs[0], boolean_math_005.inputs[1])
    # instance_on_points_004.Instances -> join_geometry_004.Geometry
    slider_sim_group.links.new(instance_on_points_004.outputs[0], join_geometry_004.inputs[0])
    # set_material_001.Geometry -> join_geometry_005.Geometry
    slider_sim_group.links.new(set_material_001.outputs[0], join_geometry_005.inputs[0])
    # join_geometry_004.Geometry -> set_position_004.Geometry
    slider_sim_group.links.new(join_geometry_004.outputs[0], set_position_004.inputs[0])
    # mesh_circle_1.Mesh -> instance_on_points_004.Instance
    slider_sim_group.links.new(mesh_circle_1.outputs[0], instance_on_points_004.inputs[2])
    # boolean_math_005.Boolean -> instance_on_points_004.Selection
    slider_sim_group.links.new(boolean_math_005.outputs[0], instance_on_points_004.inputs[1])
    # boolean_math_004.Boolean -> instance_on_points_003.Selection
    slider_sim_group.links.new(boolean_math_004.outputs[0], instance_on_points_003.inputs[1])
    # set_position_004.Geometry -> set_material_001.Geometry
    slider_sim_group.links.new(set_position_004.outputs[0], set_material_001.inputs[0])
    # instance_on_points_001_1.Instances -> delete_geometry_004.Geometry
    slider_sim_group.links.new(instance_on_points_001_1.outputs[0], delete_geometry_004.inputs[0])
    # named_attribute_013.Attribute -> delete_geometry_004.Selection
    slider_sim_group.links.new(named_attribute_013.outputs[0], delete_geometry_004.inputs[1])
    # attribute_statistic_002.Mean -> set_curve_radius.Radius
    slider_sim_group.links.new(attribute_statistic_002.outputs[0], set_curve_radius.inputs[2])
    # reroute_010_1.Output -> join_geometry_002.Geometry
    slider_sim_group.links.new(reroute_010_1.outputs[0], join_geometry_002.inputs[0])
    # join_geometry_002.Geometry -> join_geometry_003.Geometry
    slider_sim_group.links.new(join_geometry_002.outputs[0], join_geometry_003.inputs[0])
    # mesh_line_001.Mesh -> join_geometry_1.Geometry
    slider_sim_group.links.new(mesh_line_001.outputs[0], join_geometry_1.inputs[0])
    # join_geometry_005.Geometry -> join_geometry_001.Geometry
    slider_sim_group.links.new(join_geometry_005.outputs[0], join_geometry_001.inputs[0])
    # set_material_002.Geometry -> join_geometry_005.Geometry
    slider_sim_group.links.new(set_material_002.outputs[0], join_geometry_005.inputs[0])
    # instance_on_points_003.Instances -> join_geometry_004.Geometry
    slider_sim_group.links.new(instance_on_points_003.outputs[0], join_geometry_004.inputs[0])
    return slider_sim_group

# initialize spinner_sim_group node group
def spinner_sim_group_node_group():
    spinner_sim_group = bpy.data.node_groups.new(type='GeometryNodeTree', name="Spinner Sim Group")

    spinner_sim_group.color_tag = 'NONE'
    spinner_sim_group.description = ""

    # spinner_sim_group interface
    # Socket Geometry
    geometry_socket_3 = spinner_sim_group.interface.new_socket(name="Geometry", in_out='OUTPUT',
                                                               socket_type='NodeSocketGeometry')
    geometry_socket_3.attribute_domain = 'POINT'

    # Socket Geometry
    geometry_socket_4 = spinner_sim_group.interface.new_socket(name="Geometry", in_out='INPUT',
                                                               socket_type='NodeSocketGeometry')
    geometry_socket_4.attribute_domain = 'POINT'

    # Socket Scale
    scale_socket = spinner_sim_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    scale_socket.default_value = 1.0
    scale_socket.min_value = 0.0
    scale_socket.max_value = 3.4028234663852886e+38
    scale_socket.subtype = 'NONE'
    scale_socket.attribute_domain = 'POINT'

    # Socket Spinner Material
    spinner_material_socket = spinner_sim_group.interface.new_socket(name="Spinner Material", in_out='INPUT',
                                                                     socket_type='NodeSocketMaterial')
    spinner_material_socket.attribute_domain = 'POINT'

    # Socket Y Offset
    y_offset_socket_1 = spinner_sim_group.interface.new_socket(name="Y Offset", in_out='INPUT',
                                                               socket_type='NodeSocketFloat')
    y_offset_socket_1.default_value = 0.0
    y_offset_socket_1.min_value = -10000.0
    y_offset_socket_1.max_value = 10000.0
    y_offset_socket_1.subtype = 'NONE'
    y_offset_socket_1.attribute_domain = 'POINT'

    # initialize spinner_sim_group nodes
    # node Group Output
    group_output_2 = spinner_sim_group.nodes.new("NodeGroupOutput")
    group_output_2.name = "Group Output"
    group_output_2.is_active_output = True

    # node Group Input
    group_input_2 = spinner_sim_group.nodes.new("NodeGroupInput")
    group_input_2.name = "Group Input"

    # node Realize Instances
    realize_instances_2 = spinner_sim_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_2.name = "Realize Instances"
    # Selection
    realize_instances_2.inputs[1].default_value = True
    # Realize All
    realize_instances_2.inputs[2].default_value = True
    # Depth
    realize_instances_2.inputs[3].default_value = 0

    # node Delete Geometry
    delete_geometry_2 = spinner_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_2.name = "Delete Geometry"
    delete_geometry_2.domain = 'POINT'
    delete_geometry_2.mode = 'ALL'

    # node Named Attribute
    named_attribute_2 = spinner_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_2.name = "Named Attribute"
    named_attribute_2.data_type = 'FLOAT'
    # Name
    named_attribute_2.inputs[0].default_value = "show"

    # node Boolean Math
    boolean_math_2 = spinner_sim_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_2.name = "Boolean Math"
    boolean_math_2.hide = True
    boolean_math_2.operation = 'NOT'

    # node Delete Geometry.001
    delete_geometry_001_2 = spinner_sim_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001_2.name = "Delete Geometry.001"
    delete_geometry_001_2.domain = 'POINT'
    delete_geometry_001_2.mode = 'ALL'

    # node Named Attribute.001
    named_attribute_001_2 = spinner_sim_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001_2.name = "Named Attribute.001"
    named_attribute_001_2.data_type = 'BOOLEAN'
    # Name
    named_attribute_001_2.inputs[0].default_value = "was_completed"

    # node Set Material
    set_material_2 = spinner_sim_group.nodes.new("GeometryNodeSetMaterial")
    set_material_2.name = "Set Material"
    set_material_2.inputs[1].hide = True
    # Selection
    set_material_2.inputs[1].default_value = True

    # node Instance on Points
    instance_on_points_2 = spinner_sim_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_2.name = "Instance on Points"
    instance_on_points_2.inputs[1].hide = True
    instance_on_points_2.inputs[3].hide = True
    instance_on_points_2.inputs[4].hide = True
    instance_on_points_2.inputs[5].hide = True
    instance_on_points_2.inputs[6].hide = True
    # Selection
    instance_on_points_2.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_2.inputs[3].default_value = False
    # Instance Index
    instance_on_points_2.inputs[4].default_value = 0
    # Rotation
    instance_on_points_2.inputs[5].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    instance_on_points_2.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Mesh Circle
    mesh_circle_2 = spinner_sim_group.nodes.new("GeometryNodeMeshCircle")
    mesh_circle_2.name = "Mesh Circle"
    mesh_circle_2.fill_type = 'NGON'
    # Vertices
    mesh_circle_2.inputs[0].default_value = 32

    # node Set Position
    set_position_2 = spinner_sim_group.nodes.new("GeometryNodeSetPosition")
    set_position_2.name = "Set Position"
    set_position_2.inputs[1].hide = True
    set_position_2.inputs[2].hide = True
    # Selection
    set_position_2.inputs[1].default_value = True
    # Position
    set_position_2.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Combine XYZ
    combine_xyz_1 = spinner_sim_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_1.name = "Combine XYZ"
    combine_xyz_1.inputs[0].hide = True
    combine_xyz_1.inputs[2].hide = True
    # X
    combine_xyz_1.inputs[0].default_value = 0.0
    # Z
    combine_xyz_1.inputs[2].default_value = 0.0

    # node Group Input.001
    group_input_001_2 = spinner_sim_group.nodes.new("NodeGroupInput")
    group_input_001_2.name = "Group Input.001"
    group_input_001_2.outputs[0].hide = True
    group_input_001_2.outputs[1].hide = True
    group_input_001_2.outputs[2].hide = True
    group_input_001_2.outputs[4].hide = True

    # node Group Input.002
    group_input_002_1 = spinner_sim_group.nodes.new("NodeGroupInput")
    group_input_002_1.name = "Group Input.002"
    group_input_002_1.outputs[0].hide = True
    group_input_002_1.outputs[1].hide = True
    group_input_002_1.outputs[3].hide = True
    group_input_002_1.outputs[4].hide = True

    # node Group Input.003
    group_input_003_1 = spinner_sim_group.nodes.new("NodeGroupInput")
    group_input_003_1.name = "Group Input.003"
    group_input_003_1.outputs[0].hide = True
    group_input_003_1.outputs[2].hide = True
    group_input_003_1.outputs[3].hide = True
    group_input_003_1.outputs[4].hide = True

    # Set locations
    group_output_2.location = (510.50048828125, 94.5011215209961)
    group_input_2.location = (-600.0, 100.0)
    realize_instances_2.location = (-440.0, 100.0)
    delete_geometry_2.location = (-280.0, 100.0)
    named_attribute_2.location = (-280.0, -100.0)
    boolean_math_2.location = (-280.0, -60.0)
    delete_geometry_001_2.location = (-120.0, 100.0)
    named_attribute_001_2.location = (-120.0, -60.0)
    set_material_2.location = (360.0, 100.0)
    instance_on_points_2.location = (40.0, 100.0)
    mesh_circle_2.location = (40.0, -20.0)
    set_position_2.location = (200.0, 100.0)
    combine_xyz_1.location = (200.0, 0.0)
    group_input_001_2.location = (200.0, -80.0)
    group_input_002_1.location = (360.0, 0.0)
    group_input_003_1.location = (40.0, -160.0)

    # Set dimensions
    group_output_2.width, group_output_2.height = 140.0, 100.0
    group_input_2.width, group_input_2.height = 140.0, 100.0
    realize_instances_2.width, realize_instances_2.height = 140.0, 100.0
    delete_geometry_2.width, delete_geometry_2.height = 140.0, 100.0
    named_attribute_2.width, named_attribute_2.height = 140.0, 100.0
    boolean_math_2.width, boolean_math_2.height = 140.0, 100.0
    delete_geometry_001_2.width, delete_geometry_001_2.height = 140.0, 100.0
    named_attribute_001_2.width, named_attribute_001_2.height = 140.0, 100.0
    set_material_2.width, set_material_2.height = 140.0, 100.0
    instance_on_points_2.width, instance_on_points_2.height = 140.0, 100.0
    mesh_circle_2.width, mesh_circle_2.height = 140.0, 100.0
    set_position_2.width, set_position_2.height = 140.0, 100.0
    combine_xyz_1.width, combine_xyz_1.height = 140.0, 100.0
    group_input_001_2.width, group_input_001_2.height = 140.0, 100.0
    group_input_002_1.width, group_input_002_1.height = 140.0, 100.0
    group_input_003_1.width, group_input_003_1.height = 140.0, 100.0

    # initialize spinner_sim_group links
    # boolean_math_2.Boolean -> delete_geometry_2.Selection
    spinner_sim_group.links.new(boolean_math_2.outputs[0], delete_geometry_2.inputs[1])
    # named_attribute_2.Attribute -> boolean_math_2.Boolean
    spinner_sim_group.links.new(named_attribute_2.outputs[0], boolean_math_2.inputs[0])
    # group_input_2.Geometry -> realize_instances_2.Geometry
    spinner_sim_group.links.new(group_input_2.outputs[0], realize_instances_2.inputs[0])
    # realize_instances_2.Geometry -> delete_geometry_2.Geometry
    spinner_sim_group.links.new(realize_instances_2.outputs[0], delete_geometry_2.inputs[0])
    # set_material_2.Geometry -> group_output_2.Geometry
    spinner_sim_group.links.new(set_material_2.outputs[0], group_output_2.inputs[0])
    # delete_geometry_2.Geometry -> delete_geometry_001_2.Geometry
    spinner_sim_group.links.new(delete_geometry_2.outputs[0], delete_geometry_001_2.inputs[0])
    # named_attribute_001_2.Attribute -> delete_geometry_001_2.Selection
    spinner_sim_group.links.new(named_attribute_001_2.outputs[0], delete_geometry_001_2.inputs[1])
    # set_position_2.Geometry -> set_material_2.Geometry
    spinner_sim_group.links.new(set_position_2.outputs[0], set_material_2.inputs[0])
    # delete_geometry_001_2.Geometry -> instance_on_points_2.Points
    spinner_sim_group.links.new(delete_geometry_001_2.outputs[0], instance_on_points_2.inputs[0])
    # mesh_circle_2.Mesh -> instance_on_points_2.Instance
    spinner_sim_group.links.new(mesh_circle_2.outputs[0], instance_on_points_2.inputs[2])
    # instance_on_points_2.Instances -> set_position_2.Geometry
    spinner_sim_group.links.new(instance_on_points_2.outputs[0], set_position_2.inputs[0])
    # combine_xyz_1.Vector -> set_position_2.Offset
    spinner_sim_group.links.new(combine_xyz_1.outputs[0], set_position_2.inputs[3])
    # group_input_001_2.Y Offset -> combine_xyz_1.Y
    spinner_sim_group.links.new(group_input_001_2.outputs[3], combine_xyz_1.inputs[1])
    # group_input_002_1.Spinner Material -> set_material_2.Material
    spinner_sim_group.links.new(group_input_002_1.outputs[2], set_material_2.inputs[2])
    # group_input_003_1.Scale -> mesh_circle_2.Radius
    spinner_sim_group.links.new(group_input_003_1.outputs[1], mesh_circle_2.inputs[1])
    return spinner_sim_group

# initialize cursor_group node group
def cursor_group_node_group():
    cursor_group = bpy.data.node_groups.new(type='GeometryNodeTree', name="Cursor Group")

    cursor_group.color_tag = 'NONE'
    cursor_group.description = ""

    # cursor_group interface
    # Socket Geometry
    geometry_socket_5 = cursor_group.interface.new_socket(name="Geometry", in_out='OUTPUT',
                                                          socket_type='NodeSocketGeometry')
    geometry_socket_5.attribute_domain = 'POINT'

    # Socket Points
    points_socket = cursor_group.interface.new_socket(name="Points", in_out='INPUT', socket_type='NodeSocketGeometry')
    points_socket.attribute_domain = 'POINT'

    # Socket Cursor Material
    cursor_material_socket = cursor_group.interface.new_socket(name="Cursor Material", in_out='INPUT',
                                                               socket_type='NodeSocketMaterial')
    cursor_material_socket.attribute_domain = 'POINT'

    # Socket Y Offset
    y_offset_socket_2 = cursor_group.interface.new_socket(name="Y Offset", in_out='INPUT',
                                                          socket_type='NodeSocketFloat')
    y_offset_socket_2.default_value = 0.0
    y_offset_socket_2.min_value = -10000.0
    y_offset_socket_2.max_value = 10000.0
    y_offset_socket_2.subtype = 'NONE'
    y_offset_socket_2.attribute_domain = 'POINT'

    # initialize cursor_group nodes
    # node Group Output
    group_output_3 = cursor_group.nodes.new("NodeGroupOutput")
    group_output_3.name = "Group Output"
    group_output_3.is_active_output = True

    # node Group Input
    group_input_3 = cursor_group.nodes.new("NodeGroupInput")
    group_input_3.name = "Group Input"

    # node Instance on Points
    instance_on_points_3 = cursor_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_3.name = "Instance on Points"
    instance_on_points_3.inputs[1].hide = True
    instance_on_points_3.inputs[3].hide = True
    instance_on_points_3.inputs[4].hide = True
    instance_on_points_3.inputs[5].hide = True
    instance_on_points_3.inputs[6].hide = True
    # Selection
    instance_on_points_3.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_3.inputs[3].default_value = False
    # Instance Index
    instance_on_points_3.inputs[4].default_value = 0
    # Rotation
    instance_on_points_3.inputs[5].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    instance_on_points_3.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Mesh Circle
    mesh_circle_3 = cursor_group.nodes.new("GeometryNodeMeshCircle")
    mesh_circle_3.name = "Mesh Circle"
    mesh_circle_3.fill_type = 'NGON'
    # Vertices
    mesh_circle_3.inputs[0].default_value = 32

    # node Set Material
    set_material_3 = cursor_group.nodes.new("GeometryNodeSetMaterial")
    set_material_3.name = "Set Material"
    set_material_3.inputs[1].hide = True
    # Selection
    set_material_3.inputs[1].default_value = True

    # node Set Position
    set_position_3 = cursor_group.nodes.new("GeometryNodeSetPosition")
    set_position_3.name = "Set Position"
    set_position_3.inputs[1].hide = True
    set_position_3.inputs[2].hide = True
    # Selection
    set_position_3.inputs[1].default_value = True
    # Position
    set_position_3.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Combine XYZ
    combine_xyz_2 = cursor_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_2.name = "Combine XYZ"
    combine_xyz_2.inputs[0].hide = True
    combine_xyz_2.inputs[2].hide = True
    # X
    combine_xyz_2.inputs[0].default_value = 0.0
    # Z
    combine_xyz_2.inputs[2].default_value = 0.0

    # node Group Input.001
    group_input_001_3 = cursor_group.nodes.new("NodeGroupInput")
    group_input_001_3.name = "Group Input.001"
    group_input_001_3.outputs[0].hide = True
    group_input_001_3.outputs[1].hide = True
    group_input_001_3.outputs[3].hide = True

    # node Group Input.002
    group_input_002_2 = cursor_group.nodes.new("NodeGroupInput")
    group_input_002_2.name = "Group Input.002"
    group_input_002_2.outputs[0].hide = True
    group_input_002_2.outputs[2].hide = True
    group_input_002_2.outputs[3].hide = True

    # node Realize Instances
    realize_instances_3 = cursor_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_3.name = "Realize Instances"
    # Selection
    realize_instances_3.inputs[1].default_value = True
    # Realize All
    realize_instances_3.inputs[2].default_value = True
    # Depth
    realize_instances_3.inputs[3].default_value = 0

    # node Named Attribute
    named_attribute_3 = cursor_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_3.name = "Named Attribute"
    named_attribute_3.data_type = 'FLOAT'
    # Name
    named_attribute_3.inputs[0].default_value = "cursor_size"

    # node Attribute Statistic
    attribute_statistic_1 = cursor_group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_1.name = "Attribute Statistic"
    attribute_statistic_1.data_type = 'FLOAT'
    attribute_statistic_1.domain = 'POINT'
    # Selection
    attribute_statistic_1.inputs[1].default_value = True

    # Set locations
    group_output_3.location = (480.0, -60.0)
    group_input_3.location = (-320.0, -60.0)
    instance_on_points_3.location = (0.0, -60.0)
    mesh_circle_3.location = (0.0, -160.0)
    set_material_3.location = (320.0, -60.0)
    set_position_3.location = (160.0, -60.0)
    combine_xyz_2.location = (160.0, -160.0)
    group_input_001_3.location = (160.0, -240.0)
    group_input_002_2.location = (320.0, -160.0)
    realize_instances_3.location = (-160.0, -60.0)
    named_attribute_3.location = (-320.0, -220.0)
    attribute_statistic_1.location = (-160.0, -220.0)

    # Set dimensions
    group_output_3.width, group_output_3.height = 140.0, 100.0
    group_input_3.width, group_input_3.height = 140.0, 100.0
    instance_on_points_3.width, instance_on_points_3.height = 140.0, 100.0
    mesh_circle_3.width, mesh_circle_3.height = 140.0, 100.0
    set_material_3.width, set_material_3.height = 140.0, 100.0
    set_position_3.width, set_position_3.height = 140.0, 100.0
    combine_xyz_2.width, combine_xyz_2.height = 140.0, 100.0
    group_input_001_3.width, group_input_001_3.height = 140.0, 100.0
    group_input_002_2.width, group_input_002_2.height = 140.0, 100.0
    realize_instances_3.width, realize_instances_3.height = 140.0, 100.0
    named_attribute_3.width, named_attribute_3.height = 140.0, 100.0
    attribute_statistic_1.width, attribute_statistic_1.height = 140.0, 100.0

    # initialize cursor_group links
    # mesh_circle_3.Mesh -> instance_on_points_3.Instance
    cursor_group.links.new(mesh_circle_3.outputs[0], instance_on_points_3.inputs[2])
    # set_position_3.Geometry -> set_material_3.Geometry
    cursor_group.links.new(set_position_3.outputs[0], set_material_3.inputs[0])
    # realize_instances_3.Geometry -> instance_on_points_3.Points
    cursor_group.links.new(realize_instances_3.outputs[0], instance_on_points_3.inputs[0])
    # set_material_3.Geometry -> group_output_3.Geometry
    cursor_group.links.new(set_material_3.outputs[0], group_output_3.inputs[0])
    # instance_on_points_3.Instances -> set_position_3.Geometry
    cursor_group.links.new(instance_on_points_3.outputs[0], set_position_3.inputs[0])
    # combine_xyz_2.Vector -> set_position_3.Offset
    cursor_group.links.new(combine_xyz_2.outputs[0], set_position_3.inputs[3])
    # group_input_001_3.Y Offset -> combine_xyz_2.Y
    cursor_group.links.new(group_input_001_3.outputs[2], combine_xyz_2.inputs[1])
    # group_input_002_2.Cursor Material -> set_material_3.Material
    cursor_group.links.new(group_input_002_2.outputs[1], set_material_3.inputs[2])
    # group_input_3.Points -> realize_instances_3.Geometry
    cursor_group.links.new(group_input_3.outputs[0], realize_instances_3.inputs[0])
    # named_attribute_3.Attribute -> attribute_statistic_1.Attribute
    cursor_group.links.new(named_attribute_3.outputs[0], attribute_statistic_1.inputs[2])
    # realize_instances_3.Geometry -> attribute_statistic_1.Geometry
    cursor_group.links.new(realize_instances_3.outputs[0], attribute_statistic_1.inputs[0])
    # attribute_statistic_1.Mean -> mesh_circle_3.Radius
    cursor_group.links.new(attribute_statistic_1.outputs[0], mesh_circle_3.inputs[1])
    return cursor_group

# initialize approach_circle_group node group
def approach_circle_group_node_group():
    approach_circle_group = bpy.data.node_groups.new(type='GeometryNodeTree', name="Approach Circle Group")

    approach_circle_group.color_tag = 'NONE'
    approach_circle_group.description = ""

    # approach_circle_group interface
    # Socket Instances
    instances_socket = approach_circle_group.interface.new_socket(name="Instances", in_out='OUTPUT',
                                                                  socket_type='NodeSocketGeometry')
    instances_socket.attribute_domain = 'POINT'

    # Socket Geometry
    geometry_socket_6 = approach_circle_group.interface.new_socket(name="Geometry", in_out='INPUT',
                                                                   socket_type='NodeSocketGeometry')
    geometry_socket_6.attribute_domain = 'POINT'

    # Socket Y Offset
    y_offset_socket_3 = approach_circle_group.interface.new_socket(name="Y Offset", in_out='INPUT',
                                                                   socket_type='NodeSocketFloat')
    y_offset_socket_3.default_value = 0.0
    y_offset_socket_3.min_value = -10000.0
    y_offset_socket_3.max_value = 10000.0
    y_offset_socket_3.subtype = 'NONE'
    y_offset_socket_3.attribute_domain = 'POINT'

    # Socket Approach Circle Material
    approach_circle_material_socket = approach_circle_group.interface.new_socket(name="Approach Circle Material",
                                                                                 in_out='INPUT',
                                                                                 socket_type='NodeSocketMaterial')
    approach_circle_material_socket.attribute_domain = 'POINT'

    # initialize approach_circle_group nodes
    # node Group Output
    group_output_4 = approach_circle_group.nodes.new("NodeGroupOutput")
    group_output_4.name = "Group Output"
    group_output_4.is_active_output = True

    # node Group Input
    group_input_4 = approach_circle_group.nodes.new("NodeGroupInput")
    group_input_4.name = "Group Input"
    group_input_4.outputs[1].hide = True
    group_input_4.outputs[2].hide = True
    group_input_4.outputs[3].hide = True

    # node Instance on Points
    instance_on_points_4 = approach_circle_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_4.name = "Instance on Points"
    instance_on_points_4.inputs[1].hide = True
    instance_on_points_4.inputs[3].hide = True
    instance_on_points_4.inputs[4].hide = True
    instance_on_points_4.inputs[5].hide = True
    # Selection
    instance_on_points_4.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_4.inputs[3].default_value = False
    # Instance Index
    instance_on_points_4.inputs[4].default_value = 0
    # Rotation
    instance_on_points_4.inputs[5].default_value = (1.5707963705062866, 0.0, 0.0)

    # node Named Attribute
    named_attribute_4 = approach_circle_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_4.name = "Named Attribute"
    named_attribute_4.data_type = 'FLOAT'
    # Name
    named_attribute_4.inputs[0].default_value = "scale"

    # node Delete Geometry
    delete_geometry_3 = approach_circle_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_3.name = "Delete Geometry"
    delete_geometry_3.domain = 'POINT'
    delete_geometry_3.mode = 'ALL'

    # node Named Attribute.001
    named_attribute_001_3 = approach_circle_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001_3.name = "Named Attribute.001"
    named_attribute_001_3.data_type = 'BOOLEAN'
    # Name
    named_attribute_001_3.inputs[0].default_value = "show"

    # node Boolean Math
    boolean_math_3 = approach_circle_group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_3.name = "Boolean Math"
    boolean_math_3.hide = True
    boolean_math_3.operation = 'NOT'

    # node Named Attribute.002
    named_attribute_002_2 = approach_circle_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002_2.name = "Named Attribute.002"
    named_attribute_002_2.data_type = 'FLOAT'
    # Name
    named_attribute_002_2.inputs[0].default_value = "cs"

    # node Mesh Circle
    mesh_circle_4 = approach_circle_group.nodes.new("GeometryNodeMeshCircle")
    mesh_circle_4.name = "Mesh Circle"
    mesh_circle_4.fill_type = 'NONE'
    # Vertices
    mesh_circle_4.inputs[0].default_value = 32

    # node Extrude Mesh
    extrude_mesh = approach_circle_group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.mode = 'EDGES'
    # Selection
    extrude_mesh.inputs[1].default_value = True
    # Offset
    extrude_mesh.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Realize Instances
    realize_instances_4 = approach_circle_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_4.name = "Realize Instances"
    # Selection
    realize_instances_4.inputs[1].default_value = True
    # Realize All
    realize_instances_4.inputs[2].default_value = True
    # Depth
    realize_instances_4.inputs[3].default_value = 0

    # node Attribute Statistic
    attribute_statistic_2 = approach_circle_group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_2.name = "Attribute Statistic"
    attribute_statistic_2.hide = True
    attribute_statistic_2.data_type = 'FLOAT'
    attribute_statistic_2.domain = 'POINT'
    # Selection
    attribute_statistic_2.inputs[1].default_value = True

    # node Map Range
    map_range = approach_circle_group.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    # From Min
    map_range.inputs[1].default_value = 1.0
    # From Max
    map_range.inputs[2].default_value = 5.0
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 0.09999999403953552

    # node Set Position
    set_position_4 = approach_circle_group.nodes.new("GeometryNodeSetPosition")
    set_position_4.name = "Set Position"
    # Selection
    set_position_4.inputs[1].default_value = True
    # Position
    set_position_4.inputs[2].default_value = (0.0, 0.0, 0.0)

    # node Combine XYZ
    combine_xyz_3 = approach_circle_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_3.name = "Combine XYZ"
    # X
    combine_xyz_3.inputs[0].default_value = 0.0
    # Z
    combine_xyz_3.inputs[2].default_value = 0.0

    # node Set Material
    set_material_4 = approach_circle_group.nodes.new("GeometryNodeSetMaterial")
    set_material_4.name = "Set Material"
    # Selection
    set_material_4.inputs[1].default_value = True

    # node Attribute Statistic.001
    attribute_statistic_001_1 = approach_circle_group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001_1.name = "Attribute Statistic.001"
    attribute_statistic_001_1.data_type = 'FLOAT'
    attribute_statistic_001_1.domain = 'POINT'
    attribute_statistic_001_1.inputs[1].hide = True
    attribute_statistic_001_1.outputs[1].hide = True
    attribute_statistic_001_1.outputs[2].hide = True
    attribute_statistic_001_1.outputs[3].hide = True
    attribute_statistic_001_1.outputs[4].hide = True
    attribute_statistic_001_1.outputs[5].hide = True
    attribute_statistic_001_1.outputs[6].hide = True
    attribute_statistic_001_1.outputs[7].hide = True
    # Selection
    attribute_statistic_001_1.inputs[1].default_value = True

    # node Reroute
    reroute_2 = approach_circle_group.nodes.new("NodeReroute")
    reroute_2.name = "Reroute"
    # node Reroute.001
    reroute_001_2 = approach_circle_group.nodes.new("NodeReroute")
    reroute_001_2.name = "Reroute.001"
    # node Reroute.002
    reroute_002_2 = approach_circle_group.nodes.new("NodeReroute")
    reroute_002_2.name = "Reroute.002"
    # node Reroute.003
    reroute_003_2 = approach_circle_group.nodes.new("NodeReroute")
    reroute_003_2.name = "Reroute.003"
    # node Reroute.004
    reroute_004_2 = approach_circle_group.nodes.new("NodeReroute")
    reroute_004_2.name = "Reroute.004"
    # node Group Input.001
    group_input_001_4 = approach_circle_group.nodes.new("NodeGroupInput")
    group_input_001_4.name = "Group Input.001"
    group_input_001_4.outputs[0].hide = True
    group_input_001_4.outputs[1].hide = True
    group_input_001_4.outputs[3].hide = True

    # node Group Input.002
    group_input_002_3 = approach_circle_group.nodes.new("NodeGroupInput")
    group_input_002_3.name = "Group Input.002"
    group_input_002_3.outputs[0].hide = True
    group_input_002_3.outputs[2].hide = True
    group_input_002_3.outputs[3].hide = True

    # node Math
    math = approach_circle_group.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 2.0

    # Set locations
    group_output_4.location = (1140.0, 220.0)
    group_input_4.location = (-760.0, 220.1756591796875)
    instance_on_points_4.location = (660.0, 220.0)
    named_attribute_4.location = (40.0, -180.0)
    delete_geometry_3.location = (-440.0, 220.1756591796875)
    named_attribute_001_3.location = (-440.0, 20.1756591796875)
    boolean_math_3.location = (-440.0, 60.1756591796875)
    named_attribute_002_2.location = (-200.0, -60.0)
    mesh_circle_4.location = (458.61968994140625, -134.40338134765625)
    extrude_mesh.location = (460.0, -280.0)
    realize_instances_4.location = (-600.0, 220.1756591796875)
    attribute_statistic_2.location = (280.0, -420.0)
    map_range.location = (280.0, -140.0)
    set_position_4.location = (820.0, 220.0)
    combine_xyz_3.location = (820.0, 60.0)
    set_material_4.location = (980.0, 220.0)
    attribute_statistic_001_1.location = (-200.0, 100.0)
    reroute_2.location = (-260.0, 180.1756591796875)
    reroute_001_2.location = (-260.0, 0.1756591796875)
    reroute_002_2.location = (-260.0, -399.8243408203125)
    reroute_003_2.location = (620.0, -320.0)
    reroute_004_2.location = (620.0, 140.0)
    group_input_001_4.location = (980.0, 80.0)
    group_input_002_3.location = (820.0, -80.0)
    math.location = (-43.1097412109375, 106.15355682373047)

    # Set dimensions
    group_output_4.width, group_output_4.height = 140.0, 100.0
    group_input_4.width, group_input_4.height = 140.0, 100.0
    instance_on_points_4.width, instance_on_points_4.height = 140.0, 100.0
    named_attribute_4.width, named_attribute_4.height = 140.0, 100.0
    delete_geometry_3.width, delete_geometry_3.height = 140.0, 100.0
    named_attribute_001_3.width, named_attribute_001_3.height = 140.0, 100.0
    boolean_math_3.width, boolean_math_3.height = 140.0, 100.0
    named_attribute_002_2.width, named_attribute_002_2.height = 140.0, 100.0
    mesh_circle_4.width, mesh_circle_4.height = 140.0, 100.0
    extrude_mesh.width, extrude_mesh.height = 140.0, 100.0
    realize_instances_4.width, realize_instances_4.height = 140.0, 100.0
    attribute_statistic_2.width, attribute_statistic_2.height = 140.0, 100.0
    map_range.width, map_range.height = 140.0, 100.0
    set_position_4.width, set_position_4.height = 140.0, 100.0
    combine_xyz_3.width, combine_xyz_3.height = 140.0, 100.0
    set_material_4.width, set_material_4.height = 140.0, 100.0
    attribute_statistic_001_1.width, attribute_statistic_001_1.height = 140.0, 100.0
    reroute_2.width, reroute_2.height = 16.0, 100.0
    reroute_001_2.width, reroute_001_2.height = 16.0, 100.0
    reroute_002_2.width, reroute_002_2.height = 16.0, 100.0
    reroute_003_2.width, reroute_003_2.height = 16.0, 100.0
    reroute_004_2.width, reroute_004_2.height = 16.0, 100.0
    group_input_001_4.width, group_input_001_4.height = 140.0, 100.0
    group_input_002_3.width, group_input_002_3.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0

    # initialize approach_circle_group links
    # named_attribute_001_3.Attribute -> boolean_math_3.Boolean
    approach_circle_group.links.new(named_attribute_001_3.outputs[0], boolean_math_3.inputs[0])
    # boolean_math_3.Boolean -> delete_geometry_3.Selection
    approach_circle_group.links.new(boolean_math_3.outputs[0], delete_geometry_3.inputs[1])
    # reroute_2.Output -> instance_on_points_4.Points
    approach_circle_group.links.new(reroute_2.outputs[0], instance_on_points_4.inputs[0])
    # realize_instances_4.Geometry -> delete_geometry_3.Geometry
    approach_circle_group.links.new(realize_instances_4.outputs[0], delete_geometry_3.inputs[0])
    # mesh_circle_4.Mesh -> extrude_mesh.Mesh
    approach_circle_group.links.new(mesh_circle_4.outputs[0], extrude_mesh.inputs[0])
    # reroute_004_2.Output -> instance_on_points_4.Instance
    approach_circle_group.links.new(reroute_004_2.outputs[0], instance_on_points_4.inputs[2])
    # group_input_4.Geometry -> realize_instances_4.Geometry
    approach_circle_group.links.new(group_input_4.outputs[0], realize_instances_4.inputs[0])
    # named_attribute_4.Attribute -> attribute_statistic_2.Attribute
    approach_circle_group.links.new(named_attribute_4.outputs[0], attribute_statistic_2.inputs[2])
    # attribute_statistic_2.Mean -> map_range.Value
    approach_circle_group.links.new(attribute_statistic_2.outputs[0], map_range.inputs[0])
    # map_range.Result -> extrude_mesh.Offset Scale
    approach_circle_group.links.new(map_range.outputs[0], extrude_mesh.inputs[3])
    # set_material_4.Geometry -> group_output_4.Instances
    approach_circle_group.links.new(set_material_4.outputs[0], group_output_4.inputs[0])
    # instance_on_points_4.Instances -> set_position_4.Geometry
    approach_circle_group.links.new(instance_on_points_4.outputs[0], set_position_4.inputs[0])
    # combine_xyz_3.Vector -> set_position_4.Offset
    approach_circle_group.links.new(combine_xyz_3.outputs[0], set_position_4.inputs[3])
    # set_position_4.Geometry -> set_material_4.Geometry
    approach_circle_group.links.new(set_position_4.outputs[0], set_material_4.inputs[0])
    # named_attribute_002_2.Attribute -> attribute_statistic_001_1.Attribute
    approach_circle_group.links.new(named_attribute_002_2.outputs[0], attribute_statistic_001_1.inputs[2])
    # reroute_001_2.Output -> attribute_statistic_001_1.Geometry
    approach_circle_group.links.new(reroute_001_2.outputs[0], attribute_statistic_001_1.inputs[0])
    # delete_geometry_3.Geometry -> reroute_2.Input
    approach_circle_group.links.new(delete_geometry_3.outputs[0], reroute_2.inputs[0])
    # reroute_2.Output -> reroute_001_2.Input
    approach_circle_group.links.new(reroute_2.outputs[0], reroute_001_2.inputs[0])
    # reroute_002_2.Output -> attribute_statistic_2.Geometry
    approach_circle_group.links.new(reroute_002_2.outputs[0], attribute_statistic_2.inputs[0])
    # reroute_001_2.Output -> reroute_002_2.Input
    approach_circle_group.links.new(reroute_001_2.outputs[0], reroute_002_2.inputs[0])
    # extrude_mesh.Mesh -> reroute_003_2.Input
    approach_circle_group.links.new(extrude_mesh.outputs[0], reroute_003_2.inputs[0])
    # reroute_003_2.Output -> reroute_004_2.Input
    approach_circle_group.links.new(reroute_003_2.outputs[0], reroute_004_2.inputs[0])
    # group_input_001_4.Approach Circle Material -> set_material_4.Material
    approach_circle_group.links.new(group_input_001_4.outputs[2], set_material_4.inputs[2])
    # group_input_002_3.Y Offset -> combine_xyz_3.Y
    approach_circle_group.links.new(group_input_002_3.outputs[1], combine_xyz_3.inputs[1])
    # attribute_statistic_001_1.Mean -> math.Value
    approach_circle_group.links.new(attribute_statistic_001_1.outputs[0], math.inputs[0])
    # math.Value -> mesh_circle_4.Radius
    approach_circle_group.links.new(math.outputs[0], mesh_circle_4.inputs[1])
    # named_attribute_4.Attribute -> instance_on_points_4.Scale
    approach_circle_group.links.new(named_attribute_4.outputs[0], instance_on_points_4.inputs[6])
    return approach_circle_group

# initialize combo node group
def combo_node_group():
    combo = bpy.data.node_groups.new(type='GeometryNodeTree', name="Combo")

    combo.color_tag = 'NONE'
    combo.description = ""

    # combo interface
    # Socket Geometry
    geometry_socket_7 = combo.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket_7.attribute_domain = 'POINT'

    # Socket Size
    size_socket = combo.interface.new_socket(name="Size", in_out='INPUT', socket_type='NodeSocketFloat')
    size_socket.default_value = 1.0
    size_socket.min_value = -3.4028234663852886e+38
    size_socket.max_value = 3.4028234663852886e+38
    size_socket.subtype = 'NONE'
    size_socket.attribute_domain = 'POINT'

    # initialize combo nodes
    # node Group Output
    group_output_5 = combo.nodes.new("NodeGroupOutput")
    group_output_5.name = "Group Output"
    group_output_5.is_active_output = True

    # node Group Input
    group_input_5 = combo.nodes.new("NodeGroupInput")
    group_input_5.name = "Group Input"

    # node Repeat Input
    repeat_input = combo.nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    # node Repeat Output
    repeat_output = combo.nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    repeat_output.repeat_items.clear()
    # Create item "Geometry"
    repeat_output.repeat_items.new('GEOMETRY', "Geometry")
    # Create item "Integer"
    repeat_output.repeat_items.new('INT', "Integer")

    # node Math
    math_1 = combo.nodes.new("ShaderNodeMath")
    math_1.name = "Math"
    math_1.operation = 'ADD'
    math_1.use_clamp = False
    # Value_001
    math_1.inputs[1].default_value = 1.0

    # node Value to String
    value_to_string = combo.nodes.new("FunctionNodeValueToString")
    value_to_string.name = "Value to String"
    # Decimals
    value_to_string.inputs[1].default_value = 0

    # node Sort Elements
    sort_elements = combo.nodes.new("GeometryNodeSortElements")
    sort_elements.name = "Sort Elements"
    sort_elements.domain = 'INSTANCE'
    # Selection
    sort_elements.inputs[1].default_value = True
    # Sort Weight
    sort_elements.inputs[3].default_value = 0.0

    # node Named Attribute
    named_attribute_5 = combo.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_5.name = "Named Attribute"
    named_attribute_5.data_type = 'FLOAT'
    # Name
    named_attribute_5.inputs[0].default_value = "combo_str"

    # node Fill Curve
    fill_curve = combo.nodes.new("GeometryNodeFillCurve")
    fill_curve.name = "Fill Curve"
    fill_curve.mode = 'NGONS'
    # Group ID
    fill_curve.inputs[1].default_value = 0

    # node String to Curves.001
    string_to_curves_001 = combo.nodes.new("GeometryNodeStringToCurves")
    string_to_curves_001.name = "String to Curves.001"
    string_to_curves_001.align_x = 'CENTER'
    string_to_curves_001.align_y = 'MIDDLE'
    string_to_curves_001.overflow = 'OVERFLOW'
    string_to_curves_001.pivot_mode = 'BOTTOM_LEFT'
    # Character Spacing
    string_to_curves_001.inputs[2].default_value = 1.0
    # Word Spacing
    string_to_curves_001.inputs[3].default_value = 1.0
    # Line Spacing
    string_to_curves_001.inputs[4].default_value = 1.0
    # Text Box Width
    string_to_curves_001.inputs[5].default_value = 0.0

    # node Store Named Attribute.001
    store_named_attribute_001_1 = combo.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001_1.name = "Store Named Attribute.001"
    store_named_attribute_001_1.data_type = 'FLOAT'
    store_named_attribute_001_1.domain = 'INSTANCE'
    # Selection
    store_named_attribute_001_1.inputs[1].default_value = True
    # Name
    store_named_attribute_001_1.inputs[2].default_value = "combo_str"

    # node Join Geometry
    join_geometry_2 = combo.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_2.name = "Join Geometry"

    # Process zone input Repeat Input
    repeat_input.pair_with_output(repeat_output)
    # Iterations
    repeat_input.inputs[0].default_value = 9
    # Item_2
    repeat_input.inputs[2].default_value = 0

    # Set locations
    group_output_5.location = (1120.0, -40.0)
    group_input_5.location = (-580.0, -260.0)
    repeat_input.location = (-900.0, -40.0)
    repeat_output.location = (100.0, -40.0)
    math_1.location = (-740.0, -40.0)
    value_to_string.location = (-580.0, -100.0)
    sort_elements.location = (420.0, -40.0)
    named_attribute_5.location = (260.0, -180.0)
    fill_curve.location = (260.0, -40.0)
    string_to_curves_001.location = (-420.0, -40.0)
    store_named_attribute_001_1.location = (-220.0, -40.0)
    join_geometry_2.location = (-60.0, -40.0)

    # Set dimensions
    group_output_5.width, group_output_5.height = 140.0, 100.0
    group_input_5.width, group_input_5.height = 140.0, 100.0
    repeat_input.width, repeat_input.height = 140.0, 100.0
    repeat_output.width, repeat_output.height = 140.0, 100.0
    math_1.width, math_1.height = 140.0, 100.0
    value_to_string.width, value_to_string.height = 140.0, 100.0
    sort_elements.width, sort_elements.height = 140.0, 100.0
    named_attribute_5.width, named_attribute_5.height = 140.0, 100.0
    fill_curve.width, fill_curve.height = 140.0, 100.0
    string_to_curves_001.width, string_to_curves_001.height = 190.0, 100.0
    store_named_attribute_001_1.width, store_named_attribute_001_1.height = 140.0, 100.0
    join_geometry_2.width, join_geometry_2.height = 140.0, 100.0

    # initialize combo links
    # math_1.Value -> value_to_string.Value
    combo.links.new(math_1.outputs[0], value_to_string.inputs[0])
    # math_1.Value -> repeat_output.Integer
    combo.links.new(math_1.outputs[0], repeat_output.inputs[1])
    # repeat_output.Geometry -> fill_curve.Curve
    combo.links.new(repeat_output.outputs[0], fill_curve.inputs[0])
    # repeat_input.Integer -> math_1.Value
    combo.links.new(repeat_input.outputs[1], math_1.inputs[0])
    # fill_curve.Mesh -> sort_elements.Geometry
    combo.links.new(fill_curve.outputs[0], sort_elements.inputs[0])
    # sort_elements.Geometry -> group_output_5.Geometry
    combo.links.new(sort_elements.outputs[0], group_output_5.inputs[0])
    # string_to_curves_001.Curve Instances -> store_named_attribute_001_1.Geometry
    combo.links.new(string_to_curves_001.outputs[0], store_named_attribute_001_1.inputs[0])
    # value_to_string.String -> string_to_curves_001.String
    combo.links.new(value_to_string.outputs[0], string_to_curves_001.inputs[0])
    # join_geometry_2.Geometry -> repeat_output.Geometry
    combo.links.new(join_geometry_2.outputs[0], repeat_output.inputs[0])
    # repeat_input.Geometry -> join_geometry_2.Geometry
    combo.links.new(repeat_input.outputs[0], join_geometry_2.inputs[0])
    # group_input_5.Size -> string_to_curves_001.Size
    combo.links.new(group_input_5.outputs[0], string_to_curves_001.inputs[1])
    # named_attribute_5.Attribute -> sort_elements.Group ID
    combo.links.new(named_attribute_5.outputs[0], sort_elements.inputs[2])
    # math_1.Value -> store_named_attribute_001_1.Value
    combo.links.new(math_1.outputs[0], store_named_attribute_001_1.inputs[3])
    # store_named_attribute_001_1.Geometry -> join_geometry_2.Geometry
    combo.links.new(store_named_attribute_001_1.outputs[0], join_geometry_2.inputs[0])
    return combo

# initialize gn_osu node group
def gn_osu_node_group():
    gn_osu = bpy.data.node_groups.new(type='GeometryNodeTree', name="GN_Osu")

    gn_osu.color_tag = 'NONE'
    gn_osu.description = ""

    gn_osu.is_modifier = True

    # gn_osu interface
    # Socket Geometry
    geometry_socket_8 = gn_osu.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket_8.attribute_domain = 'POINT'

    # Socket Geometry
    geometry_socket_9 = gn_osu.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_9.attribute_domain = 'POINT'

    # Socket Cursor Collection
    cursor_collection_socket = gn_osu.interface.new_socket(name="Cursor Collection", in_out='INPUT',
                                                           socket_type='NodeSocketCollection')
    cursor_collection_socket.attribute_domain = 'POINT'

    # Socket Approach Circles Collection
    approach_circles_collection_socket = gn_osu.interface.new_socket(name="Approach Circles Collection", in_out='INPUT',
                                                                     socket_type='NodeSocketCollection')
    approach_circles_collection_socket.attribute_domain = 'POINT'

    # Socket Circles Collection
    circles_collection_socket = gn_osu.interface.new_socket(name="Circles Collection", in_out='INPUT',
                                                            socket_type='NodeSocketCollection')
    circles_collection_socket.attribute_domain = 'POINT'

    # Socket Sliders Collection
    sliders_collection_socket = gn_osu.interface.new_socket(name="Sliders Collection", in_out='INPUT',
                                                            socket_type='NodeSocketCollection')
    sliders_collection_socket.attribute_domain = 'POINT'

    # Socket Slider Head/Tail Collection
    slider_head_tail_collection_socket = gn_osu.interface.new_socket(name="Slider Head/Tail Collection", in_out='INPUT',
                                                                     socket_type='NodeSocketCollection')
    slider_head_tail_collection_socket.attribute_domain = 'POINT'

    # Socket Slider Balls Collection
    slider_balls_collection_socket = gn_osu.interface.new_socket(name="Slider Balls Collection", in_out='INPUT',
                                                                 socket_type='NodeSocketCollection')
    slider_balls_collection_socket.attribute_domain = 'POINT'

    # Socket Spinners Collection
    spinners_collection_socket = gn_osu.interface.new_socket(name="Spinners Collection", in_out='INPUT',
                                                             socket_type='NodeSocketCollection')
    spinners_collection_socket.attribute_domain = 'POINT'

    # Socket Cursor Material
    cursor_material_socket_1 = gn_osu.interface.new_socket(name="Cursor Material", in_out='INPUT',
                                                           socket_type='NodeSocketMaterial')
    cursor_material_socket_1.attribute_domain = 'POINT'

    # Socket Circle Material
    circle_material_socket_1 = gn_osu.interface.new_socket(name="Circle Material", in_out='INPUT',
                                                           socket_type='NodeSocketMaterial')
    circle_material_socket_1.attribute_domain = 'POINT'

    # Socket Slider Material
    slider_material_socket_1 = gn_osu.interface.new_socket(name="Slider Material", in_out='INPUT',
                                                           socket_type='NodeSocketMaterial')
    slider_material_socket_1.attribute_domain = 'POINT'

    # Socket Slider Balls Material
    slider_balls_material_socket_1 = gn_osu.interface.new_socket(name="Slider Balls Material", in_out='INPUT',
                                                                 socket_type='NodeSocketMaterial')
    slider_balls_material_socket_1.attribute_domain = 'POINT'

    # Socket Slider Head/Tail Material
    slider_head_tail_material_socket_1 = gn_osu.interface.new_socket(name="Slider Head/Tail Material", in_out='INPUT',
                                                                     socket_type='NodeSocketMaterial')
    slider_head_tail_material_socket_1.attribute_domain = 'POINT'

    # Socket Spinner Material
    spinner_material_socket_1 = gn_osu.interface.new_socket(name="Spinner Material", in_out='INPUT',
                                                            socket_type='NodeSocketMaterial')
    spinner_material_socket_1.attribute_domain = 'POINT'

    # Socket Approach Circle Material
    approach_circle_material_socket_1 = gn_osu.interface.new_socket(name="Approach Circle Material", in_out='INPUT',
                                                                    socket_type='NodeSocketMaterial')
    approach_circle_material_socket_1.attribute_domain = 'POINT'

    # initialize gn_osu nodes
    # node Group Input
    group_input_6 = gn_osu.nodes.new("NodeGroupInput")
    group_input_6.name = "Group Input"
    group_input_6.outputs[0].hide = True
    group_input_6.outputs[2].hide = True
    group_input_6.outputs[3].hide = True
    group_input_6.outputs[4].hide = True
    group_input_6.outputs[5].hide = True
    group_input_6.outputs[6].hide = True
    group_input_6.outputs[7].hide = True
    group_input_6.outputs[8].hide = True
    group_input_6.outputs[9].hide = True
    group_input_6.outputs[10].hide = True
    group_input_6.outputs[11].hide = True
    group_input_6.outputs[12].hide = True
    group_input_6.outputs[13].hide = True
    group_input_6.outputs[14].hide = True
    group_input_6.outputs[15].hide = True

    # node Group Output
    group_output_6 = gn_osu.nodes.new("NodeGroupOutput")
    group_output_6.name = "Group Output"
    group_output_6.is_active_output = True

    # node Collection Info
    collection_info_1 = gn_osu.nodes.new("GeometryNodeCollectionInfo")
    collection_info_1.name = "Collection Info"
    collection_info_1.hide = True
    collection_info_1.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info_1.inputs[1].default_value = False
    # Reset Children
    collection_info_1.inputs[2].default_value = False

    # node Group
    group = gn_osu.nodes.new("GeometryNodeGroup")
    group.name = "Group"
    group.node_tree = circle_sim_group_node_group()
    # Socket_4
    group.inputs[2].default_value = 0.009999999776482582

    # node Collection Info.001
    collection_info_001 = gn_osu.nodes.new("GeometryNodeCollectionInfo")
    collection_info_001.name = "Collection Info.001"
    collection_info_001.hide = True
    collection_info_001.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info_001.inputs[1].default_value = False
    # Reset Children
    collection_info_001.inputs[2].default_value = False

    # node Group.001
    group_001 = gn_osu.nodes.new("GeometryNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = slider_sim_group_node_group()
    # Socket_5
    group_001.inputs[4].default_value = True

    # node Join Geometry
    join_geometry_3 = gn_osu.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_3.name = "Join Geometry"

    # node Collection Info.002
    collection_info_002 = gn_osu.nodes.new("GeometryNodeCollectionInfo")
    collection_info_002.name = "Collection Info.002"
    collection_info_002.hide = True
    collection_info_002.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info_002.inputs[1].default_value = False
    # Reset Children
    collection_info_002.inputs[2].default_value = False

    # node Collection Info.003
    collection_info_003 = gn_osu.nodes.new("GeometryNodeCollectionInfo")
    collection_info_003.name = "Collection Info.003"
    collection_info_003.hide = True
    collection_info_003.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info_003.inputs[1].default_value = False
    # Reset Children
    collection_info_003.inputs[2].default_value = False

    # node Group.002
    group_002 = gn_osu.nodes.new("GeometryNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = spinner_sim_group_node_group()
    # Socket_2
    group_002.inputs[1].default_value = 5.0
    # Socket_4
    group_002.inputs[3].default_value = 0.0

    # node Group.003
    group_003 = gn_osu.nodes.new("GeometryNodeGroup")
    group_003.name = "Group.003"
    group_003.node_tree = cursor_group_node_group()
    # Socket_3
    group_003.inputs[2].default_value = -0.20000000298023224

    # node Group Input.001
    group_input_001_5 = gn_osu.nodes.new("NodeGroupInput")
    group_input_001_5.name = "Group Input.001"
    group_input_001_5.outputs[0].hide = True
    group_input_001_5.outputs[1].hide = True
    group_input_001_5.outputs[2].hide = True
    group_input_001_5.outputs[3].hide = True
    group_input_001_5.outputs[4].hide = True
    group_input_001_5.outputs[5].hide = True
    group_input_001_5.outputs[6].hide = True
    group_input_001_5.outputs[8].hide = True
    group_input_001_5.outputs[9].hide = True
    group_input_001_5.outputs[10].hide = True
    group_input_001_5.outputs[11].hide = True
    group_input_001_5.outputs[12].hide = True
    group_input_001_5.outputs[13].hide = True
    group_input_001_5.outputs[14].hide = True
    group_input_001_5.outputs[15].hide = True

    # node Group Input.002
    group_input_002_4 = gn_osu.nodes.new("NodeGroupInput")
    group_input_002_4.name = "Group Input.002"
    group_input_002_4.outputs[0].hide = True
    group_input_002_4.outputs[1].hide = True
    group_input_002_4.outputs[2].hide = True
    group_input_002_4.outputs[3].hide = True
    group_input_002_4.outputs[4].hide = True
    group_input_002_4.outputs[5].hide = True
    group_input_002_4.outputs[7].hide = True
    group_input_002_4.outputs[8].hide = True
    group_input_002_4.outputs[9].hide = True
    group_input_002_4.outputs[10].hide = True
    group_input_002_4.outputs[11].hide = True
    group_input_002_4.outputs[12].hide = True
    group_input_002_4.outputs[13].hide = True
    group_input_002_4.outputs[14].hide = True
    group_input_002_4.outputs[15].hide = True

    # node Group Input.003
    group_input_003_2 = gn_osu.nodes.new("NodeGroupInput")
    group_input_003_2.name = "Group Input.003"
    group_input_003_2.outputs[0].hide = True
    group_input_003_2.outputs[1].hide = True
    group_input_003_2.outputs[2].hide = True
    group_input_003_2.outputs[3].hide = True
    group_input_003_2.outputs[5].hide = True
    group_input_003_2.outputs[6].hide = True
    group_input_003_2.outputs[7].hide = True
    group_input_003_2.outputs[8].hide = True
    group_input_003_2.outputs[9].hide = True
    group_input_003_2.outputs[10].hide = True
    group_input_003_2.outputs[11].hide = True
    group_input_003_2.outputs[12].hide = True
    group_input_003_2.outputs[13].hide = True
    group_input_003_2.outputs[14].hide = True
    group_input_003_2.outputs[15].hide = True

    # node Group Input.004
    group_input_004_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_004_1.name = "Group Input.004"
    group_input_004_1.outputs[0].hide = True
    group_input_004_1.outputs[1].hide = True
    group_input_004_1.outputs[2].hide = True
    group_input_004_1.outputs[4].hide = True
    group_input_004_1.outputs[5].hide = True
    group_input_004_1.outputs[6].hide = True
    group_input_004_1.outputs[7].hide = True
    group_input_004_1.outputs[8].hide = True
    group_input_004_1.outputs[9].hide = True
    group_input_004_1.outputs[10].hide = True
    group_input_004_1.outputs[11].hide = True
    group_input_004_1.outputs[12].hide = True
    group_input_004_1.outputs[13].hide = True
    group_input_004_1.outputs[14].hide = True
    group_input_004_1.outputs[15].hide = True

    # node Join Geometry.001
    join_geometry_001_1 = gn_osu.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001_1.name = "Join Geometry.001"

    # node Join Geometry.002
    join_geometry_002_1 = gn_osu.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002_1.name = "Join Geometry.002"

    # node Group Input.005
    group_input_005_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_005_1.name = "Group Input.005"
    group_input_005_1.outputs[0].hide = True
    group_input_005_1.outputs[1].hide = True
    group_input_005_1.outputs[2].hide = True
    group_input_005_1.outputs[3].hide = True
    group_input_005_1.outputs[4].hide = True
    group_input_005_1.outputs[5].hide = True
    group_input_005_1.outputs[6].hide = True
    group_input_005_1.outputs[7].hide = True
    group_input_005_1.outputs[8].hide = True
    group_input_005_1.outputs[10].hide = True
    group_input_005_1.outputs[11].hide = True
    group_input_005_1.outputs[12].hide = True
    group_input_005_1.outputs[13].hide = True
    group_input_005_1.outputs[14].hide = True
    group_input_005_1.outputs[15].hide = True

    # node Group Input.006
    group_input_006 = gn_osu.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[0].hide = True
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[3].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True
    group_input_006.outputs[6].hide = True
    group_input_006.outputs[7].hide = True
    group_input_006.outputs[9].hide = True
    group_input_006.outputs[10].hide = True
    group_input_006.outputs[11].hide = True
    group_input_006.outputs[12].hide = True
    group_input_006.outputs[13].hide = True
    group_input_006.outputs[14].hide = True
    group_input_006.outputs[15].hide = True

    # node Group Input.007
    group_input_007 = gn_osu.nodes.new("NodeGroupInput")
    group_input_007.name = "Group Input.007"
    group_input_007.outputs[0].hide = True
    group_input_007.outputs[1].hide = True
    group_input_007.outputs[2].hide = True
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    group_input_007.outputs[5].hide = True
    group_input_007.outputs[6].hide = True
    group_input_007.outputs[7].hide = True
    group_input_007.outputs[8].hide = True
    group_input_007.outputs[9].hide = True
    group_input_007.outputs[10].hide = True
    group_input_007.outputs[11].hide = True
    group_input_007.outputs[12].hide = True
    group_input_007.outputs[14].hide = True
    group_input_007.outputs[15].hide = True

    # node Group Input.008
    group_input_008_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_008_1.name = "Group Input.008"
    group_input_008_1.outputs[0].hide = True
    group_input_008_1.outputs[1].hide = True
    group_input_008_1.outputs[2].hide = True
    group_input_008_1.outputs[3].hide = True
    group_input_008_1.outputs[4].hide = True
    group_input_008_1.outputs[5].hide = True
    group_input_008_1.outputs[6].hide = True
    group_input_008_1.outputs[7].hide = True
    group_input_008_1.outputs[8].hide = True
    group_input_008_1.outputs[9].hide = True
    group_input_008_1.outputs[10].hide = True
    group_input_008_1.outputs[11].hide = True
    group_input_008_1.outputs[13].hide = True
    group_input_008_1.outputs[14].hide = True
    group_input_008_1.outputs[15].hide = True

    # node Group Input.009
    group_input_009_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_009_1.name = "Group Input.009"
    group_input_009_1.outputs[0].hide = True
    group_input_009_1.outputs[1].hide = True
    group_input_009_1.outputs[2].hide = True
    group_input_009_1.outputs[3].hide = True
    group_input_009_1.outputs[4].hide = True
    group_input_009_1.outputs[5].hide = True
    group_input_009_1.outputs[6].hide = True
    group_input_009_1.outputs[7].hide = True
    group_input_009_1.outputs[8].hide = True
    group_input_009_1.outputs[9].hide = True
    group_input_009_1.outputs[10].hide = True
    group_input_009_1.outputs[12].hide = True
    group_input_009_1.outputs[13].hide = True
    group_input_009_1.outputs[14].hide = True
    group_input_009_1.outputs[15].hide = True

    # node Group Input.010
    group_input_010_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_010_1.name = "Group Input.010"
    group_input_010_1.outputs[0].hide = True
    group_input_010_1.outputs[1].hide = True
    group_input_010_1.outputs[2].hide = True
    group_input_010_1.outputs[3].hide = True
    group_input_010_1.outputs[4].hide = True
    group_input_010_1.outputs[5].hide = True
    group_input_010_1.outputs[6].hide = True
    group_input_010_1.outputs[7].hide = True
    group_input_010_1.outputs[8].hide = True
    group_input_010_1.outputs[9].hide = True
    group_input_010_1.outputs[11].hide = True
    group_input_010_1.outputs[12].hide = True
    group_input_010_1.outputs[13].hide = True
    group_input_010_1.outputs[14].hide = True
    group_input_010_1.outputs[15].hide = True

    # node Collection Info.004
    collection_info_004 = gn_osu.nodes.new("GeometryNodeCollectionInfo")
    collection_info_004.name = "Collection Info.004"
    collection_info_004.hide = True
    collection_info_004.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info_004.inputs[1].default_value = False
    # Reset Children
    collection_info_004.inputs[2].default_value = False

    # node Group Input.011
    group_input_011_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_011_1.name = "Group Input.011"
    group_input_011_1.outputs[0].hide = True
    group_input_011_1.outputs[1].hide = True
    group_input_011_1.outputs[3].hide = True
    group_input_011_1.outputs[4].hide = True
    group_input_011_1.outputs[5].hide = True
    group_input_011_1.outputs[6].hide = True
    group_input_011_1.outputs[7].hide = True
    group_input_011_1.outputs[8].hide = True
    group_input_011_1.outputs[9].hide = True
    group_input_011_1.outputs[10].hide = True
    group_input_011_1.outputs[11].hide = True
    group_input_011_1.outputs[12].hide = True
    group_input_011_1.outputs[13].hide = True
    group_input_011_1.outputs[14].hide = True
    group_input_011_1.outputs[15].hide = True

    # node Join Geometry.003
    join_geometry_003_1 = gn_osu.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003_1.name = "Join Geometry.003"

    # node Group.004
    group_004 = gn_osu.nodes.new("GeometryNodeGroup")
    group_004.name = "Group.004"
    group_004.node_tree = approach_circle_group_node_group()
    # Socket_2
    group_004.inputs[1].default_value = -0.10000000149011612

    # node Bake
    bake = gn_osu.nodes.new("GeometryNodeBake")
    bake.name = "Bake"
    bake.active_index = 0
    bake.bake_items.clear()
    bake.bake_items.new('GEOMETRY', "Geometry")
    bake.bake_items[0].attribute_domain = 'POINT'

    # node Group Input.012
    group_input_012_1 = gn_osu.nodes.new("NodeGroupInput")
    group_input_012_1.name = "Group Input.012"
    group_input_012_1.outputs[0].hide = True
    group_input_012_1.outputs[1].hide = True
    group_input_012_1.outputs[2].hide = True
    group_input_012_1.outputs[3].hide = True
    group_input_012_1.outputs[4].hide = True
    group_input_012_1.outputs[5].hide = True
    group_input_012_1.outputs[6].hide = True
    group_input_012_1.outputs[7].hide = True
    group_input_012_1.outputs[8].hide = True
    group_input_012_1.outputs[9].hide = True
    group_input_012_1.outputs[10].hide = True
    group_input_012_1.outputs[11].hide = True
    group_input_012_1.outputs[12].hide = True
    group_input_012_1.outputs[13].hide = True
    group_input_012_1.outputs[15].hide = True

    # node Collection Info.005
    collection_info_005 = gn_osu.nodes.new("GeometryNodeCollectionInfo")
    collection_info_005.name = "Collection Info.005"
    collection_info_005.hide = True
    collection_info_005.transform_space = 'ORIGINAL'
    # Separate Children
    collection_info_005.inputs[1].default_value = False
    # Reset Children
    collection_info_005.inputs[2].default_value = False

    # node Group Input.013
    group_input_013 = gn_osu.nodes.new("NodeGroupInput")
    group_input_013.name = "Group Input.013"
    group_input_013.outputs[0].hide = True
    group_input_013.outputs[1].hide = True
    group_input_013.outputs[2].hide = True
    group_input_013.outputs[3].hide = True
    group_input_013.outputs[4].hide = True
    group_input_013.outputs[6].hide = True
    group_input_013.outputs[7].hide = True
    group_input_013.outputs[8].hide = True
    group_input_013.outputs[9].hide = True
    group_input_013.outputs[10].hide = True
    group_input_013.outputs[11].hide = True
    group_input_013.outputs[12].hide = True
    group_input_013.outputs[13].hide = True
    group_input_013.outputs[14].hide = True
    group_input_013.outputs[15].hide = True

    # node Group.005
    group_005 = gn_osu.nodes.new("GeometryNodeGroup")
    group_005.name = "Group.005"
    group_005.node_tree = combo_node_group()
    # Socket_1
    group_005.inputs[0].default_value = 0.4000000059604645

    # node Reroute
    reroute_3 = gn_osu.nodes.new("NodeReroute")
    reroute_3.name = "Reroute"
    # node Reroute.001
    reroute_001_3 = gn_osu.nodes.new("NodeReroute")
    reroute_001_3.name = "Reroute.001"
    # node Named Attribute
    named_attribute_6 = gn_osu.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_6.name = "Named Attribute"
    named_attribute_6.data_type = 'INT'
    # Name
    named_attribute_6.inputs[0].default_value = "combo"

    # node Map Range
    map_range_1 = gn_osu.nodes.new("ShaderNodeMapRange")
    map_range_1.name = "Map Range"
    map_range_1.clamp = True
    map_range_1.data_type = 'FLOAT'
    map_range_1.interpolation_type = 'LINEAR'
    # From Min
    map_range_1.inputs[1].default_value = 1.0
    # To Min
    map_range_1.inputs[3].default_value = 0.0
    # To Max
    map_range_1.inputs[4].default_value = 0.10000000149011612

    # node Combine XYZ
    combine_xyz_4 = gn_osu.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_4.name = "Combine XYZ"
    # X
    combine_xyz_4.inputs[0].default_value = 0.0
    # Z
    combine_xyz_4.inputs[2].default_value = 0.0

    # node Attribute Statistic
    attribute_statistic_3 = gn_osu.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_3.name = "Attribute Statistic"
    attribute_statistic_3.data_type = 'FLOAT'
    attribute_statistic_3.domain = 'INSTANCE'

    # node Set Position.002
    set_position_002_1 = gn_osu.nodes.new("GeometryNodeSetPosition")
    set_position_002_1.name = "Set Position.002"
    # Selection
    set_position_002_1.inputs[1].default_value = True
    # Position
    set_position_002_1.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Set locations
    group_input_6.location = (3180.0, -20.0)
    group_output_6.location = (4020.0, 60.0)
    collection_info_1.location = (40.0, 60.0)
    group.location = (200.0, 60.0)
    collection_info_001.location = (620.0, -20.0)
    group_001.location = (780.0, -40.0)
    join_geometry_3.location = (1020.0, 60.0)
    collection_info_002.location = (3340.0, -20.0)
    collection_info_003.location = (1340.0, -20.0)
    group_002.location = (1500.0, -20.0)
    group_003.location = (3500.0, -20.0)
    group_input_001_5.location = (1180.0, -20.0)
    group_input_002_4.location = (620.0, -200.0)
    group_input_003_2.location = (460.0, -20.0)
    group_input_004_1.location = (-120.0, 60.0)
    join_geometry_001_1.location = (1680.0, 60.0)
    join_geometry_002_1.location = (3700.0, 60.0)
    group_input_005_1.location = (40.0, -20.0)
    group_input_006.location = (3500.0, -180.0)
    group_input_007.location = (1500.0, -200.0)
    group_input_008_1.location = (620.0, -320.0)
    group_input_009_1.location = (620.0, -260.0)
    group_input_010_1.location = (620.0, -140.0)
    collection_info_004.location = (2020.0, -20.0)
    group_input_011_1.location = (1860.0, -20.0)
    join_geometry_003_1.location = (2340.0, 60.0)
    group_004.location = (2180.0, -20.0)
    bake.location = (3860.0, 60.0)
    group_input_012_1.location = (2180.0, -180.0)
    collection_info_005.location = (620.0, -80.0)
    group_input_013.location = (460.0, -80.0)
    group_005.location = (40.0, -100.0)
    reroute_3.location = (380.0, 0.0)
    reroute_001_3.location = (380.0, -140.0)
    named_attribute_6.location = (2520.0, -360.0)
    map_range_1.location = (2680.0, -20.0)
    combine_xyz_4.location = (2840.0, -20.0)
    attribute_statistic_3.location = (2520.0, -20.0)
    set_position_002_1.location = (3000.0, 60.0)

    # Set dimensions
    group_input_6.width, group_input_6.height = 140.0, 100.0
    group_output_6.width, group_output_6.height = 140.0, 100.0
    collection_info_1.width, collection_info_1.height = 140.0, 100.0
    group.width, group.height = 140.0, 100.0
    collection_info_001.width, collection_info_001.height = 140.0, 100.0
    group_001.width, group_001.height = 213.9149169921875, 100.0
    join_geometry_3.width, join_geometry_3.height = 140.0, 100.0
    collection_info_002.width, collection_info_002.height = 140.0, 100.0
    collection_info_003.width, collection_info_003.height = 140.0, 100.0
    group_002.width, group_002.height = 140.0, 100.0
    group_003.width, group_003.height = 181.4385986328125, 100.0
    group_input_001_5.width, group_input_001_5.height = 140.0, 100.0
    group_input_002_4.width, group_input_002_4.height = 140.0, 100.0
    group_input_003_2.width, group_input_003_2.height = 140.0, 100.0
    group_input_004_1.width, group_input_004_1.height = 140.0, 100.0
    join_geometry_001_1.width, join_geometry_001_1.height = 140.0, 100.0
    join_geometry_002_1.width, join_geometry_002_1.height = 140.0, 100.0
    group_input_005_1.width, group_input_005_1.height = 140.0, 100.0
    group_input_006.width, group_input_006.height = 140.0, 100.0
    group_input_007.width, group_input_007.height = 140.0, 100.0
    group_input_008_1.width, group_input_008_1.height = 140.0, 100.0
    group_input_009_1.width, group_input_009_1.height = 140.0, 100.0
    group_input_010_1.width, group_input_010_1.height = 140.0, 100.0
    collection_info_004.width, collection_info_004.height = 140.0, 100.0
    group_input_011_1.width, group_input_011_1.height = 140.0, 100.0
    join_geometry_003_1.width, join_geometry_003_1.height = 140.0, 100.0
    group_004.width, group_004.height = 140.0, 100.0
    bake.width, bake.height = 140.0, 100.0
    group_input_012_1.width, group_input_012_1.height = 140.0, 100.0
    collection_info_005.width, collection_info_005.height = 140.0, 100.0
    group_input_013.width, group_input_013.height = 140.0, 100.0
    group_005.width, group_005.height = 140.0, 100.0
    reroute_3.width, reroute_3.height = 16.0, 100.0
    reroute_001_3.width, reroute_001_3.height = 16.0, 100.0
    named_attribute_6.width, named_attribute_6.height = 140.0, 100.0
    map_range_1.width, map_range_1.height = 140.0, 100.0
    combine_xyz_4.width, combine_xyz_4.height = 140.0, 100.0
    attribute_statistic_3.width, attribute_statistic_3.height = 140.0, 100.0
    set_position_002_1.width, set_position_002_1.height = 140.0, 100.0

    # initialize gn_osu links
    # collection_info_1.Instances -> group.Geometry
    gn_osu.links.new(collection_info_1.outputs[0], group.inputs[0])
    # collection_info_001.Instances -> group_001.Geometry
    gn_osu.links.new(collection_info_001.outputs[0], group_001.inputs[0])
    # bake.Geometry -> group_output_6.Geometry
    gn_osu.links.new(bake.outputs[0], group_output_6.inputs[0])
    # group_001.Geometry -> join_geometry_3.Geometry
    gn_osu.links.new(group_001.outputs[0], join_geometry_3.inputs[0])
    # collection_info_003.Instances -> group_002.Geometry
    gn_osu.links.new(collection_info_003.outputs[0], group_002.inputs[0])
    # reroute_001_3.Output -> group_001.Circle Mesh
    gn_osu.links.new(reroute_001_3.outputs[0], group_001.inputs[1])
    # collection_info_002.Instances -> group_003.Points
    gn_osu.links.new(collection_info_002.outputs[0], group_003.inputs[0])
    # group_input_6.Cursor Collection -> collection_info_002.Collection
    gn_osu.links.new(group_input_6.outputs[1], collection_info_002.inputs[0])
    # group_input_001_5.Spinners Collection -> collection_info_003.Collection
    gn_osu.links.new(group_input_001_5.outputs[7], collection_info_003.inputs[0])
    # group_input_002_4.Slider Balls Collection -> group_001.Slider Balls
    gn_osu.links.new(group_input_002_4.outputs[6], group_001.inputs[5])
    # group_input_003_2.Sliders Collection -> collection_info_001.Collection
    gn_osu.links.new(group_input_003_2.outputs[4], collection_info_001.inputs[0])
    # group_input_004_1.Circles Collection -> collection_info_1.Collection
    gn_osu.links.new(group_input_004_1.outputs[3], collection_info_1.inputs[0])
    # group_002.Geometry -> join_geometry_001_1.Geometry
    gn_osu.links.new(group_002.outputs[0], join_geometry_001_1.inputs[0])
    # group_003.Geometry -> join_geometry_002_1.Geometry
    gn_osu.links.new(group_003.outputs[0], join_geometry_002_1.inputs[0])
    # group_input_005_1.Circle Material -> group.Circle Material
    gn_osu.links.new(group_input_005_1.outputs[9], group.inputs[1])
    # group_input_006.Cursor Material -> group_003.Cursor Material
    gn_osu.links.new(group_input_006.outputs[8], group_003.inputs[1])
    # group_input_007.Spinner Material -> group_002.Spinner Material
    gn_osu.links.new(group_input_007.outputs[13], group_002.inputs[2])
    # group_input_008_1.Slider Head/Tail Material -> group_001.Slider Head/Tail Material
    gn_osu.links.new(group_input_008_1.outputs[12], group_001.inputs[7])
    # group_input_009_1.Slider Balls Material -> group_001.Slider Balls Material
    gn_osu.links.new(group_input_009_1.outputs[11], group_001.inputs[6])
    # group_input_010_1.Slider Material -> group_001.Slider Material
    gn_osu.links.new(group_input_010_1.outputs[10], group_001.inputs[3])
    # group_input_011_1.Approach Circles Collection -> collection_info_004.Collection
    gn_osu.links.new(group_input_011_1.outputs[2], collection_info_004.inputs[0])
    # group_004.Instances -> join_geometry_003_1.Geometry
    gn_osu.links.new(group_004.outputs[0], join_geometry_003_1.inputs[0])
    # collection_info_004.Instances -> group_004.Geometry
    gn_osu.links.new(collection_info_004.outputs[0], group_004.inputs[0])
    # join_geometry_002_1.Geometry -> bake.Geometry
    gn_osu.links.new(join_geometry_002_1.outputs[0], bake.inputs[0])
    # group_input_012_1.Approach Circle Material -> group_004.Approach Circle Material
    gn_osu.links.new(group_input_012_1.outputs[14], group_004.inputs[2])
    # collection_info_005.Instances -> group_001.Slider Head/Tail
    gn_osu.links.new(collection_info_005.outputs[0], group_001.inputs[2])
    # group_input_013.Slider Head/Tail Collection -> collection_info_005.Collection
    gn_osu.links.new(group_input_013.outputs[5], collection_info_005.inputs[0])
    # group_005.Geometry -> group.Instance
    gn_osu.links.new(group_005.outputs[0], group.inputs[3])
    # group.Circle Mesh -> reroute_3.Input
    gn_osu.links.new(group.outputs[1], reroute_3.inputs[0])
    # reroute_3.Output -> reroute_001_3.Input
    gn_osu.links.new(reroute_3.outputs[0], reroute_001_3.inputs[0])
    # group_005.Geometry -> group_001.Instance
    gn_osu.links.new(group_005.outputs[0], group_001.inputs[8])
    # named_attribute_6.Attribute -> map_range_1.Value
    gn_osu.links.new(named_attribute_6.outputs[0], map_range_1.inputs[0])
    # map_range_1.Result -> combine_xyz_4.Y
    gn_osu.links.new(map_range_1.outputs[0], combine_xyz_4.inputs[1])
    # named_attribute_6.Attribute -> attribute_statistic_3.Selection
    gn_osu.links.new(named_attribute_6.outputs[0], attribute_statistic_3.inputs[1])
    # named_attribute_6.Attribute -> attribute_statistic_3.Attribute
    gn_osu.links.new(named_attribute_6.outputs[0], attribute_statistic_3.inputs[2])
    # join_geometry_001_1.Geometry -> attribute_statistic_3.Geometry
    gn_osu.links.new(join_geometry_001_1.outputs[0], attribute_statistic_3.inputs[0])
    # attribute_statistic_3.Max -> map_range_1.From Max
    gn_osu.links.new(attribute_statistic_3.outputs[4], map_range_1.inputs[2])
    # combine_xyz_4.Vector -> set_position_002_1.Offset
    gn_osu.links.new(combine_xyz_4.outputs[0], set_position_002_1.inputs[3])
    # join_geometry_003_1.Geometry -> set_position_002_1.Geometry
    gn_osu.links.new(join_geometry_003_1.outputs[0], set_position_002_1.inputs[0])
    # group.Circles -> join_geometry_3.Geometry
    gn_osu.links.new(group.outputs[0], join_geometry_3.inputs[0])
    # join_geometry_3.Geometry -> join_geometry_001_1.Geometry
    gn_osu.links.new(join_geometry_3.outputs[0], join_geometry_001_1.inputs[0])
    # set_position_002_1.Geometry -> join_geometry_002_1.Geometry
    gn_osu.links.new(set_position_002_1.outputs[0], join_geometry_002_1.inputs[0])
    # join_geometry_001_1.Geometry -> join_geometry_003_1.Geometry
    gn_osu.links.new(join_geometry_001_1.outputs[0], join_geometry_003_1.inputs[0])
    return gn_osu
