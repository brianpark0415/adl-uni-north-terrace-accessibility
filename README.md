# Accessible Campus Navigation System
## University of Adelaide - North Terrace Campus

A comprehensive routing system designed to help people with mobility challenges navigate the University of Adelaide's North Terrace campus efficiently and safely.

## Features

### 1. Multi-Criteria Route Optimisation
- Shortest Route: Minimises total distance
- Flattest Route: Avoids steep slopes and elevation changes
- Most Sheltered Route: Maximises coverage from the weather
- Balanced Route: Optimises across all factors

### 2. Google Maps Integration
- Interactive campus map with all accessible routes
- Visual route display with turn-by-turn directions

### 3. Collaborative Editing System
- Report temporarily blocked paths (elevator maintenance, construction)
- Community-driven data updates
- Real-time campus statistics

## Technical Architecture

### Core Components

1. **Campus Graph Model** (`campus_graph.py`)
   - Node-based representation of campus locations
   - Edge-based pathways with accessibility attributes
   - Support for:
     - Slope gradients
     - Surface types (smooth pavement, brick, grass, etc.)
     - Accessibility features (ramps, elevators, automatic doors)
     - Width measurements
     - Shelter status
     - Temporary blockages

2. **Multi-Criteria Pathfinding** (`pathfinding.py`)
   - A* algorithm with customizable cost functions
   - Supports multiple routing preferences
   - Calculates:
     - Total distance and time
     - Elevation gain/loss
     - Sheltered percentage
     - Accessibility score (0-100)
     - Rest stop locations

3. **REST API** (`app.py`)
   - Flask-based backend
   - Endpoints for:
     - Route finding (single and multiple alternatives)
     - Node/edge management
     - Path blocking/unblocking
     - Data export
     - Statistics

4. **Web Interface** (`templates/index.html`)
   - Interactive Google Maps integration
   - Route preference selection
   - Turn-by-turn directions
   - Collaborative editing interface
   - Real-time statistics dashboard

## Installation

### Prerequisites
- Python 3.8+
- Google Maps API key (for map display)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd accessible-campus-nav
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate sample data** (if needed)
```bash
python src/sample_data.py
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Google Maps API key
# GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

5. **Run the application**
```bash
python app.py
```

6. **Access the interface**
Open your browser to `http://localhost:8080` (or port 5000 if not in use)


## Usage

### Finding a Route

1. Select your starting point from the dropdown
2. Select your destination
3. Choose your route preference:
   - **Balanced**: Best overall route
   - **Shortest**: Quickest distance
   - **Flattest**: Minimal slopes
   - **Sheltered**: Maximum weather protection
4. Click "Find Route" to see results

### Viewing Alternative Routes

Click "Compare Alternatives" to see multiple route options side-by-side, each optimized for different criteria.

### Contributing Data

1. Switch to the "Contribute" tab
2. Report blocked paths by selecting from/to locations
3. Provide a description of the issue
4. Submit the report

## API Documentation

### Find Route
```bash
POST /api/route
Content-Type: application/json

{
  "start": "node_id",
  "end": "node_id",
  "preference": "balanced|shortest|flattest|most_sheltered",
  "max_slope": 8.0,
  "min_width": 1.2
}
```

### Find Alternative Routes
```bash
POST /api/route/alternatives
Content-Type: application/json

{
  "start": "node_id",
  "end": "node_id",
  "num_alternatives": 3
}
```

### Get All Nodes
```bash
GET /api/nodes
```

### Add Node (Collaborative Editing)
```bash
POST /api/nodes
Content-Type: application/json

{
  "id": "new_node_id",
  "name": "Building Name",
  "latitude": -34.9195,
  "longitude": 138.6055,
  "building": "Building Name",
  "floor": 0,
  "features": ["automatic_door", "elevator"],
  "notes": "Additional information"
}
```

### Block Path
```bash
POST /api/block_path
Content-Type: application/json

{
  "from_node": "node_id_1",
  "to_node": "node_id_2",
  "reason": "Elevator maintenance",
  "until": "2024-12-31T23:59:59"
}
```

### Get Statistics
```bash
GET /api/statistics
```

## Customization

### Adding New Buildings/Nodes

Edit `src/sample_data.py` and add new nodes:

```python
new_building = Node(
    id="building_id",
    name="Building Name - Entrance",
    latitude=-34.9200,
    longitude=138.6050,
    building="Building Name",
    features={
        AccessibilityFeature.AUTOMATIC_DOOR,
        AccessibilityFeature.ELEVATOR,
        AccessibilityFeature.ACCESSIBLE_BATHROOM
    }
)
graph.add_node(new_building)
```

### Adding New Pathways/Edges

```python
graph.add_edge(Edge(
    from_node="node_1",
    to_node="node_2",
    distance=100,  # meters
    slope=2.5,     # percentage
    surface=SurfaceType.SMOOTH_PAVEMENT,
    width=3.0,     # meters
    is_sheltered=True,
    features={AccessibilityFeature.SHELTERED}
))
```

### Adjusting Cost Functions

Modify `_calculate_edge_cost()` in `pathfinding.py` to customise how routes are optimised:

```python
def _calculate_edge_cost(self, edge, preference, max_slope):
    base_cost = edge.distance
    
    # Add custom penalties/bonuses
    if preference == RoutingPreference.CUSTOM:
        # Your custom logic here
        return base_cost * custom_multiplier
```

## 📁 Project Structure

```
accessible-campus-nav/
├── src/
│   ├── campus_graph.py      # Core graph data structure
│   ├── pathfinding.py        # Multi-criteria routing algorithms
│   └── sample_data.py        # Sample campus data generator
├── data/
│   └── north_terrace_campus.json  # Campus graph data
├── templates/
│   └── index.html            # Web interface
├── static/                   # CSS, JS, images (if needed)
├── app.py                    # Flask REST API
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 📝 Data Format

Campus data is stored in JSON format:

```json
{
  "metadata": {
    "campus_name": "University of Adelaide - North Terrace Campus",
    "last_updated": "2024-02-02T00:00:00",
    "contributors": []
  },
  "nodes": [
    {
      "id": "node_id",
      "name": "Location Name",
      "latitude": -34.9195,
      "longitude": 138.6055,
      "features": ["elevator", "automatic_door"]
    }
  ],
  "edges": [
    {
      "from_node": "node_1",
      "to_node": "node_2",
      "distance": 100,
      "slope": 2.5,
      "surface": "smooth_pavement",
      "is_accessible": true
    }
  ]
}
```

## Security Considerations

- Input validation on all API endpoints
- Rate limiting for collaborative editing
- Authentication system for administrative changes
- Data backup and version control

## Authors

Brian Park

## Acknowledgments

- University of Adelaide for campus inspiration
- Open-source routing algorithms
- Accessibility advocacy groups

## Contact

For questions, suggestions, or collaboration opportunities:
brianpark0415@gmail.com

---
