"""
Setup verification script
Run this to check if everything is installed correctly
"""

import sys

print("="*60)
print("SETUP VERIFICATION")
print("="*60)

# Check Python version
print(f"\n✓ Python version: {sys.version}")
print(f"✓ Python path: {sys.executable}")

# Check Flask
try:
    import flask
    print(f"✓ Flask version: {flask.__version__}")
except ImportError as e:
    print(f"✗ Flask NOT installed")
    print(f"  Error: {e}")
    print(f"  Fix: pip install flask")
    sys.exit(1)

# Check Flask-CORS
try:
    from flask_cors import CORS
    print("✓ Flask-CORS installed")
except ImportError as e:
    print(f"✗ Flask-CORS NOT installed")
    print(f"  Error: {e}")
    print(f"  Fix: pip install flask-cors")
    sys.exit(1)

# Check project structure
import os
print("\n" + "="*60)
print("PROJECT STRUCTURE CHECK")
print("="*60)

required_files = [
    "src/campus_graph.py",
    "src/pathfinding.py",
    "src/sample_data.py",
    "data/north_terrace_campus.json",
    "templates/index.html",
    "app.py",
    "demo.py",
    "requirements.txt"
]

all_present = True
for file in required_files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} MISSING")
        all_present = False

# Try importing project modules
print("\n" + "="*60)
print("MODULE IMPORT CHECK")
print("="*60)

sys.path.insert(0, 'src')

try:
    from campus_graph import CampusGraph, Node, Edge
    print("✓ campus_graph module imports successfully")
except ImportError as e:
    print(f"✗ campus_graph import failed: {e}")
    all_present = False

try:
    from pathfinding import MultiCriteriaRouter, RoutingPreference
    print("✓ pathfinding module imports successfully")
except ImportError as e:
    print(f"✗ pathfinding import failed: {e}")
    all_present = False

# Check if data file exists and is valid
print("\n" + "="*60)
print("DATA FILE CHECK")
print("="*60)

try:
    graph = CampusGraph.load_from_file("data/north_terrace_campus.json")
    stats = graph.get_statistics()
    print(f"✓ Campus data loaded successfully")
    print(f"  - Nodes: {stats['total_nodes']}")
    print(f"  - Edges: {stats['total_edges']}")
    print(f"  - Buildings: {stats['buildings']}")
except Exception as e:
    print(f"✗ Failed to load campus data: {e}")
    all_present = False

# Final result
print("\n" + "="*60)
if all_present:
    print("✓✓✓ ALL CHECKS PASSED! ✓✓✓")
    print("="*60)
    print("\nYou're ready to go!")
    print("\nNext steps:")
    print("  1. Run demo: python demo.py")
    print("  2. Start web server: python app.py")
    print("  3. Open browser: http://localhost:5000")
else:
    print("✗✗✗ SOME CHECKS FAILED ✗✗✗")
    print("="*60)
    print("\nPlease fix the issues above before running the application.")
    print("See TROUBLESHOOTING.md for help.")

print()
