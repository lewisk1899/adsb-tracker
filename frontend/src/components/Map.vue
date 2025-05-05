<template>
  <div id="map"></div>
</template>

<script setup>
// This block is only for imports
import L from 'leaflet';
import { onMounted } from 'vue';
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
      this.map = L.map('map', {
        maxBounds:[[-90, -180], [90, 180]],
        maxBoundsViscosity: 1.0,
        noWrap: true,
      }).setView([37.7749, -122.4194], 12);

      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
        minZoom: 2,
        noWrap: true,
      }).addTo(this.map);

      // Use canvas renderer
      this.canvasRenderer = L.canvas({ padding: 0.5 });

      // Add data points using canvas renderer
      dataset.states.forEach(([icao24, callsign, originCountry,
        timePosition, lastContact, longitude, latitude, baroAltitude,
        onGround, velocity, trueTrack, verticalRate, sensors,
        geoAltitude, squak, spi, positionSource]) => {

        if (latitude !== null || longitude !== null) {

          L.circleMarker([latitude, longitude], {
            radius: 2,
            color: '#3388ff',
            fillOpacity: 0.7,
            renderer: this.canvasRenderer
          }).addTo(this.map);
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
#map {
  width: 100%;    /* Avoid 100vw */
  height: 100vh;
  display: block; /* Optional: avoids inline div issues */
}
</style>
