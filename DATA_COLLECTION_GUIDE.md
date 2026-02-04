# Campus Data Collection Guide

## How to Expand and Improve the Campus Map

This guide helps you collect accurate data to expand the accessible navigation system.

## What Data to Collect

### For Each Building/Location:

1. **Basic Information**
   - Building name
   - Main accessible entrance location
   - GPS coordinates (use Google Maps or a GPS app)
   - Floor number (ground = 0)

2. **Accessibility Features**
   - ✅ Automatic doors
   - ✅ Elevators
   - ✅ Ramps
   - ✅ Accessible bathrooms
   - ✅ Rest areas with seating
   - ✅ Curb cuts
   - ✅ Handrails
   - ✅ Well-lit areas

3. **Additional Notes**
   - Operating hours (if restricted)
   - Temporary conditions
   - Alternative entrances

### For Each Pathway:

1. **Physical Measurements**
   - Distance (use Google Maps measurement tool)
   - Width (minimum clearance)
   - Slope/grade (use smartphone app like Clinometer)
   - Surface type (smooth pavement, brick, etc)

2. **Accessibility Features**
   - Is it sheltered? (covered walkway, building connection)
   - Are there handrails?
   - Are there rest areas along the way?
   - Automatic doors at entry/exit points?

3. **Conditions**
   - Is it always accessible?
   - Are there stairs as an alternative?
   - Weather-dependent conditions?

## Tools Needed

### Essential
- Smartphone with GPS
- Google Maps (for coordinates and distances)
- Notes app or form

### Helpful
- Measuring wheel or laser distance measurer
- Clinometer app (for measuring slopes)
- Camera (for documentation)
- Clipboard and paper maps

## 📱 Recommended Apps

1. **Clinometer** (iOS/Android)
   - Measure slope percentages accurately

2. **Google Maps**
   - Right-click → "Measure distance"
   - Get coordinates: Right-click → "What's here?"


## Data Collection Template

### Node Template
```
Node ID: [short_unique_id]
Name: [Full descriptive name]
Latitude: Use Google Maps -> right click on location -> copy/paste latitude
Longitude: Use Google Maps -> right click on location -> copy/paste longitude
Building: [Building name or null]
Floor: [0 for ground level]
Features: [list of features]
Notes: [Any additional information]
```

### Edge Template
```
From: [node_id_1]
To: [node_id_2]
Distance: [metres]
Slope: [percentage, positive=uphill, negative=downhill]
Surface: [smooth_pavement|brick|gravel|grass|etc]
Width: [metres]
Sheltered: [yes/no]
Features: [list of features]
Notes: [Any additional information]
```

## Priority Areas to Map

### High Priority (Most Used)
1. **Main library entrances**
   - Barr Smith Library all accessible entrances
   
2. **Lecture theaters**
   - Scott Theatre
   - Napier Lecture Theatres

3. **Student services**
   - Hub Central
   - Student center
   - Medical services

4. **Major academic buildings**
   - Engineering buildings
   - Sciences buildings
   - Arts buildings

### Medium Priority
5. **F&B areas**
   - Union House
   - Uni Bar

6. **Student Accomodations**
   - If applicable

### Lower Priority
7. **Auxiliary buildings**
   - Administrative offices
   - Maintenance facilities

## Measuring Slopes

Slope is critical for accessibility. Here's how to measure:

1. **Using a smartphone app:**
   - Place phone flat on the pathway
   - Walk along the path
   - Note the maximum slope

2. **Converting measurements:**
   - App shows degrees? Convert to percentage: tan(angle) × 100
   - Example: 5° = tan(5°) × 100 = 8.7% slope

3. **Accessibility guidelines:**
   - **≤ 5%**: Accessible without assistance
   - **5-8%**: Manageable for most wheelchair users
   - **> 8%**: May require assistance
   - **> 12%**: Generally not accessible

## 📊 How to Add Data to the System

### Method 1: Via Web Interface
1. Go to the "Contribute" tab
2. Use the collaborative editing features
3. Submit new nodes and edges

### Method 2: Via Code
Edit `src/sample_data.py`:

```python
# Add a new node
new_building = Node(
    id="your_building_id",  # Use lowercase, underscores
    name="Your Building Name - Entrance",
    latitude=-34.XXXXXXXXX,
    longitude=138.XXXXXXXXX,
    building="Your Building Name",
    floor=0,
    features={
        AccessibilityFeature.AUTOMATIC_DOOR,
        AccessibilityFeature.ELEVATOR
    },
    notes="Any special notes"
)
graph.add_node(new_building)

# Add a new pathway
graph.add_edge(Edge(
    from_node="existing_node_id",
    to_node="your_building_id",
    distance=50,  # metres
    slope=2.5,    # percentage
    surface=SurfaceType.SMOOTH_PAVEMENT,
    width=2.5,    # metres
    is_sheltered=False,
    features={AccessibilityFeature.CURB_CUT}
))
```

Then run:
```bash
python src/sample_data.py
```

### Method 3: Direct JSON Editing
Edit `data/north_terrace_campus.json` directly (advanced users only).

## Data Quality Checklist

Before adding data, verify:

- [ ] GPS coordinates are accurate
- [ ] Distance measurements are reasonable
- [ ] Slope percentages are measured, not estimated
- [ ] Width is the minimum clearance
- [ ] Surface type is correctly identified
- [ ] All accessibility features are noted
- [ ] Sheltered status is accurate

## Updating Existing Data

When campus changes occur:

1. **New construction**: Mark affected paths as blocked
2. **Renovations**: Update accessibility features
3. **Maintenance**: Use "Report Issue" feature
4. **Permanent changes**: Update the base data

## Community Collaboration

### For Student Projects:
- Assign building/area zones to different team members
- Use shared spreadsheet for data collection
- Regular sync meetings to combine data
- Cross-verification of measurements

### For University Partnerships:
- Contact Facilities Management for:
  - Building floor plans
  - Elevator schedules
  - Planned maintenance
  - Official measurements

### For Ongoing Maintenance:
- Encourage user reports
- Regular data audits
- Seasonal updates (weather impacts)
- Version control for changes

## Validation Methods

### Self-Testing
1. Walk/navigate the route yourself
2. Verify measurements against reality
3. Test with different mobility aids if possible

### User Testing
1. Recruit users with mobility challenges
2. Have them test routes
3. Collect feedback on accuracy
4. Adjust based on real experiences

### Cross-Referencing
1. Compare with official campus maps
2. Check against accessibility reports
3. Verify with facilities management
4. Use multiple measurement methods

## Getting Help

If you need assistance:

1. Check the main README.md
2. Review the code documentation
