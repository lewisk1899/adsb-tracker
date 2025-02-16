<template>
  <div id="map" ref="mapContainer"></div>
</template>

<script>
import { onMounted, ref } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "LeafletMap",
  setup() {
    const mapContainer = ref(null);
    let map;

    onMounted(() => {
      map = L.map(mapContainer.value, {
        minZoom: 3,  // Prevent zooming out too far
        maxZoom: 18, // Optional: Restrict max zoom
        zoomSnap: 1, // Ensures zoom levels snap properly
      }).setView([37.7749, -122.4194], 13); // Centered on San Francisco

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(map);

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

