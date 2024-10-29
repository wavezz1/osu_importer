import bpy

def create_geometry_nodes_modifier(obj, node_group_name, attributes):
    # Überprüfen, ob die Node Group bereits existiert, sonst erstellen
    if node_group_name in bpy.data.node_groups:
        group = bpy.data.node_groups[node_group_name]
    else:
        group = bpy.data.node_groups.new(node_group_name, 'GeometryNodeTree')
        setup_node_group_interface(group, attributes)

    # Modifier hinzufügen und Node Group zuweisen
    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
    modifier.node_group = group


def setup_node_group_interface(group, attributes):
    x_offset = 200
    # Füge einen Geometry Eingang und Ausgang hinzu
    group.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    group.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')

    input_node = group.nodes.new('NodeGroupInput')
    input_node.location = (0, 0)
    output_node = group.nodes.new('NodeGroupOutput')
    output_node.location = (x_offset * (len(attributes) + 1), 0)

    # Verlinke direkt Geometry Input mit dem ersten Store Node
    previous_node_output = input_node.outputs['Geometry']

    socket_map = {
        "BOOLEAN": "NodeSocketBool",
        "FLOAT": "NodeSocketFloat",
        "INT": "NodeSocketInt"
    }

    for i, (attr_name, attr_type) in enumerate(attributes.items()):
        store_node = group.nodes.new('GeometryNodeStoreNamedAttribute')
        store_node.location = (x_offset * (i + 1), 0)
        store_node.inputs['Name'].default_value = attr_name
        store_node.data_type = attr_type
        store_node.domain = 'POINT'

        # Verlinken des vorherigen Knotens mit dem aktuellen Store Node
        group.links.new(previous_node_output, store_node.inputs['Geometry'])
        previous_node_output = store_node.outputs['Geometry']

        # Hole den richtigen Socket-Typ aus der socket_map
        socket_type = socket_map.get(attr_type.upper(), "NodeSocketFloat")  # Fallback auf Float, falls nicht gefunden
        new_socket = group.interface.new_socket(name=attr_name, in_out='INPUT', socket_type=socket_type)
        group.links.new(input_node.outputs[new_socket.name], store_node.inputs['Value'])
    # Verlinke den letzten Store Node mit dem Output
    group.links.new(previous_node_output, output_node.inputs['Geometry'])


def create_geometry_nodes_modifier_circle(obj, node_group_name):
    attributes = {"show": 'BOOLEAN', "was_hit": 'BOOLEAN', "ar": 'FLOAT', "cs": 'FLOAT'}
    create_geometry_nodes_modifier(obj, node_group_name, attributes)


def create_geometry_nodes_modifier_slider(obj, node_group_name):
    attributes = {
        "show": 'BOOLEAN',
        "slider_duration": 'FLOAT',
        "slider_duration_frames": 'FLOAT',
        "ar": 'FLOAT',
        "cs": 'FLOAT',
        "was_hit": 'BOOLEAN',
        "was_completed": 'BOOLEAN'
    }
    create_geometry_nodes_modifier(obj, node_group_name, attributes)


def create_geometry_nodes_modifier_spinner(obj, node_group_name):
    attributes = {
        "show": 'BOOLEAN',
        "spinner_duration_ms": 'FLOAT',
        "spinner_duration_frames": 'FLOAT',
        "was_hit": 'BOOLEAN',
        "was_completed": 'BOOLEAN'
    }
    create_geometry_nodes_modifier(obj, node_group_name, attributes)


def create_geometry_nodes_modifier_cursor(obj, node_group_name):
    attributes = {"k1": 'BOOLEAN', "k2": 'BOOLEAN', "m1": 'BOOLEAN', "m2": 'BOOLEAN'}
    create_geometry_nodes_modifier(obj, node_group_name, attributes)


def connect_attributes_with_drivers(obj, attributes):
    modifier = obj.modifiers.get("GeometryNodes")
    if not modifier:
        return

    # Definiere die Socket-Zuordnungen je nach Objekttyp
    socket_mapping = {
        "circle": {
            "ar": "Socket_2",
            "cs": "Socket_3",
            "show": "Socket_4",
            "was_hit": "Socket_5"
        },
        "slider": {
            "ar": "Socket_2",
            "cs": "Socket_3",
            "show": "Socket_4",
            "slider_duration_frames": "Socket_5",
            "slider_duration_ms": "Socket_6",
            "was_completed": "Socket_7",
            "was_hit": "Socket_8"
        },
        "spinner": {
            "show": "Socket_2",
            "spinner_duration_frames": "Socket_3",
            "spinner_duration_ms": "Socket_4",
            "was_completed": "Socket_5",
            "was_hit": "Socket_6"
        },
        "cursor": {
            "k1": "Socket_2",
            "k2": "Socket_3",
            "m1": "Socket_4",
            "m2": "Socket_5"
        }
    }

    # Bestimme den Objekttyp und die zugehörige Socket-Zuordnung
    if "circle" in obj.name.lower():
        sockets = socket_mapping["circle"]
    elif "slider" in obj.name.lower():
        sockets = socket_mapping["slider"]
    elif "spinner" in obj.name.lower():
        sockets = socket_mapping["spinner"]
    elif "cursor" in obj.name.lower():
        sockets = socket_mapping["cursor"]
    else:
        print(f"Unrecognized object type for {obj.name}. Skipping driver setup.")
        return

    # Füge die Driver für jedes Attribut entsprechend der Socket-Zuordnung hinzu
    for attr_name, socket_name in sockets.items():
        # Überprüfen, ob die Objekt-Property für das Attribut existiert
        if attr_name not in obj:
            continue

        try:
            # Füge den Driver hinzu, der den Object-Property-Wert an den Socket-Wert bindet
            driver = modifier.driver_add(f'["{socket_name}"]').driver
            driver.type = 'AVERAGE'
            var = driver.variables.new()
            var.name = 'var'
            var.targets[0].id_type = 'OBJECT'
            var.targets[0].id = obj
            var.targets[0].data_path = f'["{attr_name}"]'
        except Exception as e:
            print(f"Could not set driver for {attr_name} on {socket_name}: {e}")
