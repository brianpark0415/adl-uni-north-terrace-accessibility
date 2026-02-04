import heapq
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import math

from campus_graph import CampusGraph, Node, Edge, AccessibilityFeature, SurfaceType


class RoutingPreference(Enum):
    """Different routing optimization preferences"""
    SHORTEST = "shortest"  # Minimize distance
    FLATTEST = "flattest"  # Minimize slope changes
    MOST_SHELTERED = "most_sheltered"  # Maximize sheltered paths
    WITH_REST_STOPS = "with_rest_stops"  # Prefer routes with rest areas
    BALANCED = "balanced"  # Balance multiple factors


@dataclass
class RouteSegment:
    """A segment of the route"""
    from_node: Node
    to_node: Node
    edge: Edge
    cumulative_distance: float
    cumulative_elevation_change: float


@dataclass
class Route:
    """A complete route from start to destination"""
    segments: List[RouteSegment]
    total_distance: float
    total_elevation_gain: float
    total_elevation_loss: float
    sheltered_percentage: float
    rest_stops: List[Node]
    estimated_time_minutes: float
    accessibility_score: float
    
    def get_turn_by_turn_directions(self) -> List[str]:
        """Generate human-readable directions"""
        directions = []
        
        for i, segment in enumerate(self.segments):
            direction = f"{i+1}. From {segment.from_node.name} to {segment.to_node.name}"
            
            # Add distance
            direction += f" ({segment.edge.distance:.0f}m)"
            
            # Add slope info
            if abs(segment.edge.slope) > 2:
                slope_desc = "uphill" if segment.edge.slope > 0 else "downhill"
                direction += f" - {slope_desc} ({abs(segment.edge.slope):.1f}% grade)"
            
            # Add surface info
            if segment.edge.surface != SurfaceType.SMOOTH_PAVEMENT:
                direction += f" - {segment.edge.surface.value.replace('_', ' ')}"
            
            # Add features
            if segment.edge.features:
                features_str = ", ".join([f.value.replace('_', ' ') for f in segment.edge.features])
                direction += f" - Features: {features_str}"
            
            directions.append(direction)
        
        # Add summary
        summary = f"\nTotal distance: {self.total_distance:.0f}m (~{self.estimated_time_minutes:.0f} min)"
        if self.total_elevation_gain > 1:
            summary += f"\nElevation gain: {self.total_elevation_gain:.1f}m"
        if self.sheltered_percentage > 50:
            summary += f"\n{self.sheltered_percentage:.0f}% of route is sheltered"
        if self.rest_stops:
            summary += f"\nRest stops available: {len(self.rest_stops)}"
        
        directions.append(summary)
        return directions
    
    def to_dict(self) -> dict:
        """Convert route to dictionary for JSON serialization"""
        return {
            "segments": [
                {
                    "from": seg.from_node.to_dict(),
                    "to": seg.to_node.to_dict(),
                    "distance": seg.edge.distance,
                    "slope": seg.edge.slope,
                    "surface": seg.edge.surface.value,
                    "features": [f.value for f in seg.edge.features],
                    "is_sheltered": seg.edge.is_sheltered
                }
                for seg in self.segments
            ],
            "summary": {
                "total_distance": self.total_distance,
                "total_elevation_gain": self.total_elevation_gain,
                "total_elevation_loss": self.total_elevation_loss,
                "sheltered_percentage": self.sheltered_percentage,
                "estimated_time_minutes": self.estimated_time_minutes,
                "accessibility_score": self.accessibility_score,
                "rest_stops_count": len(self.rest_stops)
            },
            "directions": self.get_turn_by_turn_directions()
        }


class MultiCriteriaRouter:
    """
    Multi-criteria pathfinding router using A* algorithm with customizable cost functions
    """
    
    def __init__(self, campus_graph: CampusGraph):
        self.graph = campus_graph
    
    def _heuristic(self, node1_id: str, node2_id: str) -> float:
        """
        Heuristic function for A* (straight-line distance)
        """
        node1 = self.graph.nodes[node1_id]
        node2 = self.graph.nodes[node2_id]
        
        # Haversine formula for geographic distance
        lat1, lon1 = math.radians(node1.latitude), math.radians(node1.longitude)
        lat2, lon2 = math.radians(node2.latitude), math.radians(node2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in meters
        r = 6371000
        return r * c
    
    def _calculate_edge_cost(
        self, 
        edge: Edge, 
        preference: RoutingPreference,
        max_slope: float = 8.0
    ) -> float:
        """
        Calculate the cost of traversing an edge based on routing preference
        Enhanced to better consider real accessibility needs
        """
        if not edge.is_accessible:
            return float('inf')
        
        base_cost = edge.distance
        
        if preference == RoutingPreference.SHORTEST:
            # Simple distance-based cost, but still penalize very steep slopes
            if abs(edge.slope) > 5:
                return base_cost * (1 + abs(edge.slope) / 20)
            return base_cost
        
        elif preference == RoutingPreference.FLATTEST:
            # Heavily penalize slopes - this is critical for wheelchair users
            # Exponential penalty for steeper slopes
            if abs(edge.slope) < 1:
                slope_penalty = 1.0  # No penalty for nearly flat
            elif abs(edge.slope) < 3:
                slope_penalty = 1.5  # Mild penalty
            elif abs(edge.slope) < 5:
                slope_penalty = 2.5  # Moderate penalty
            elif abs(edge.slope) < 7:
                slope_penalty = 4.0  # Strong penalty
            else:
                slope_penalty = 8.0  # Very strong penalty (still passable but avoid)
            
            # Additional penalty for going uphill vs downhill
            direction_penalty = 1.0
            if edge.slope > 0:  # Uphill is harder
                direction_penalty = 1.5
            
            surface_penalty = self._get_surface_penalty(edge.surface)
            
            return base_cost * slope_penalty * direction_penalty * surface_penalty
        
        elif preference == RoutingPreference.MOST_SHELTERED:
            # Strongly prefer sheltered paths
            shelter_penalty = 1.0 if edge.is_sheltered else 3.0
            
            # Still consider slope somewhat
            slope_consideration = 1.0
            if abs(edge.slope) > 5:
                slope_consideration = 1.5
            
            return base_cost * shelter_penalty * slope_consideration
        
        elif preference == RoutingPreference.WITH_REST_STOPS:
            # Prefer routes with rest stops, but this is handled more in route selection
            # Still penalize difficult terrain
            slope_penalty = 1.0 + (abs(edge.slope) ** 1.2) / 15
            surface_penalty = self._get_surface_penalty(edge.surface)
            return base_cost * slope_penalty * surface_penalty
        
        elif preference == RoutingPreference.BALANCED:
            # Balance all factors with realistic weights
            
            # Slope penalty (progressive)
            if abs(edge.slope) < 2:
                slope_penalty = 1.0
            elif abs(edge.slope) < 4:
                slope_penalty = 1.3
            elif abs(edge.slope) < 6:
                slope_penalty = 1.8
            else:
                slope_penalty = 2.5
            
            # Uphill is harder than downhill
            if edge.slope > 3:
                slope_penalty *= 1.3
            elif edge.slope < -3:
                slope_penalty *= 0.9  # Downhill is slightly easier
            
            # Surface quality matters
            surface_penalty = self._get_surface_penalty(edge.surface)
            
            # Shelter bonus
            shelter_bonus = 0.85 if edge.is_sheltered else 1.0
            
            # Bonus for paths with handrails on slopes
            handrail_bonus = 1.0
            if abs(edge.slope) > 3 and AccessibilityFeature.HANDRAILS in edge.features:
                handrail_bonus = 0.9
            
            return base_cost * slope_penalty * surface_penalty * shelter_bonus * handrail_bonus
        
        return base_cost
    
    def _get_surface_penalty(self, surface: SurfaceType) -> float:
        """
        Get penalty multiplier based on surface type
        Enhanced penalties based on real wheelchair/mobility aid experiences
        """
        penalties = {
            SurfaceType.SMOOTH_PAVEMENT: 1.0,      # Ideal
            SurfaceType.INDOOR_TILE: 1.0,          # Ideal, smooth
            SurfaceType.INDOOR_CARPET: 1.15,       # Slightly harder to push through
            SurfaceType.ROUGH_PAVEMENT: 1.35,      # Cracks and bumps
            SurfaceType.BRICK: 1.6,                # Bumpy, gaps between bricks
            SurfaceType.GRAVEL: 2.5,               # Very difficult for wheelchairs
            SurfaceType.GRASS: 3.0                 # Often impassable when wet
        }
        return penalties.get(surface, 1.0)
    
    def find_route(
        self,
        start_node_id: str,
        end_node_id: str,
        preference: RoutingPreference = RoutingPreference.BALANCED,
        max_slope: float = 8.0,
        min_width: float = 1.2
    ) -> Optional[Route]:
        """
        Find the optimal route using A* algorithm with multi-criteria optimization
        
        Args:
            start_node_id: Starting node ID
            end_node_id: Destination node ID
            preference: Routing preference (shortest, flattest, etc.)
            max_slope: Maximum acceptable slope percentage
            min_width: Minimum acceptable path width in meters
        
        Returns:
            Route object if path found, None otherwise
        """
        if start_node_id not in self.graph.nodes or end_node_id not in self.graph.nodes:
            return None
        
        # Priority queue: (f_score, g_score, node_id, path)
        open_set = [(0, 0, start_node_id, [])]
        closed_set = set()
        
        # Best known cost to reach each node
        g_scores = {start_node_id: 0}
        
        while open_set:
            f_score, g_score, current_id, path = heapq.heappop(open_set)
            
            if current_id in closed_set:
                continue
            
            if current_id == end_node_id:
                # Found the destination, construct the route
                return self._construct_route(path)
            
            closed_set.add(current_id)
            
            # Explore neighbors
            for neighbor_id, edge in self.graph.get_neighbors(current_id):
                if neighbor_id in closed_set:
                    continue
                
                # Check constraints
                if abs(edge.slope) > max_slope or edge.width < min_width:
                    continue
                
                # Calculate cost
                edge_cost = self._calculate_edge_cost(edge, preference, max_slope)
                tentative_g_score = g_score + edge_cost
                
                if neighbor_id not in g_scores or tentative_g_score < g_scores[neighbor_id]:
                    g_scores[neighbor_id] = tentative_g_score
                    h_score = self._heuristic(neighbor_id, end_node_id)
                    f_score = tentative_g_score + h_score
                    
                    new_path = path + [(current_id, neighbor_id, edge)]
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor_id, new_path))
        
        # No path found
        return None
    
    def _construct_route(self, path: List[Tuple[str, str, Edge]]) -> Route:
        """Construct a Route object from the path"""
        segments = []
        total_distance = 0
        total_elevation_gain = 0
        total_elevation_loss = 0
        sheltered_distance = 0
        rest_stops = []
        
        for from_id, to_id, edge in path:
            from_node = self.graph.nodes[from_id]
            to_node = self.graph.nodes[to_id]
            
            # Calculate cumulative elevation change
            elevation_change = edge.distance * edge.slope / 100
            if elevation_change > 0:
                total_elevation_gain += elevation_change
            else:
                total_elevation_loss += abs(elevation_change)
            
            segment = RouteSegment(
                from_node=from_node,
                to_node=to_node,
                edge=edge,
                cumulative_distance=total_distance + edge.distance,
                cumulative_elevation_change=total_elevation_gain - total_elevation_loss
            )
            segments.append(segment)
            
            total_distance += edge.distance
            
            if edge.is_sheltered:
                sheltered_distance += edge.distance
            
            if AccessibilityFeature.REST_AREA in to_node.features:
                rest_stops.append(to_node)
        
        # Calculate metrics
        sheltered_percentage = (sheltered_distance / total_distance * 100) if total_distance > 0 else 0
        
        # Estimate time (assuming ~3 km/h for accessible walking with mobility aids)
        # Adjust for slope
        base_time_hours = total_distance / 3000
        slope_adjustment = (total_elevation_gain / 10) / 60  # Add time for elevation
        estimated_time_minutes = (base_time_hours + slope_adjustment) * 60
        
        # Calculate accessibility score (0-100, higher is better)
        accessibility_score = self._calculate_accessibility_score(segments)
        
        return Route(
            segments=segments,
            total_distance=total_distance,
            total_elevation_gain=total_elevation_gain,
            total_elevation_loss=total_elevation_loss,
            sheltered_percentage=sheltered_percentage,
            rest_stops=rest_stops,
            estimated_time_minutes=estimated_time_minutes,
            accessibility_score=accessibility_score
        )
    
    def _calculate_accessibility_score(self, segments: List[RouteSegment]) -> float:
        """
        Calculate overall accessibility score for the route
        Higher score = more accessible
        """
        if not segments:
            return 0
        
        score = 100.0
        
        for segment in segments:
            edge = segment.edge
            
            # Penalize steep slopes
            if abs(edge.slope) > 5:
                score -= abs(edge.slope) * 2
            
            # Penalize poor surfaces
            if edge.surface in [SurfaceType.GRAVEL, SurfaceType.GRASS]:
                score -= 10
            elif edge.surface in [SurfaceType.BRICK, SurfaceType.ROUGH_PAVEMENT]:
                score -= 5
            
            # Reward sheltered paths
            if edge.is_sheltered:
                score += 2
            
            # Reward accessibility features
            score += len(edge.features) * 3
        
        return max(0, min(100, score))
    
    def find_alternative_routes(
        self,
        start_node_id: str,
        end_node_id: str,
        num_alternatives: int = 3
    ) -> List[Route]:
        """
        Find multiple alternative routes with different optimization criteria
        """
        routes = []
        preferences = [
            RoutingPreference.SHORTEST,
            RoutingPreference.FLATTEST,
            RoutingPreference.MOST_SHELTERED,
            RoutingPreference.BALANCED
        ]
        
        for preference in preferences[:num_alternatives]:
            route = self.find_route(start_node_id, end_node_id, preference)
            if route:
                routes.append((preference, route))
        
        return routes
