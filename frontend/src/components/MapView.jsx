import { useEffect, useRef, useState } from "react";
import { OlaMaps } from "olamaps-web-sdk";
import { getMapConfig } from "../api/client";

// 50+ Bengaluru locations — [lat, lon] (Note: We will convert this to [lon, lat] for Ola Maps)
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

export default function MapView({ source, destination }) {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const [apiKey, setApiKey] = useState(null);

  // 1. Convert coords to [lon, lat] format for Ola Maps
  const getCoords = (loc) => {
    const raw = LOCATION_COORDS[loc] || DEFAULT;
    return [raw[1], raw[0]]; // [lon, lat]
  };

  const srcCoords = getCoords(source);
  const dstCoords = getCoords(destination);

  // 2. Fetch API Key
  useEffect(() => {
    getMapConfig().then(res => setApiKey(res.data.apiKey));
  }, []);

  // 3. Initialize Map
  useEffect(() => {
    if (!apiKey || !mapContainerRef.current) return;

    // Destroy previous instance if any
    if (mapRef.current) {
      mapRef.current.remove();
      mapRef.current = null;
    }

    const olaMaps = new OlaMaps({ apiKey });
    
    olaMaps.init({
      style: "https://api.olamaps.io/tiles/vector/v1/styles/default-light-standard/style.json",
      container: mapContainerRef.current,
      center: [(srcCoords[0] + dstCoords[0]) / 2, (srcCoords[1] + dstCoords[1]) / 2],
      zoom: 12,
    }).then(mapInstance => {
      mapRef.current = mapInstance;

      // Wait for load to add markers and fit bounds
      mapInstance.on('load', () => {
        // Add Source Marker
        olaMaps.addMarker({ offset: [0, -15], anchor: 'bottom' })
          .setLngLat(srcCoords)
          .addTo(mapInstance);

        // Add Destination Marker
        olaMaps.addMarker({ offset: [0, -15], anchor: 'bottom' })
          .setLngLat(dstCoords)
          .addTo(mapInstance);

        // Fit Bounds to show both points
        const bounds = [
          [Math.min(srcCoords[0], dstCoords[0]) - 0.05, Math.min(srcCoords[1], dstCoords[1]) - 0.05],
          [Math.max(srcCoords[0], dstCoords[0]) + 0.05, Math.max(srcCoords[1], dstCoords[1]) + 0.05]
        ];
        mapInstance.fitBounds(bounds, { padding: 40 });
      });
    });

    return () => {
      if (mapRef.current) mapRef.current.remove();
    };
  }, [apiKey, source, destination]);

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
      <div 
        ref={mapContainerRef} 
        className="ola-map-container"
        style={{ height: "350px", width: "100%", position: "relative" }} 
      />
    </div>
  );
}