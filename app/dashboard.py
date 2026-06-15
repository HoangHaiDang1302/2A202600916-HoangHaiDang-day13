from fastapi.responses import HTMLResponse

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day 13 Observability Dashboard</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(22, 28, 45, 0.4);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --primary: #8b5cf6;
            --secondary: #06b6d4;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 2rem;
            background-image: 
                radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1.5rem;
        }

        .logo-section h1 {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(to right, #a78bfa, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        .logo-section p {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }

        .controls {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .badge {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .badge-pulse {
            width: 8px;
            height: 8px;
            background-color: var(--success);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.6; }
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }

        .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        /* Overview stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.5rem;
            backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .stat-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .stat-card .label {
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stat-card .value {
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0.5rem;
            color: var(--text-primary);
        }

        /* 6 Panels grid */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 1.5rem;
        }

        @media (max-width: 600px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .chart-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            height: 350px;
            transition: all 0.3s;
        }

        .chart-card:hover {
            border-color: rgba(139, 92, 246, 0.25);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .chart-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .chart-subtitle {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .chart-container {
            position: relative;
            flex-grow: 1;
            width: 100%;
            height: calc(100% - 30px);
        }
    </style>
</head>
<body>
    <header>
        <div class="logo-section">
            <h1>Day 13 Observability Cockpit</h1>
            <p>Layer-2 Operational Metrics & Real-time SLO Monitoring</p>
        </div>
        <div class="controls">
            <div class="badge">
                <div class="badge-pulse"></div>
                Live Polling (15s)
            </div>
            <button class="btn" onclick="fetchMetrics()">Refresh Now</button>
        </div>
    </header>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="label">Total Traffic</div>
            <div class="value" id="stat-traffic">0</div>
        </div>
        <div class="stat-card">
            <div class="label">Latency P95</div>
            <div class="value" id="stat-p95">0 ms</div>
        </div>
        <div class="stat-card">
            <div class="label">Total Cost</div>
            <div class="value" id="stat-cost">$0.0000</div>
        </div>
        <div class="stat-card">
            <div class="label">Avg Quality</div>
            <div class="value" id="stat-quality">0.00</div>
        </div>
    </div>

    <div class="dashboard-grid">
        <!-- 1. Latency P50/P95/P99 -->
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Latency Trends</div>
                    <div class="chart-subtitle">P50, P95, and P99 tail latencies (ms)</div>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="chart-latency"></canvas>
            </div>
        </div>

        <!-- 2. Traffic (Request Count / QPS) -->
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Traffic & Throughput</div>
                    <div class="chart-subtitle">Request count over time</div>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="chart-traffic"></canvas>
            </div>
        </div>

        <!-- 3. Error Rate Breakdown -->
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Error Distribution</div>
                    <div class="chart-subtitle">Failure breakdown by exception type</div>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="chart-errors"></canvas>
            </div>
        </div>

        <!-- 4. Cost over time -->
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Cost Analytics</div>
                    <div class="chart-subtitle">Cumulative API cost progression (USD)</div>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="chart-cost"></canvas>
            </div>
        </div>

        <!-- 5. Tokens In/Out -->
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Token Consumed</div>
                    <div class="chart-subtitle">Compare input prompts vs output generation tokens</div>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="chart-tokens"></canvas>
            </div>
        </div>

        <!-- 6. Quality Proxy -->
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Quality Score (SLO)</div>
                    <div class="chart-subtitle">Heuristic score compared to SLO (0.75 Target)</div>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="chart-quality"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Global variables for Chart instances
        let charts = {};

        // Helper to format chart timestamp labels
        function formatTime(timestamp) {
            const date = new Date(timestamp * 1000);
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }

        // Initialize empty charts
        function initCharts() {
            const ctxLatency = document.getElementById('chart-latency').getContext('2d');
            charts.latency = new Chart(ctxLatency, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        { label: 'P50', data: [], borderColor: '#06b6d4', backgroundColor: 'rgba(6, 182, 212, 0.1)', tension: 0.3, fill: true },
                        { label: 'P95', data: [], borderColor: '#8b5cf6', backgroundColor: 'rgba(139, 92, 246, 0.1)', tension: 0.3, fill: true },
                        { label: 'P99', data: [], borderColor: '#f59e0b', borderDash: [5, 5], tension: 0.1 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' }, title: { display: true, text: 'ms', color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });

            const ctxTraffic = document.getElementById('chart-traffic').getContext('2d');
            charts.traffic = new Chart(ctxTraffic, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{ label: 'Requests', data: [], backgroundColor: '#3b82f6', borderRadius: 4 }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', stepSize: 1 } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });

            const ctxErrors = document.getElementById('chart-errors').getContext('2d');
            charts.errors = new Chart(ctxErrors, {
                type: 'doughnut',
                data: {
                    labels: ['No Errors'],
                    datasets: [{ data: [1], backgroundColor: ['#10b981', '#ef4444', '#f59e0b', '#8b5cf6'] }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#f8fafc' } }
                    }
                }
            });

            const ctxCost = document.getElementById('chart-cost').getContext('2d');
            charts.cost = new Chart(ctxCost, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{ label: 'Cumulative Cost', data: [], borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', fill: true, tension: 0.2 }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' }, title: { display: true, text: 'USD', color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });

            const ctxTokens = document.getElementById('chart-tokens').getContext('2d');
            charts.tokens = new Chart(ctxTokens, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [
                        { label: 'Prompt Tokens', data: [], backgroundColor: '#6366f1', borderRadius: 4 },
                        { label: 'Completion Tokens', data: [], backgroundColor: '#10b981', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { stacked: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { stacked: true, grid: { display: false }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });

            const ctxQuality = document.getElementById('chart-quality').getContext('2d');
            charts.quality = new Chart(ctxQuality, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        { label: 'Quality Heuristic', data: [], borderColor: '#ec4899', backgroundColor: 'rgba(236, 72, 153, 0.1)', tension: 0.3, fill: true },
                        { label: 'SLO Threshold (0.75)', data: [], borderColor: '#ef4444', borderDash: [5, 5], pointRadius: 0, tension: 0 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { min: 0, max: 1.1, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            });
        }

        // Fetch snapshot data and redraw charts
        async function fetchMetrics() {
            try {
                const response = await fetch('/metrics');
                const data = await response.json();

                // 1. Update Overview Card values
                document.getElementById('stat-traffic').innerText = data.traffic;
                document.getElementById('stat-p95').innerText = `${data.latency_p95.toFixed(0)} ms`;
                document.getElementById('stat-cost').innerText = `$${data.total_cost_usd.toFixed(4)}`;
                document.getElementById('stat-quality').innerText = data.quality_avg.toFixed(2);

                const history = data.history || [];

                // 2. Latency Chart update
                // Since our raw history has per-request details, let's plot individual latencies or sliding aggregate
                const labels = history.map(h => formatTime(h.ts));
                const latencies = history.map(h => h.latency_ms);
                
                // Calculate sliding p50, p95, p99 for line trends
                let slidingP50 = [];
                let slidingP95 = [];
                let slidingP99 = [];
                
                for (let i = 0; i < latencies.length; i++) {
                    const windowValues = latencies.slice(0, i + 1);
                    windowValues.sort((a, b) => a - b);
                    const idx50 = Math.max(0, Math.min(windowValues.length - 1, Math.round(0.5 * windowValues.length) - 1));
                    const idx95 = Math.max(0, Math.min(windowValues.length - 1, Math.round(0.95 * windowValues.length) - 1));
                    const idx99 = Math.max(0, Math.min(windowValues.length - 1, Math.round(0.99 * windowValues.length) - 1));
                    slidingP50.push(windowValues[idx50]);
                    slidingP95.push(windowValues[idx95]);
                    slidingP99.push(windowValues[idx99]);
                }

                charts.latency.data.labels = labels;
                charts.latency.data.datasets[0].data = slidingP50;
                charts.latency.data.datasets[1].data = slidingP95;
                charts.latency.data.datasets[2].data = slidingP99;
                charts.latency.update();

                // 3. Traffic chart update
                charts.traffic.data.labels = labels;
                // Just map cumulative index to indicate transaction index
                charts.traffic.data.datasets[0].data = history.map((_, idx) => idx + 1);
                charts.traffic.update();

                // 4. Error rate doughnut chart update
                const errBreakdown = data.error_breakdown || {};
                const errKeys = Object.keys(errBreakdown);
                const errVals = Object.values(errBreakdown);

                if (errKeys.length > 0) {
                    charts.errors.data.labels = errKeys;
                    charts.errors.data.datasets[0].data = errVals;
                    charts.errors.data.datasets[0].backgroundColor = ['#ef4444', '#f59e0b', '#8b5cf6', '#3b82f6'];
                } else {
                    charts.errors.data.labels = ['No Errors (Healthy)'];
                    charts.errors.data.datasets[0].data = [1];
                    charts.errors.data.datasets[0].backgroundColor = ['#10b981'];
                }
                charts.errors.update();

                // 5. Cost progression over time
                let cumulativeCost = 0;
                const costData = history.map(h => {
                    cumulativeCost += h.cost_usd;
                    return cumulativeCost;
                });
                charts.cost.data.labels = labels;
                charts.cost.data.datasets[0].data = costData;
                charts.cost.update();

                // 6. Tokens in and out stacked bar chart
                charts.tokens.data.labels = labels;
                charts.tokens.data.datasets[0].data = history.map(h => h.tokens_in);
                charts.tokens.data.datasets[1].data = history.map(h => h.tokens_out);
                charts.tokens.update();

                // 7. Quality score vs SLO line
                charts.quality.data.labels = labels;
                charts.quality.data.datasets[0].data = history.map(h => h.quality_score);
                charts.quality.data.datasets[1].data = Array(history.length).fill(0.75);
                charts.quality.update();

            } catch (error) {
                console.error("Failed to refresh dashboard metrics", error);
            }
        }

        // Initialize on window load and set interval
        window.onload = () => {
            initCharts();
            fetchMetrics();
            // Polling every 15 seconds
            setInterval(fetchMetrics, 15000);
        };
    </script>
</body>
</html>
"""

def get_dashboard_response() -> HTMLResponse:
    return HTMLResponse(content=DASHBOARD_HTML)
