"""
Demo script to test the accessible campus navigation system
"""

import sys
sys.path.insert(0, 'src')

from campus_graph import CampusGraph
from pathfinding import MultiCriteriaRouter, RoutingPreference


def print_route_summary(route, preference_name):
    """Print a nice summary of a route"""
    print(f"\n{'='*60}")
    print(f"ROUTE: {preference_name.upper()}")
    print(f"{'='*60}")
    
    print(f"\n📍 Route Summary:")
    print(f"   Distance: {route.total_distance:.0f}m")
    print(f"   Estimated Time: {route.estimated_time_minutes:.0f} minutes")
    print(f"   Elevation Gain: {route.total_elevation_gain:.1f}m")
    print(f"   Elevation Loss: {route.total_elevation_loss:.1f}m")
    print(f"   Sheltered: {route.sheltered_percentage:.0f}%")
    print(f"   Accessibility Score: {route.accessibility_score:.0f}/100")
    print(f"   Rest Stops: {len(route.rest_stops)}")
    
    print(f"\n🚶 Turn-by-Turn Directions:")
    for direction in route.get_turn_by_turn_directions():
        print(f"   {direction}")


def demo_routing():
    """Demonstrate the routing system"""
    
    print("\n" + "="*60)
    print("ACCESSIBLE CAMPUS NAVIGATION - DEMO")
    print("University of Adelaide - North Terrace Campus")
    print("="*60)
    
    # Load campus data
    print("\n📂 Loading campus data...")
    campus = CampusGraph.load_from_file("data/north_terrace_campus.json")
    router = MultiCriteriaRouter(campus)
    
    print(f"\n📊 Campus Statistics:")
    stats = campus.get_statistics()
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # List available locations
    print(f"\n📍 Available Locations:")
    for i, (node_id, node) in enumerate(campus.nodes.items(), 1):
        print(f"   {i}. {node.name}")
    
    # Demo route 1: Hub Central to Barr Smith Library
    print("\n\n" + "🔍 FINDING ROUTE ".ljust(60, "="))
    print("From: Hub Central")
    print("To: Barr Smith Library - Main Entrance")
    
    start = "hub_central"
    end = "bs_main_entrance"
    
    # Find balanced route
    print("\n⏳ Calculating optimal route...")
    route = router.find_route(start, end, RoutingPreference.BALANCED)
    
    if route:
        print_route_summary(route, "Balanced")
    else:
        print("❌ No route found!")
    
    # Demo route 2: Compare alternatives
    print("\n\n" + "🔍 COMPARING ALTERNATIVE ROUTES ".ljust(60, "="))
    print("From: Engineering North Building")
    print("To: Scott Theatre")
    
    start = "eng_north"
    end = "scott_theatre"
    
    alternatives = router.find_alternative_routes(start, end, num_alternatives=4)
    
    if alternatives:
        print(f"\n✅ Found {len(alternatives)} alternative routes:\n")
        
        for i, (preference, route) in enumerate(alternatives, 1):
            print(f"\n{'─'*60}")
            print(f"OPTION {i}: {preference.value.upper().replace('_', ' ')}")
            print(f"{'─'*60}")
            print(f"Distance: {route.total_distance:.0f}m | "
                  f"Time: {route.estimated_time_minutes:.0f} min | "
                  f"Accessibility: {route.accessibility_score:.0f}/100")
            
            if preference == RoutingPreference.FLATTEST:
                print(f"💡 Minimal elevation: {route.total_elevation_gain:.1f}m gain")
            elif preference == RoutingPreference.MOST_SHELTERED:
                print(f"☂️  Sheltered coverage: {route.sheltered_percentage:.0f}%")
            elif preference == RoutingPreference.SHORTEST:
                print(f"⚡ Fastest route available")
    else:
        print("❌ No alternative routes found!")
    
    # Demo blocking a path
    print("\n\n" + "⚠️  SIMULATING PATH BLOCKAGE ".ljust(60, "="))
    print("Blocking path: Hub Central → Barr Smith Library")
    print("Reason: Elevator maintenance")
    
    campus.mark_path_blocked("hub_central", "bs_main_entrance", "Elevator maintenance")
    
    print("\n⏳ Recalculating route...")
    new_route = router.find_route("hub_central", "bs_main_entrance", RoutingPreference.BALANCED)
    
    if new_route:
        print_route_summary(new_route, "Alternative (Avoiding Blocked Path)")
        print("\n✅ Successfully found alternative route avoiding blocked path!")
    else:
        print("\n❌ No alternative route available - path is critical!")
    
    # Restore path
    campus.mark_path_accessible("hub_central", "bs_main_entrance")
    print("\n✓ Path restored to accessible status")
    
    print("\n\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\n💡 Next steps:")
    print("   1. Run 'python app.py' to start the web server")
    print("   2. Open http://localhost:5000 in your browser")
    print("   3. Add your Google Maps API key to templates/index.html")
    print("   4. Expand the campus data with actual measurements")
    print("   5. Implement suggested enhancements from README.md")
    print("\n")


if __name__ == "__main__":
    demo_routing()
