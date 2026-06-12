import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Polyline, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// 50+ Bengaluru locations — [lat, lon]
const LOCATION_COORDS = {
  // Central
  "MG Road":              [12.9730, 77.6015],
  "M.G. Road":            [12.9730, 77.6015],
  "Brigade Road":         [12.9716, 77.6070],
  "Majestic":             [12.9757, 77.5728],
  "Shivajinagar":         [12.9857, 77.5945],
  "Ulsoor":               [12.9812, 77.6206],
  "Cubbon Park":          [12.9763, 77.5918],
  "Richmond Town":        [12.9614, 77.5993],
  // East
  "Indiranagar":          [12.9718, 77.6411],
  "Domlur":               [12.9610, 77.6370],
  "Koramangala":          [12.9352, 77.6271],
  "HSR Layout":           [12.9121, 77.6385],
  "BTM Layout":           [12.9166, 77.6101],
  "Bellandur":            [12.9304, 77.6695],
  "Sarjapur Road":        [12.9150, 77.6830],
  "Marathahalli":         [12.9569, 77.6980],
  "Whitefield":           [12.9698, 77.7499],
  "HAL":                  [12.9591, 77.6589],
  "Old Airport Road":     [12.9635, 77.6472],
  "Varthur":              [12.9400, 77.7400],
  "Kadugodi":             [12.9961, 77.7612],
  "Kadugodi Tree Park":   [12.9961, 77.7612],
  "Hopefarm":             [12.9840, 77.7510],
  "Kr Puram":             [12.9980, 77.7030],
  "Mahadevapura":         [12.9910, 77.7150],
  // South
  "Jayanagar":            [12.9298, 77.5806],
  "JP Nagar":             [12.9063, 77.5857],
  "Bannerghatta Road":    [12.8800, 77.5960],
  "Electronic City":      [12.8452, 77.6659],
  "Silk Board":           [12.9177, 77.6238],
  "Bommanahalli":         [12.9000, 77.6183],
  "Basavanagudi":         [12.9430, 77.5747],
  "Banashankari":         [12.9250, 77.5630],
  "Kumaraswamy Layout":   [12.9100, 77.5650],
  "Kanakapura Road":      [12.8900, 77.5700],
  "Uttarahalli":          [12.9020, 77.5470],
  "Arekere":              [12.8870, 77.6020],
  "Wilson Garden":        [12.9460, 77.5960],
  "Lalbagh":              [12.9507, 77.5855],
  // North
  "Hebbal":               [13.0354, 77.5919],
  "Yeshwanthpur":         [13.0285, 77.5385],
  "Rajajinagar":          [12.9982, 77.5530],
  "Malleshwaram":         [13.0031, 77.5643],
  "Sadashivanagar":       [13.0090, 77.5800],
  "Yelahanka":            [13.1000, 77.5970],
  "Thanisandra":          [13.0590, 77.6360],
  "Nagawara":             [13.0410, 77.6160],
  "Rt Nagar":             [13.0210, 77.5940],
  "Banaswadi":            [13.0110, 77.6470],
  "Hennur":               [13.0380, 77.6400],
  "Kalyan Nagar":         [13.0220, 77.6360],
  // West
  "Vijayanagar":          [12.9700, 77.5350],
  "Basaveshwaranagar":    [12.9870, 77.5380],
  "Nagarbhavi":           [12.9600, 77.5080],
  "Kengeri":              [12.9130, 77.4870],
  "Peenya":               [13.0300, 77.5210],
  "Magadi Road":          [12.9660, 77.5420],
  "Mysore Road":          [12.9500, 77.5300],
  "Rr Nagar":             [12.9350, 77.5100],
  "Nayandahalli":         [12.9520, 77.5190],
  // Outer
  "Hosur Road":           [12.8900, 77.6350],
  "Tumkur Road":          [13.0500, 77.5400],
  "Outer Ring Road":      [12.9350, 77.6800],
  "Devanahalli":          [13.2500, 77.7100],
  "Kempegowda Airport":   [13.1989, 77.7068],
  "Hoskote":              [13.0710, 77.7980],
  "Anekal":               [12.7100, 77.6940],
  "Begur":                [12.8760, 77.6290],
  "Hulimavu":             [12.8820, 77.5990],
  "Jp Nagar 6Th Phase":   [12.8880, 77.5720],
  "Gottigere":            [12.8700, 77.5830],
  "Konanakunte":          [12.8830, 77.5680],
};

const DEFAULT = [12.9716, 77.5946];

function FitBounds({ srcCoords, dstCoords }) {
  const map = useMap();
  useEffect(() => {
    const bounds = L.latLngBounds([srcCoords, dstCoords]);
    map.fitBounds(bounds, { padding: [40, 40] });
  }, [map, srcCoords, dstCoords]);
  return null;
}

export default function MapView({ source, destination }) {
  const srcCoords = LOCATION_COORDS[source] || DEFAULT;
  const dstCoords = LOCATION_COORDS[destination] || DEFAULT;

  const srcIcon = L.divIcon({
    className: 'leaflet-custom-marker',
    html: `<div class="custom-marker src-marker">📍 ${source || 'Source'}</div>`,
    iconSize: [0, 0],
    iconAnchor: [0, 0], // CSS will center it
  });

  const dstIcon = L.divIcon({
    className: 'leaflet-custom-marker',
    html: `<div class="custom-marker dst-marker">🏁 ${destination || 'Destination'}</div>`,
    iconSize: [0, 0],
    iconAnchor: [0, 0],
  });

  return (
    <div className="map-card interactive-map">
      <div className="map-header">
        <div className="map-title">Interactive Commute Route</div>
        <div className="map-loc">
          <span className="src">{source}</span>
          <span className="sep">→</span>
          <span className="dst">{destination}</span>
        </div>
      </div>
      <div style={{ height: "350px", width: "100%", position: "relative" }}>
        <MapContainer 
          center={[(srcCoords[0] + dstCoords[0]) / 2, (srcCoords[1] + dstCoords[1]) / 2]} 
          zoom={12} 
          style={{ height: "100%", width: "100%", zIndex: 1 }}
        >
          {/* Google Maps Style Tiles */}
          <TileLayer
            url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
            attribution="&copy; Google Maps"
          />
          <Marker position={srcCoords} icon={srcIcon} />
          <Marker position={dstCoords} icon={dstIcon} />
          <Polyline positions={[srcCoords, dstCoords]} color="#3b82f6" weight={4} dashArray="5, 8" />
          <FitBounds srcCoords={srcCoords} dstCoords={dstCoords} />
        </MapContainer>
      </div>
    </div>
  );
}