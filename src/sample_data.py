"""
Campus data specific to Adelaide University North Terrace Campus
"""

from campus_graph import (
    CampusGraph, Node, Edge, AccessibilityFeature, SurfaceType
)
from datetime import datetime, timedelta


def create_sample_campus() -> CampusGraph:
    """
    Create an enhanced campus graph with realistic North Terrace buildings and pathways
    """
    graph = CampusGraph()
    
    # Update current data
    graph.metadata = {
        "campus_name": "University of Adelaide - North Terrace Campus",
        "last_updated": datetime.now().isoformat(),
        "contributors": ["Enhanced Accessibility Mapping"],
        "version": "0.2.0",
        "notes": "Expanded map with realistic accessibility features"
    }
    
    # === BARR SMITH LIBRARY - Multiple Entrances ===
    
    barr_smith_main = Node(
        id="bs_main_entrance",
        name="Barr Smith Library - Main Entrance (Ground Level)",
        latitude=-34.919251817144605,
        longitude=138.60429514698788,
        building="Barr Smith Library",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.ELEVATOR,
            AccessibilityFeature.ACCESSIBLE_BATHROOM,
            AccessibilityFeature.REST_AREA
        },
        notes="Main accessible entrance with elevator access to all floors"
    )
    
    barr_smith_north = Node(
        id="bs_north_entrance",
        name="Barr Smith Library - North Entrance",
        latitude=-34.91877896564302,
        longitude=138.60424418502268,
        building="Barr Smith Library",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.RAMP
        },
        notes="Alternative entrance with ramped access"
    )


    
    barr_smith_level1 = Node(
        id="bs_level1",
        name="Barr Smith Library - Level 1",
        latitude=-34.918619444918605,
        longitude=138.60455312015242,
        building="Barr Smith Library",
        floor=1,
        is_indoor=True,
        features={
            AccessibilityFeature.ELEVATOR,
            AccessibilityFeature.REST_AREA,
            AccessibilityFeature.ACCESSIBLE_BATHROOM
        }
    )
    
    # === HUB CENTRAL - Student Services ===
    
    hub_central = Node(
        id="hub_central",
        name="Hub Central - Main Entrance",
        latitude=-34.91955663264137,
        longitude=138.60421415275155,
        building="Hub Central",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.ELEVATOR,
            AccessibilityFeature.REST_AREA,
            AccessibilityFeature.ACCESSIBLE_BATHROOM
        },
        notes="Primary student services location"
    )
    
    hub_east_entrance = Node(
        id="hub_east_entrance",
        name="Hub Central - East Entrance",
        latitude=-34.919770155409076,
        longitude=138.60481408963486,
        building="Hub Central",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.RAMP
        }
    )
    
    # === INGKARNI WARDLI BUILDING ===
    
    ingkarni_wardli_main = Node(
        id="ingkarni_wardli_main",
        name="Ingkarni Wardli - Main Entrance",
        latitude=-34.91890907984514,
        longitude=138.60504954252696,
        building="Ingkarni Wardli",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.ELEVATOR,
            AccessibilityFeature.ACCESSIBLE_BATHROOM
        }
    )
    
    ingkarni_wardli_north = Node(
        id="ingkarni_wardli_north",
        name="Ingkarni Wardli - North Entrance",
        latitude=-34.91863424486643,
        longitude=138.6053461872855,
        building="Ingkarni Wardli",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.RAMP
        },
        notes="Level entry from north side"
    )
    
    # === NAPIER BUILDING ===
    
    napier_main = Node(
        id="napier_main",
        name="Napier Building - Main Entrance",
        latitude=-34.919935220248874,
        longitude=138.60545318096382,
        building="Napier Building",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.ELEVATOR
        }
    )
    
    napier_south = Node(
        id="napier_south",
        name="Napier Building - South Entrance (Ramped)",
        latitude=-34.92020445592288,
        longitude=138.6057735925189,
        building="Napier Building",
        floor=0,
        features={
            AccessibilityFeature.RAMP,
            AccessibilityFeature.HANDRAILS
        },
        notes="Ramped access - easier approach than main entrance"
    )
    
    # === SCOTT THEATRE ===
    
    scott_theatre = Node(
        id="scott_theatre",
        name="Scott Theatre - Accessible Entrance",
        latitude=-34.91880956495803,
        longitude=138.60281365632395,
        building="Scott Theatre",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.RAMP
        }
    )
    
    # === ENGINEERING BUILDINGS ===
    
    eng_north_main = Node(
        id="eng_north_main",
        name="Engineering North - Main Entrance",
        latitude=-34.91874719497902,
        longitude=138.6057857055029,
        building="Engineering North",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.ELEVATOR,
            AccessibilityFeature.ACCESSIBLE_BATHROOM
        }
    )
    
    eng_mathews_link = Node(
        id="eng_mathews_link",
        name="Engineering Annex",
        latitude=-34.91889389179538, 
        longitude=138.60625821610563,
        building="Engineering Annex",
        floor=1,
        is_indoor=True,
        features={
            AccessibilityFeature.ELEVATOR
        },
        notes="Engineering Annex"
    )

    eng_south_1st_floor = Node(
        id = "eng_south_1st_floor",
        name = "Engineering South 1st Floor Entrance",
        latitude=-34.91959891359262, 
        longitude=138.60557396196234,
        building = "Engineering South",
        floor = 1,
        features={
            AccessibilityFeature.REST_AREA
        },
    )

    eng_south_ground_floor = Node(
        id = "eng_south_ground_floor",
        name = "Engineering South Ground Floor Entrance",
        latitude=-34.919154404000565,
        longitude=138.60572351021352,
        building = "Engineering South",
        floor = 0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR
        },
    )
    
    # === UNION HOUSE & DINING ===
    
    union_house = Node(
        id="union_house",
        name="Union House - Main Entrance",
        latitude=-34.91863853827505, 
        longitude=138.60364727115444,
        building="Union House",
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.REST_AREA,
            AccessibilityFeature.ACCESSIBLE_BATHROOM,
            AccessibilityFeature.ELEVATOR
        },
        notes="Food court and student spaces"
    )
    
    union_courtyard = Node(
        id="union_courtyard",
        name="Union House - Courtyard Entrance",
        latitude=-34.91829152873983, 
        longitude=138.60360593542117,
        features={
            AccessibilityFeature.REST_AREA
        },
        notes="Outdoor seating area"
    )
    
    # === HORACE LAMB BUILDING ===
    
    horace_lamb = Node(
        id="horace_lamb",
        name="Horace Lamb Building - Entrance",
        latitude=-34.91907626149523, 
        longitude=138.6049329686916,
        building="Horace Lamb",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.ELEVATOR
        }
    )
    
    # === OUTDOOR PLAZAS & PATHWAYS ===
    north_terrace_crossing = Node(
        id="north_terrace_crossing",
        name="North Terrace Pedestrian Crossing",
        latitude=-34.92114391128113, 
        longitude= 138.60550434306367,
        features={
            AccessibilityFeature.CURB_CUT
        },
        notes="Accessible pedestrian crossing"
    )
    
    library_courtyard = Node(
        id="library_courtyard",
        name="Library Courtyard / Barr Smith Lawns",
        latitude=-34.91839566654292, 
        longitude=138.60428878165683,
        features={
            AccessibilityFeature.REST_AREA
        },
        notes="Quiet outdoor space with seating"
    )

    post_office_intersection = Node(
        id="post_office_intersection",
        name="Post Office Intersection",
        latitude=-34.91980688763416, 
        longitude=138.6051202466815,
        features={
            AccessibilityFeature.REST_AREA
        },
    )

    main_entrance_lawn = Node(
        id="main_entrance_lawn",
        name="Main Entrance Lawn",
        latitude=-34.9203871455419,  
        longitude=138.60514332412853,
        features={
            AccessibilityFeature.WELL_LIT
        },
    )

    main_road_south = Node(
        id = "main_road_south",
        name = "Main Road South",
        latitude=-34.92086874931701,
        longitude=138.6042519759701,
        features={AccessibilityFeature.CURB_CUT}
    )

    main_road_north = Node(
        id = "main_road_north",
        name = "Main Road North",
        latitude=-34.919562999744606,
        longitude=138.60414817720883,
        features={AccessibilityFeature.CURB_CUT}
    )

    # === LIGERTWOOD BUILDING ===
    
    ligertwood = Node(
        id="ligertwood",
        name="Ligertwood Building - Main Entrance",
        latitude=-34.92064895107989,
        longitude=138.60616141980455,
        building="Ligertwood",
        floor=0,
        features={
            AccessibilityFeature.AUTOMATIC_DOOR,
            AccessibilityFeature.RAMP
        },
        notes="Large courtyard in front"
    )

    bonythonhall = Node(
        id = "bonythonhall",
        name = "Bonython Hall",
        latitude=-34.92070163213288,
        longitude=138.6054845332078,
        building="Bonython Hall",
        floor=0,
        features={
            AccessibilityFeature.RAMP
        },
        notes="sloped"
    )

    elderhall = Node(
        id = "elderhall",
        name = "Elder Hall",
        latitude=-34.92038516757291,
        longitude=138.60500411061034,
        building = "Elder Hall",
        floor = 0,
        features={
            AccessibilityFeature.RAMP,
            AccessibilityFeature.REST_AREA
        },
    )
    
    # Add all nodes
    for node in [
        barr_smith_main, barr_smith_north, barr_smith_level1,
        hub_central, hub_east_entrance,
        ingkarni_wardli_main, ingkarni_wardli_north,
        napier_main, napier_south,
        scott_theatre,
        main_road_south, main_road_north,
        eng_north_main, eng_mathews_link,
        eng_south_1st_floor, eng_south_ground_floor,
        union_house, union_courtyard,
        horace_lamb,
        bonythonhall,
        post_office_intersection,
        elderhall,
        main_entrance_lawn,
        north_terrace_crossing, library_courtyard, ligertwood
    ]:
        graph.add_node(node)
    
    # PATHWAYS
    
    # Hub Central connections

    graph.add_edge(Edge(
        from_node="hub_central",
        to_node="hub_east_entrance",
        distance=30,
        slope=0.0,
        surface=SurfaceType.INDOOR_TILE,
        width=10,
        is_sheltered=True,
        features={AccessibilityFeature.SHELTERED}
    ))
    
    graph.add_edge(Edge(
        from_node="hub_central",
        to_node="bs_main_entrance",
        distance=110,
        slope=1.8,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.5,
        is_sheltered=True,
        features={AccessibilityFeature.SHELTERED, AccessibilityFeature.ELEVATOR}
    ))
    
    graph.add_edge(Edge(
        from_node="hub_central",
        to_node="ingkarni_wardli_main",
        distance=85,
        slope=-2,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.0,
        is_sheltered=False,
        features={AccessibilityFeature.ELEVATOR}
    ))
    
    graph.add_edge(Edge(
        from_node="hub_central",
        to_node="horace_lamb",
        distance=95,
        slope=1.2,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.0
    ))
    
    graph.add_edge(Edge(
        from_node="hub_central",
        to_node="eng_north_main",
        distance=130,
        slope=2.8,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.5
    ))

    graph.add_edge(Edge(
        from_node="hub_central",
        to_node="eng_south_1st_floor",
        distance=70,
        slope=-10,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.5,
        features={AccessibilityFeature.ELEVATOR, AccessibilityFeature.RAMP}
    ))

    graph.add_edge(Edge(
        from_node="north_terrace_crossing",
        to_node="main_road_south",
        distance=900,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=8.5,
        features={AccessibilityFeature.WELL_LIT, AccessibilityFeature.CURB_CUT}
    ))

    graph.add_edge(Edge(
        from_node="main_road_south",
        to_node="main_road_north",
        distance=120,
        slope=-5,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=7.5,
        features={AccessibilityFeature.WELL_LIT, AccessibilityFeature.CURB_CUT}
    ))

    graph.add_edge(Edge(
        from_node="bonythonhall",
        to_node="main_road_south",
        distance=50,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=7.5,
        features={AccessibilityFeature.WELL_LIT}
    ))

    graph.add_edge(Edge(
        from_node="elderhall",
        to_node="main_road_south",
        distance=30,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5.5,
        features={AccessibilityFeature.WELL_LIT}
    ))

    graph.add_edge(Edge(
        from_node="main_road_north",
        to_node="scott_theatre",
        distance=150,
        slope=2.0,
        surface=SurfaceType.ROUGH_PAVEMENT,
        width=7.5,
        features={AccessibilityFeature.CURB_CUT}
    ))
    
    # Barr Smith Library connections
    graph.add_edge(Edge(
        from_node="bs_main_entrance",
        to_node="bs_north_entrance",
        distance=45,
        slope=0.0,
        surface=SurfaceType.INDOOR_TILE,
        width=3.0,
        is_sheltered=True,
        features={AccessibilityFeature.SHELTERED, AccessibilityFeature.ELEVATOR}
    ))
    
    graph.add_edge(Edge(
        from_node="bs_main_entrance",
        to_node="library_courtyard",
        distance=45,
        slope=0.5,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=2.5
    ))

    graph.add_edge(Edge(
        from_node="main_entrance_lawn",
        to_node="post_office_intersection",
        distance=50,
        slope=-3,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5
    ))

    graph.add_edge(Edge(
        from_node="main_entrance_lawn",
        to_node="elderhall",
        distance=15,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5
    ))

    graph.add_edge(Edge(
        from_node="main_entrance_lawn",
        to_node="napier_south",
        distance=80,
        slope=-2,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5
    ))
    
    # Union House connections
    graph.add_edge(Edge(
        from_node="library_courtyard",
        to_node="union_house",
        distance=55,
        slope=0.8,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.0
    ))
    
    graph.add_edge(Edge(
        from_node="union_house",
        to_node="union_courtyard",
        distance=30,
        slope=0.0,
        surface=SurfaceType.BRICK,
        width=3.5,
        features={AccessibilityFeature.REST_AREA}
    ))
    
    graph.add_edge(Edge(
        from_node="union_courtyard",
        to_node="scott_theatre",
        distance=85,
        slope=-2.2,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=2.5,
        features={AccessibilityFeature.RAMP}
    ))

    graph.add_edge(Edge(
        from_node="scott_theatre",
        to_node="hub_central",
        distance=180,
        slope=0,
        surface=SurfaceType.ROUGH_PAVEMENT,
        width=2.5,
        features={AccessibilityFeature.RAMP}
    ))
    
    # Napier Building connections (with ramped alternative)
    graph.add_edge(Edge(
        from_node="horace_lamb",
        to_node="napier_main",
        distance=75,
        slope=3.5,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=2.5
    ))
    
    graph.add_edge(Edge(
        from_node="napier_south",
        to_node="napier_main",
        distance=40,
        slope=0.0,
        surface=SurfaceType.INDOOR_TILE,
        width=3.5,
        is_sheltered=True,
        features={AccessibilityFeature.SHELTERED}
    ))

    graph.add_edge(Edge(
        from_node="post_office_intersection",
        to_node="hub_central",
        distance=25,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=6.5,
        is_sheltered=False,
        features={AccessibilityFeature.SHELTERED}
    ))

    graph.add_edge(Edge(
        from_node="post_office_intersection",
        to_node="hub_east_entrance",
        distance=20,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5.5,
        is_sheltered=False,
        features={AccessibilityFeature.WELL_LIT}
    ))

    graph.add_edge(Edge(
        from_node="post_office_intersection",
        to_node="ingkarni_wardli_main",
        distance=60,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=4.5,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP, AccessibilityFeature.ELEVATOR}
    ))

    graph.add_edge(Edge(
        from_node="napier_south",
        to_node="elderhall",
        distance=50,
        slope=2.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5.5,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP}
    ))

    graph.add_edge(Edge(
        from_node="napier_south",
        to_node="bonythonhall",
        distance=70,
        slope=5.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=7.5,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP, AccessibilityFeature.REST_AREA}
    ))

    graph.add_edge(Edge(
        from_node="napier_main",
        to_node="eng_south_1st_floor",
        distance=30,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.0,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP}
    ))

    graph.add_edge(Edge(
        from_node="napier_main",
        to_node="elderhall",
        distance=100,
        slope=7.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=6.5,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP, AccessibilityFeature.ELEVATOR}
    ))
    
    
    # Engineering area connections
    graph.add_edge(Edge(
        from_node="eng_north_main",
        to_node="ingkarni_wardli_main",
        distance=70,
        slope=0,
        surface=SurfaceType.INDOOR_TILE,
        width=4.0,
        features={AccessibilityFeature.SHELTERED}
    ))

    graph.add_edge(Edge(
        from_node="eng_south_ground_floor",
        to_node="horace_lamb",
        distance=60,
        slope=0.0,
        surface=SurfaceType.ROUGH_PAVEMENT,
        width=8.0,
        features={AccessibilityFeature.AUTOMATIC_DOOR}
    ))

    graph.add_edge(Edge(
        from_node="eng_south_ground_floor",
        to_node="eng_mathews_link",
        distance=40,
        slope=0.0,
        surface=SurfaceType.ROUGH_PAVEMENT,
        width=8.0,
        features={AccessibilityFeature.AUTOMATIC_DOOR}
    ))

    graph.add_edge(Edge(
        from_node="eng_south_ground_floor",
        to_node="eng_north_main",
        distance=50,
        slope=0.0,
        surface=SurfaceType.INDOOR_TILE,
        width=5.0,
        features={AccessibilityFeature.AUTOMATIC_DOOR, AccessibilityFeature.SHELTERED}
    ))
    
    graph.add_edge(Edge(
        from_node="north_terrace_crossing",
        to_node="elderhall",
        distance=60,
        slope=-0.5,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5.0,
        features={AccessibilityFeature.CURB_CUT,AccessibilityFeature.WELL_LIT}
    ))

    graph.add_edge(Edge(
        from_node="north_terrace_crossing",
        to_node="bonythonhall",
        distance=50,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=8.0,
        features={AccessibilityFeature.CURB_CUT,AccessibilityFeature.WELL_LIT}
    ))

    graph.add_edge(Edge(
        from_node="bonythonhall",
        to_node="elderhall",
        distance=40,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=7.0,
        features={AccessibilityFeature.REST_AREA,AccessibilityFeature.WELL_LIT}
    ))

    graph.add_edge(Edge(
        from_node="north_terrace_crossing",
        to_node="ligertwood",
        distance=100,
        slope=0.0,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5.0,
        features={AccessibilityFeature.CURB_CUT,AccessibilityFeature.WELL_LIT, AccessibilityFeature.REST_AREA}
    ))
    
    graph.add_edge(Edge(
        from_node="ingkarni_wardli_north",
        to_node="ingkarni_wardli_main",
        distance=35,
        slope=0.0,
        surface=SurfaceType.INDOOR_TILE,
        width=4.0,
        is_sheltered=True,
        features={AccessibilityFeature.SHELTERED}
    ))
    
    # Additional alternative routes
    graph.add_edge(Edge(
        from_node="ingkarni_wardli_main",
        to_node="horace_lamb",
        distance=65,
        slope=0.5,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=3.0
    ))
    
    # Indoor elevator access in Barr Smith
    graph.add_edge(Edge(
        from_node="bs_main_entrance",
        to_node="bs_level1",
        distance=15,
        slope=0.0,
        surface=SurfaceType.INDOOR_TILE,
        width=2.0,
        is_sheltered=True,
        features={AccessibilityFeature.ELEVATOR, AccessibilityFeature.SHELTERED}
    ))

    # Ligertwood building 
    graph.add_edge(Edge(
        from_node="ligertwood",
        to_node="napier_south",
        distance=50,
        slope=-5,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=4.0,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP}
    ))

    graph.add_edge(Edge(
        from_node="elderhall",
        to_node="ligertwood",
        distance=75,
        slope=3,
        surface=SurfaceType.SMOOTH_PAVEMENT,
        width=5.0,
        is_sheltered=False,
        features={AccessibilityFeature.RAMP}
    ))


    graph.mark_path_blocked(
        "bs_level1",
        "Construction - temporary path closure",
        datetime.now() + timedelta(days = 14)
    )
    
    # Example of a temporarily difficult path (uncomment to test routing around obstacles)
    # graph.mark_path_blocked(
    #     "hub_central", 
    #     "Construction - temporary path closure",
    #     datetime.now() + timedelta(days=14)
    # )
    
    return graph


if __name__ == "__main__":
    import os
    
    # Use relative path that works from any location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_file = os.path.join(project_root, "data", "north_terrace_campus.json")
    
    # Create and save the enhanced campus
    campus = create_sample_campus()
    campus.save_to_file(data_file)
    
    print(f"✅ Enhanced campus data created!")
    print(f"📁 Saved to: {data_file}")
    print(f"\n📊 Statistics: {campus.get_statistics()}")
    
    # Print all nodes by category
    print("\n📍 Buildings and Locations:")
    buildings = {}
    outdoor = []
    
    for node_id, node in campus.nodes.items():
        if node.building:
            if node.building not in buildings:
                buildings[node.building] = []
            buildings[node.building].append(node.name)
        else:
            outdoor.append(node.name)
    
    for building, nodes in sorted(buildings.items()):
        print(f"\n  🏢 {building}:")
        for node_name in nodes:
            print(f"     - {node_name}")
    
    print(f"\n  🌳 Outdoor Spaces:")
    for node_name in outdoor:
        print(f"     - {node_name}")
    

