import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl:       require("leaflet/dist/images/marker-icon.png"),
  shadowUrl:     require("leaflet/dist/images/marker-shadow.png"),
});

const LOCATION_COORDS = {
  "Koramangala":      [12.9352, 77.6245],
  "Indiranagar":      [12.9784, 77.6408],
  "Whitefield":       [12.9698, 77.7499],
  "MG Road":          [12.9757, 77.6011],
  "Hebbal":           [13.0450, 77.5970],
  "Electronic City":  [12.8399, 77.6770],
  "Jayanagar":        [12.9308, 77.5838],
  "JP Nagar":         [12.9063, 77.5857],
  "Marathahalli":     [12.9591, 77.6974],
  "HSR Layout":       [12.9116, 77.6389],
  "Bannerghatta Road":[12.8933, 77.5975],
  "Yeshwanthpur":     [13.0213, 77.5540],
  "Rajajinagar":      [12.9916, 77.5530],
  "Malleshwaram":     [13.0034, 77.5700],
  "BTM Layout":       [12.9166, 77.6101],
  "Bellandur":        [12.9256, 77.6784],
  "Sarjapur Road":    [12.9010, 77.6849],
};

// Default to city center if location not found
const DEFAULT = [12.9716, 77.5946];

export default function MapView({ source, destination }) {
  const srcCoords  = LOCATION_COORDS[source]      || DEFAULT;
  const destCoords = LOCATION_COORDS[destination] || DEFAULT;

  // Center map between the two points
  const center = [
    (srcCoords[0]  + destCoords[0]) / 2,
    (srcCoords[1]  + destCoords[1]) / 2,
  ];

  return (
    <div className="map-card">
      <div className="map-label">
        📍 {source} → {destination}
      </div>
      <MapContainer
        center={center}
        zoom={12}
        style={{ height: 220, width: "100%", borderRadius: "0 0 12px 12px" }}
        scrollWheelZoom={false}
        zoomControl={false}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap"
        />
        <Marker position={srcCoords}>
          <Popup>🟢 Source: {source}</Popup>
        </Marker>
        <Marker position={destCoords}>
          <Popup>🔴 Destination: {destination}</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}