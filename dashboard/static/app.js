async function refresh() {
  try {
    const res = await fetch('/api/latest');
    const data = await res.json();
    // Temperature
    const t = data['iot/sensor/temperature'];
    if (t) {
      document.getElementById('temp-value').textContent = t.value;
      document.getElementById('temp-unit').textContent = t.unit || 'C';
      document.getElementById('temp-time').textContent = t.timestamp || '';
    }
    // Humidity
    const h = data['iot/sensor/humidity'];
    if (h) {
      document.getElementById('hum-value').textContent = h.value;
      document.getElementById('hum-unit').textContent = h.unit || '%';
      document.getElementById('hum-time').textContent = h.timestamp || '';
    }
    // GPS
    const g = data['iot/sensor/gps'];
    if (g) {
      document.getElementById('gps-lat').textContent = g.lat;
      document.getElementById('gps-lon').textContent = g.lon;
      document.getElementById('gps-time').textContent = g.timestamp || '';
    }
    document.getElementById('status').textContent = 'MQTT connecté, données à jour';
    document.getElementById('status').className = 'alert alert-success';
  } catch (e) {
    document.getElementById('status').textContent = 'En attente de données...' + e;
    document.getElementById('status').className = 'alert alert-warning';
  }
}

setInterval(refresh, 1000);
refresh();
