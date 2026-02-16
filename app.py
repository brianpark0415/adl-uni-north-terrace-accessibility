from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from campus_graph import CampusGraph, Node, Edge, AccessibilityFeature, SurfaceType
from pathfinding import MultiCriteriaRouter, RoutingPreference

app = Flask(__name__)
CORS(app)

# Global graph
CAMPUS_DATA_FILE = "data/north_terrace_campus.json"
campus_graph = None
router = None


def load_campus_data():
    """Load campus data from file"""
    global campus_graph, router
    try:
        campus_graph = CampusGraph.load_from_file(CAMPUS_DATA_FILE)
        router = MultiCriteriaRouter(campus_graph)
        print(f"Loaded campus data: {campus_graph.get_statistics()}")
    except FileNotFoundError:
        print("Campus data file not found. Creating sample data...")
        from sample_data import create_sample_campus
        campus_graph = create_sample_campus()
        campus_graph.save_to_file(CAMPUS_DATA_FILE)
        router = MultiCriteriaRouter(campus_graph)


# === API Endpoints ===

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        "google_maps_api_key": os.getenv('GOOGLE_MAPS_API_KEY', '')
    })


@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    nodes = [node.to_dict() for node in campus_graph.nodes.values()]
    return jsonify(nodes)


@app.route('/api/nodes/<node_id>', methods=['GET'])
def get_node(node_id):
    if node_id not in campus_graph.nodes:
        return jsonify({"error": "Node not found"}), 404
    return jsonify(campus_graph.nodes[node_id].to_dict())


@app.route('/api/nodes', methods=['POST'])
def add_node():
    """Add a new node (collaborative editing)"""
    try:
        data = request.json
        node = Node.from_dict(data)
        campus_graph.add_node(node)
        campus_graph.save_to_file(CAMPUS_DATA_FILE)
        return jsonify({"success": True, "node": node.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/edges', methods=['POST'])
def add_edge():
    """Add a new edge (collaborative editing)"""
    try:
        data = request.json
        edge = Edge.from_dict(data)
        campus_graph.add_edge(edge)
        campus_graph.save_to_file(CAMPUS_DATA_FILE)
        return jsonify({"success": True, "edge": edge.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/route', methods=['POST'])
def find_route():
    try:
        data = request.json
        start = data.get('start')
        end = data.get('end')
        preference_str = data.get('preference', 'balanced')
        max_slope = data.get('max_slope', 8.0)
        min_width = data.get('min_width', 1.2)
        
        # Convert preference string to enum
        preference = RoutingPreference(preference_str.lower())
        
        # Find route
        route = router.find_route(start, end, preference, max_slope, min_width)
        
        if route is None:
            return jsonify({"error": "No accessible route found"}), 404
        
        return jsonify(route.to_dict())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/route/alternatives', methods=['POST'])
def find_alternative_routes():
    try:
        data = request.json
        start = data.get('start')
        end = data.get('end')
        num_alternatives = data.get('num_alternatives', 3)
        
        routes = router.find_alternative_routes(start, end, num_alternatives)
        
        result = [
            {
                "preference": pref.value,
                "route": route.to_dict()
            }
            for pref, route in routes
        ]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/block_path', methods=['POST'])
def block_path():
    try:
        data = request.json
        from_node = data.get('from_node')
        to_node = data.get('to_node')
        reason = data.get('reason')
        until_str = data.get('until')
        
        until = None
        if until_str:
            from datetime import datetime
            until = datetime.fromisoformat(until_str)
        
        success = campus_graph.mark_path_blocked(from_node, to_node, reason, until)
        
        if success:
            campus_graph.save_to_file(CAMPUS_DATA_FILE)
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Path not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/unblock_path', methods=['POST'])
def unblock_path():
    """Mark a path as accessible again"""
    try:
        data = request.json
        from_node = data.get('from_node')
        to_node = data.get('to_node')
        
        success = campus_graph.mark_path_accessible(from_node, to_node)
        
        if success:
            campus_graph.save_to_file(CAMPUS_DATA_FILE)
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Path not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get campus statistics"""
    return jsonify(campus_graph.get_statistics())


@app.route('/api/export', methods=['GET'])
def export_data():
    """Export complete campus data"""
    with open(CAMPUS_DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Accessible Campus Navigation Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on (default: 8080)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on (default: 0.0.0.0)')
    args = parser.parse_args()
    
    load_campus_data()
    print(f"\n🚀 Starting server on http://localhost:{args.port}")
    print(f"   Press Ctrl+C to stop\n")
    app.run(debug=True, host=args.host, port=args.port)
