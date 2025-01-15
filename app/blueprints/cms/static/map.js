
// Initialize and add the map
let map;
let map_lat = parseFloat(document.getElementById('map').getAttribute("map-lat"));
let map_lng = parseFloat(document.getElementById('map').getAttribute("map-lng"));
let map_zoom = parseFloat(document.getElementById('map').getAttribute("map-zoom"));
let map_marker_title = document.getElementById('map').getAttribute("map-marker-title");

async function initMap() {
  // The location of Plym Auditorium
  const position = { lat: map_lat, lng: map_lng };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

  // The map, centered at Plym Auditorium
  map = new Map(document.getElementById("map"), {
    zoom: map_zoom,
    center: position,
    mapId: "plym",
    mapTypeId: 'satellite',
    disableDefaultUI: true,
    tilt: 0,
  });

  // The marker, positioned at Plym Auditorium
  const marker = new AdvancedMarkerView({
    map: map,
    position: position,
    title: map_marker_title,
  });
}

initMap();

