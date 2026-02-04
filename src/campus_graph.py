"""
Represent the campus as a weighted graph with accessibility features
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import json
from datetime import datetime


class SurfaceType(Enum):
    """Types of surface materials"""
    SMOOTH_PAVEMENT = "smooth_pavement"
    ROUGH_PAVEMENT = "rough_pavement"
    BRICK = "brick"
    GRAVEL = "gravel"
    GRASS = "grass"
    INDOOR_TILE = "indoor_tile"
    INDOOR_CARPET = "indoor_carpet"


class AccessibilityFeature(Enum):
    """Accessibility features along routes"""
    RAMP = "ramp"
    ELEVATOR = "elevator"
    AUTOMATIC_DOOR = "automatic_door"
    CURB_CUT = "curb_cut"
    REST_AREA = "rest_area"
    ACCESSIBLE_BATHROOM = "accessible_bathroom"
    SHELTERED = "sheltered"
    WELL_LIT = "well_lit"
    HANDRAILS = "handrails"


@dataclass
class Node:
    id: str
    name: str
    latitude: float
    longitude: float
    building: Optional[str] = None
    floor: int = 0
    features: Set[AccessibilityFeature] = field(default_factory=set)
    is_indoor: bool = False
    notes: str = ""
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "building": self.building,
            "floor": self.floor,
            "features": [f.value for f in self.features],
            "is_indoor": self.is_indoor,
            "notes": self.notes
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Node':
        features = {AccessibilityFeature(f) for f in data.get("features", [])}
        return Node(
            id=data["id"],
            name=data["name"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            building=data.get("building"),
            floor=data.get("floor", 0),
            features=features,
            is_indoor=data.get("is_indoor", False),
            notes=data.get("notes", "")
        )


@dataclass
class Edge:
    from_node: str
    to_node: str
    distance: float  
    slope: float = 0.0  # percentage grade (positive = uphill, negative = downhill)
    surface: SurfaceType = SurfaceType.SMOOTH_PAVEMENT
    width: float = 2.0 
    is_bidirectional: bool = True
    is_sheltered: bool = False
    features: Set[AccessibilityFeature] = field(default_factory=set)
    is_accessible: bool = True  # Can be set to False if blocked
    blocked_reason: Optional[str] = None
    blocked_until: Optional[datetime] = None
    
    def get_reverse_edge(self) -> 'Edge':
        """Returns the reverse direction of this edge"""
        return Edge(
            from_node=self.to_node,
            to_node=self.from_node,
            distance=self.distance,
            slope=-self.slope,  # Reverse the slope
            surface=self.surface,
            width=self.width,
            is_bidirectional=self.is_bidirectional,
            is_sheltered=self.is_sheltered,
            features=self.features.copy(),
            is_accessible=self.is_accessible,
            blocked_reason=self.blocked_reason,
            blocked_until=self.blocked_until
        )
    
    def to_dict(self) -> dict:
        return {
            "from_node": self.from_node,
            "to_node": self.to_node,
            "distance": self.distance,
            "slope": self.slope,
            "surface": self.surface.value,
            "width": self.width,
            "is_bidirectional": self.is_bidirectional,
            "is_sheltered": self.is_sheltered,
            "features": [f.value for f in self.features],
            "is_accessible": self.is_accessible,
            "blocked_reason": self.blocked_reason,
            "blocked_until": self.blocked_until.isoformat() if self.blocked_until else None
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Edge':
        features = {AccessibilityFeature(f) for f in data.get("features", [])}
        blocked_until = None
        if data.get("blocked_until"):
            blocked_until = datetime.fromisoformat(data["blocked_until"])
        
        return Edge(
            from_node=data["from_node"],
            to_node=data["to_node"],
            distance=data["distance"],
            slope=data.get("slope", 0.0),
            surface=SurfaceType(data.get("surface", "smooth_pavement")),
            width=data.get("width", 2.0),
            is_bidirectional=data.get("is_bidirectional", True),
            is_sheltered=data.get("is_sheltered", False),
            features=features,
            is_accessible=data.get("is_accessible", True),
            blocked_reason=data.get("blocked_reason"),
            blocked_until=blocked_until
        )


class CampusGraph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}  # from_node -> list of edges
        self.metadata = {
            "campus_name": "University of Adelaide - North Terrace Campus",
            "last_updated": datetime.now().isoformat(),
            "contributors": []
        }
    
    def add_node(self, node: Node) -> None:
        """Add a node to the graph"""
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = []
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph"""
        if edge.from_node not in self.edges:
            self.edges[edge.from_node] = []
        
        self.edges[edge.from_node].append(edge)
        
        # Add reverse edge if bidirectional
        if edge.is_bidirectional:
            reverse_edge = edge.get_reverse_edge()
            if edge.to_node not in self.edges:
                self.edges[edge.to_node] = []
            self.edges[edge.to_node].append(reverse_edge)
    
    def get_neighbors(self, node_id: str, accessible_only: bool = True) -> List[Tuple[str, Edge]]:
        """
        Get all neighboring nodes from a given node
        Returns list of (neighbor_id, edge) tuples
        """
        if node_id not in self.edges:
            return []
        
        neighbors = []
        for edge in self.edges[node_id]:
            if accessible_only and not edge.is_accessible:
                continue
            neighbors.append((edge.to_node, edge))
        
        return neighbors
    
    def mark_path_blocked(self, from_node: str, to_node: str, reason: str, until: Optional[datetime] = None) -> bool:
        if from_node not in self.edges:
            return False
        
        updated = False
        for edge in self.edges[from_node]:
            if edge.to_node == to_node:
                edge.is_accessible = False
                edge.blocked_reason = reason
                edge.blocked_until = until
                updated = True
        
        # Also update reverse direction if exists
        if to_node in self.edges:
            for edge in self.edges[to_node]:
                if edge.to_node == from_node:
                    edge.is_accessible = False
                    edge.blocked_reason = reason
                    edge.blocked_until = until
        
        return updated
    
    def mark_path_accessible(self, from_node: str, to_node: str) -> bool:
        """Mark a path as accessible again"""
        if from_node not in self.edges:
            return False
        
        updated = False
        for edge in self.edges[from_node]:
            if edge.to_node == to_node:
                edge.is_accessible = True
                edge.blocked_reason = None
                edge.blocked_until = None
                updated = True
        
        # Also update reverse direction
        if to_node in self.edges:
            for edge in self.edges[to_node]:
                if edge.to_node == from_node:
                    edge.is_accessible = True
                    edge.blocked_reason = None
                    edge.blocked_until = None
        
        return updated
    
    def save_to_file(self, filename: str) -> None:
        data = {
            "metadata": self.metadata,
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": []
        }
        
        # Only save one direction of bidirectional edges to avoid duplication
        seen_pairs = set()
        for node_id, edge_list in self.edges.items():
            for edge in edge_list:
                pair = tuple(sorted([edge.from_node, edge.to_node]))
                if pair not in seen_pairs or not edge.is_bidirectional:
                    data["edges"].append(edge.to_dict())
                    if edge.is_bidirectional:
                        seen_pairs.add(pair)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_from_file(filename: str) -> 'CampusGraph':
        with open(filename, 'r') as f:
            data = json.load(f)
        
        graph = CampusGraph()
        graph.metadata = data.get("metadata", graph.metadata)
        
        # Load nodes
        for node_data in data.get("nodes", []):
            graph.add_node(Node.from_dict(node_data))
        
        # Load edges
        for edge_data in data.get("edges", []):
            graph.add_edge(Edge.from_dict(edge_data))
        
        return graph
    
    def get_statistics(self) -> dict:
        total_distance = sum(
            edge.distance 
            for edges in self.edges.values() 
            for edge in edges
        ) / 2  # Divide by 2 for bidirectional edges
        
        blocked_paths = sum(
            1 for edges in self.edges.values() 
            for edge in edges 
            if not edge.is_accessible
        )
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len([e for edges in self.edges.values() for e in edges]) // 2,
            "total_distance_km": round(total_distance / 1000, 2),
            "blocked_paths": blocked_paths,
            "buildings": len(set(n.building for n in self.nodes.values() if n.building))
        }
