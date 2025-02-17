<template>
  <div id="map" ref="mapContainer"></div>
</template>

<script>
import { onMounted, ref } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import json from './OpenSky/adsb_response.json'

export default {
  name: "LeafletMap",
  setup() {
    const mapContainer = ref(null);
    let map;

    let markers = new Map(); // store markers in a map by aircraft ICAO24 ID

    const aircraftIcon = L.icon({
      iconUrl: "airplane.svg",
      iconSize: [32,32],
    });

    const fetchADSBData = async () => {
      try {
        // const response = await fetch("/OpenSky/adsb_response.json"); // TODO: make path a variable
        const data = json;
        plotAircraft(data.states);

      } catch(error) {
        console.error("Error loading ADS-B data:", error);
      }
    };

    const plotAircraft = (flightData) => {
      if (!flightData) return;

      // set names for each flight param, making it easier to reference later
      flightData.forEach(flight => {
        const [
          icao24,      // Unique aircraft ID
          callsign,    // Flight number or callsign
          origin,      // Origin country
          timePos,     // Last position time
          timeContact, // Last contact time
          longitude,   // Longitude
          latitude,    // Latitude
          altitude,    // Altitude (meters)
          onGround,    // Boolean: is on ground
          velocity,    // Speed (m/s)
          heading,     // Heading (degrees)
          verticalRate,// Vertical speed
          sensors,     // Sensor IDs (nullable)
          baroAltitude,// Barometric altitude
          squawk,      // Squawk code
          spi,         // Special purpose indicator
          positionSrc  // Source of position info
        ] = flight;
        
        const popupContent = `
          <b>Flight: ${callsign ? callsign.trim() : "Unknown"}</b><br>
          Origin: ${origin || "Unknown"}<br>
          Altitude: ${altitude ? altitude.toFixed(0) + " m" : "N/A"}<br>
          Speed: ${velocity ? velocity.toFixed(1) + " m/s" : "N/A"}<br>
          Heading: ${heading ? heading.toFixed(1) + "°" : "N/A"}
        `;

        // Update marker if it exists, otherwise create a new one
        if (markers.has(icao24)) {
          markers.get(icao24)
            .setLatLng([latitude, longitude])
            .setIcon(aircraftIcon) // Ensure correct icon --> may be redundant might remove
            .bindPopup(popupContent);
        } else {
          const marker = L.marker([latitude, longitude], { icon: aircraftIcon })
            .addTo(map)
            .bindPopup(popupContent);
          markers.set(icao24, marker);
        }
      });

      
      // remove aircraft no longer in the dataset
      const activeIcao24s = new Set(stateData.map(flight => flight[0]));
      markers.forEach((marker, key) => {
        if (!activeIcao24s.has(key)) {
          map.removeLayer(marker);
          markers.delete(key);
        }
      });

    };

    onMounted(() => {
      map = L.map(mapContainer.value, {
        minZoom: 3,  // Prevent zooming out too far
        maxZoom: 18, // Optional: Restrict max zoom
        zoomSnap: 1, // Ensures zoom levels snap properly
      }).setView([37.7749, -122.4194], 13); // Centered on San Francisco

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(map);

      const updateTime = 10000; // equal to 10 seconds
      // Fetch and plot data
      fetchADSBData();
      // Set refresh time to repopulate map from flight data
      setInterval(fetchADSBData, updateTime);
      // Handle window resize
      window.addEventListener("resize", () => {
        map.invalidateSize();
      });
    });

    return { mapContainer };
  },
};
</script>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

#map {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 100%;
}
</style>

