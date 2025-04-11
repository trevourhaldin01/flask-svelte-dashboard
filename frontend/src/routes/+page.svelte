<script lang="ts">
    import { onMount } from 'svelte';
    import type { SensorReading } from '$lib/types';
    import TemperatureChart from '$lib/components/TemperatureChart.svelte';
    import HumidityGauge from '$lib/components/HumidityGauge.svelte';
  
    let currentReading: SensorReading | null = null;
    let historicalData: SensorReading[] = [];
    let eventSource: EventSource | undefined;

    const url = import.meta.env.VITE_API_URL;
  
    onMount(() => {
      const init = async () => {
        try {
          const response = await fetch(`${url}/current`);
          currentReading = await response.json();
  
          eventSource = new EventSource(`${url}/stream`);
          eventSource.addEventListener('sensor_update', (event) => {
            currentReading = JSON.parse(event.data);
          });
        } catch (error) {
          console.error('Error fetching sensor data:', error);
        }
      };
  
      init();
  
      return () => {
        if (eventSource) eventSource.close();
      };
    });
</script>

<main class="container">
    <h1>Sensor Dashboard</h1>
  
    {#if currentReading}
      <div class="dashboard-grid">
        <div class="card span-2">
          <h2>Temperature History</h2>
          <TemperatureChart data={historicalData} />
        </div>
  
        <div class="card">
          <h2>Current Humidity</h2>
          <HumidityGauge value={currentReading.humidity} />
        </div>
  
        <div class="card">
          <h2>System Status</h2>
          <div class="status-container">
            <div class="status-indicator {currentReading.status}"></div>
            <p class="status-text">{currentReading.status}</p>
            <p class="timestamp">Last updated: {new Date(currentReading.timestamp).toLocaleTimeString()}</p>
          </div>
        </div>
      </div>
    {/if}
  </main>
  
<style>
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
    }
  
    .dashboard-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
      margin-top: 2rem;
    }
  
    .card {
      background: #fff;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  
    .span-2 {
      grid-column: span 2;
    }
  
    .status-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }
  
    .status-indicator {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      margin: 1rem 0;
    }
  
    .status-indicator.normal { background-color: #2ecc71; }
    .status-indicator.warning { background-color: #f1c40f; }
    .status-indicator.critical { background-color: #e74c3c; }
  
    .status-text {
      text-transform: uppercase;
      font-weight: bold;
    }
  
    .timestamp {
      color: #666;
      font-size: 0.9rem;
    }
  
    @media (max-width: 768px) {
      .dashboard-grid {
        grid-template-columns: 1fr;
      }
  
      .span-2 {
        grid-column: auto;
      }
    }
</style>