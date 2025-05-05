<template>
  <div id="map" ref="mapContainer"></div>
</template>

<script setup>
import L from 'leaflet';
import dataset from './OpenSky/adsb_response.json';
</script>

<script>
export default {
  name: 'Map',
  data() {
    return {
      map: null,
      canvasRenderer: null
    };
  },
  methods: {
  handleResize() {
      if (this.map) {
        this.map.invalidateSize();
      }
    },
    initMap() {
      // Initialize map
      this.map = L.map(this.$refs.mapContainer, {
        maxBounds:[[-90, -180], [90, 180]],
        maxBoundsViscosity: 1.0,
        minZoom: 2,
        maxZoom: 20,
        noWrap: true,
      }).setView([37.7749, -122.4194], 12);

      // Add tile layer
      const baseMaps = {
        "OpenStreetMap": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors',
        }),
        "ESRI Satellite": L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
          attribution: "Tiles &copy; Esri",
        }),
        /*
        "NASA": L.tileLayer('https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_ShadedRelief_Bathymetry/default/{time}/{z}/{y}/{x}.jpg', {
          attribution: 'NASA Blue Marble',
          time: '2020-01-01'
        }),
        */
        "Slate Mode": L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
          attribution: "&copy; OpenStreetMap contributors & CartoDB",
          subdomains: "abcd",
          tileSize: 256,
          maxZoom: 19,
        })
      };

      baseMaps["OpenStreetMap"].addTo(this.map);
      L.control.layers(baseMaps).addTo(this.map);

      // Use canvas renderer
      this.canvasRenderer = L.canvas({ padding: 0.5 });

      // Add data points using canvas renderer
      dataset.states.forEach(([icao24, callsign, originCountry,
        timePosition, lastContact, longitude, latitude, baroAltitude,
        onGround, velocity, trueTrack, verticalRate, sensors,
        geoAltitude, squak, spi, positionSource]) => {

        if (latitude !== null && longitude !== null) {
          const popupContent = `
            <b>Flight: ${callsign ? callsign.trim() : "Unknown"}</b><br>
            Origin: ${originCountry || "Unknown"}<br>
            Altitude: ${baroAltitude ? baroAltitude.toFixed(0) + " m" : "N/A"}<br>
            Speed: ${velocity ? velocity.toFixed(1) + " m/s" : "N/A"}<br>
            Heading: ${trueTrack ? trueTrack.toFixed(1) + "°" : "N/A"}
          `;
          L.circleMarker([latitude, longitude], {
            radius: 6,
            color: '#3388ff',
            fillOpacity: 0.7,
            renderer: this.canvasRenderer
          }).addTo(this.map).bindPopup(popupContent);
        }
       });
    }
  },
  mounted() {
    this.initMap();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
};
</script>

<style>
/* Ensure the map takes the full size of the page */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#map {
  height: 100vh;
  width: 100vw;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
