"""
Google Maps API key management.

The MAP_API_KEY environment variable must be set to a valid Google Maps API key
for accessing Google Maps Platform features. This key is used for generating 
static map images.
"""

import os










MAP_API_KEY = os.getenv("MAP_API_KEY")
