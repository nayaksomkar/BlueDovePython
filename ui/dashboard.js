var charts = {};
var cur = '', currentView = 'trends', allDates = [], currentData = null;
var colors = ['#667eea', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'];

function fmt(s) {
    var h = Math.floor(s / 3600);
    var m = Math.floor((s % 3600) / 60);
    return h + 'h ' + m + 'm';
}

function fmtHours(s) {
    return (s / 3600).toFixed(2);
}

function destroyCharts() {
    Object.values(charts).forEach(function(c) { if (c) c.destroy(); });
    charts = {};
}

function switchView(view) {
    if (view === currentView) return;
    
    destroyCharts();
    
    var oldView = document.getElementById('view-' + currentView);
    var newView = document.getElementById('view-' + view);
    
    oldView.style.opacity = '0';
    oldView.style.transform = 'translateX(50px)';
    
    setTimeout(function() {
        oldView.classList.remove('active');
        newView.classList.add('active');
        newView.style.transform = 'translateX(-50px)';
        
        setTimeout(function() {
            newView.style.transform = 'translateX(0)';
            newView.style.opacity = '1';
        }, 20);
        
        currentView = view;
        
        if (currentData) {
            if (view === 'trends') {
                loadTrendsData();
            } else {
                renderCurrentChart();
            }
        }
    }, 300);
    
    document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
    document.querySelector('.tab[data-view="' + view + '"]').classList.add('active');
}

document.querySelectorAll('.tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
        switchView(this.dataset.view);
    });
});

function renderCurrentChart() {
    if (!currentData) return;
    var s = currentData.summary;
    var tot = currentData.total;
    
    var labels = s.slice(0, 6).map(function(x) { return x.app; });
    var data = s.slice(0, 6).map(function(x) { return x.seconds; });
    
    if (currentView === 'pie') {
        var ctx = document.getElementById('chartPie').getContext('2d');
        charts.pie = new Chart(ctx, {
            type: 'pie',
            data: { labels: labels, datasets: [{ data: data, backgroundColor: colors, borderWidth: 3, borderColor: '#fff', hoverOffset: 10 }] },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom', labels: { padding: 15, usePointStyle: true } },
                    tooltip: { callbacks: { label: function(ctx) { var pct = tot > 0 ? ((ctx.raw / tot) * 100).toFixed(1) : 0; return ' ' + fmt(ctx.raw) + ' (' + pct + '%)'; } } }
                },
                animation: { animateRotate: true, duration: 800 }
            }
        });
        document.getElementById('chartNumPie').textContent = (tot / 3600).toFixed(1);
    }
    
    else if (currentView === 'bar') {
        var ctx = document.getElementById('chartBar').getContext('2d');
        charts.bar = new Chart(ctx, {
            type: 'bar',
            data: { labels: labels, datasets: [{ data: data, backgroundColor: colors.slice(0, data.length), borderRadius: 8, borderSkipped: false }] },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false },
                    tooltip: { callbacks: { label: function(ctx) { var pct = tot > 0 ? ((ctx.raw / tot) * 100).toFixed(1) : 0; return ' ' + fmt(ctx.raw) + ' (' + pct + '%)'; } } }
                },
                scales: { x: { grid: { display: false } }, y: { grid: { display: false } } },
                animation: { duration: 800 }
            }
        });
    }
    
    else if (currentView === 'doughnut') {
        var ctx = document.getElementById('chartDoughnut').getContext('2d');
        charts.doughnut = new Chart(ctx, {
            type: 'doughnut',
            data: { labels: labels, datasets: [{ data: data, backgroundColor: colors, borderWidth: 3, borderColor: '#fff', hoverOffset: 10 }] },
            options: {
                responsive: true,
                cutout: '60%',
                plugins: {
                    legend: { position: 'bottom', labels: { padding: 15, usePointStyle: true } },
                    tooltip: { callbacks: { label: function(ctx) { var pct = tot > 0 ? ((ctx.raw / tot) * 100).toFixed(1) : 0; return ' ' + fmt(ctx.raw) + ' (' + pct + '%)'; } } }
                },
                animation: { animateRotate: true, duration: 800 }
            }
        });
        document.getElementById('chartNumDoughnut').textContent = (tot / 3600).toFixed(1);
    }
}

function loadTrendsData() {
    var dates = allDates.slice(0, 7);
    if (dates.length === 0) return;
    
    var promises = dates.map(function(d) {
        return new Promise(function(resolve) {
            var x = new XMLHttpRequest();
            x.open('GET', '/api/data/' + d);
            x.onload = function() { resolve({ date: d, data: JSON.parse(this.responseText) }); };
            x.onerror = function() { resolve({ date: d, data: { summary: [] } }); };
            x.send();
        });
    });
    
    Promise.all(promises).then(renderTrendsCharts);
}

function renderTrendsCharts(results) {
    var appTotals = {};
    var dateLabels = [];
    
    results.forEach(function(r) {
        dateLabels.push(r.date);
        r.data.summary.forEach(function(s) {
            appTotals[s.app] = (appTotals[s.app] || 0) + s.seconds;
        });
    });
    
    var topApps = Object.entries(appTotals).sort(function(a, b) { return b[1] - a[1]; }).slice(0, 5);
    
    var datasets = {};
    topApps.forEach(function(app) {
        datasets[app[0]] = results.map(function(r) {
            var found = r.data.summary.find(function(s) { return s.app === app[0]; });
            return found ? found.seconds : 0;
        });
    });
    
    if (charts.trends) charts.trends.destroy();
    var ctx1 = document.getElementById('trendsChart').getContext('2d');
    charts.trends = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: dateLabels,
            datasets: topApps.map(function(app, idx) {
                return {
                    label: app[0],
                    data: datasets[app[0]],
                    borderColor: colors[idx],
                    backgroundColor: idx === 0 ? 'rgba(102, 126, 234, 0.1)' : 'transparent',
                    borderWidth: idx === 0 ? 3 : 2,
                    fill: idx === 0,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 7
                };
            })
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { padding: 15, usePointStyle: true } },
                tooltip: { callbacks: { label: function(ctx) { return ' ' + ctx.dataset.label + ': ' + fmt(ctx.raw); } } }
            },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: '#f0f0f5' }, ticks: { callback: function(v) { return fmt(v); } } }
            }
        }
    });
    
    if (charts.stacked) charts.stacked.destroy();
    var ctx2 = document.getElementById('stackedChart').getContext('2d');
    charts.stacked = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: dateLabels,
            datasets: topApps.map(function(app, idx) {
                return {
                    label: app[0],
                    data: datasets[app[0]],
                    backgroundColor: colors[idx],
                    borderRadius: 4
                };
            })
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { padding: 15, usePointStyle: true } },
                tooltip: { callbacks: { label: function(ctx) { return ' ' + ctx.dataset.label + ': ' + fmt(ctx.raw); } } }
            },
            scales: {
                x: { stacked: true, grid: { display: false } },
                y: { stacked: true, grid: { color: '#f0f0f5' }, ticks: { callback: function(v) { return fmt(v); } } }
            }
        }
    });
}

function load(d) {
    var x = new XMLHttpRequest();
    x.open('GET', '/api/data/' + d);
    x.onload = function() {
        var r = JSON.parse(this.responseText);
        var s = r.summary || [];
        var t = r.records || [];
        var tot = 0;
        for (var i = 0; i < s.length; i++) tot += s[i].seconds || 0;
        
        document.getElementById('total').textContent = fmt(tot);
        document.getElementById('apps').textContent = s.length;
        document.getElementById('top').textContent = s[0] ? s[0].app.substring(0, 15) : '-';
        
        currentData = { summary: s, total: tot, records: t };
        
        if (currentView === 'trends') {
            loadTrendsData();
        } else {
            renderCurrentChart();
        }
        
        var tbFull = '';
        for (var i = 0; i < s.length; i++) {
            var sec = s[i].seconds || 0;
            var pct = tot > 0 ? ((sec / tot) * 100).toFixed(1) : 0;
            tbFull += '<tr><td>' + s[i].app + '</td><td>' + fmt(sec) + '</td><td>' + pct + '%</td><td>' + fmtHours(sec) + 'h</td></tr>';
        }
        document.getElementById('tableFull').innerHTML = tbFull;
        
        var act = '';
        var recent = t.slice(-12).reverse();
        for (var i = 0; i < recent.length; i++) {
            act += '<div class="activity-item"><div class="app">' + (recent[i].app || '-') + '</div>' +
                '<div class="time">' + (recent[i].window || '').substring(0, 30) + '</div>' +
                '<div class="dur">' + (recent[i].duration || '00:00') + '</div></div>';
        }
        document.getElementById('activity').innerHTML = act;
    };
    x.send();
}

function loadDates(db) {
    var x = new XMLHttpRequest();
    x.open('GET', '/api/use/' + db);
    x.onload = function() {
        var d = JSON.parse(this.responseText);
        allDates = d.dates || [];
        var sel = document.getElementById('date');
        sel.innerHTML = '';
        for (var i = 0; i < allDates.length; i++) {
            sel.innerHTML += '<option value="' + allDates[i] + '">' + allDates[i] + '</option>';
        }
        if (allDates.length) { 
            cur = allDates[0]; 
            load(cur); 
            loadTrendsData();
        }
        else { cur = ''; destroyCharts(); }
    };
    x.send();
}

function init() {
    loadDates('main');
}

document.getElementById('db').onchange = function() { destroyCharts(); loadDates(this.value); };

document.getElementById('date').onchange = function() { destroyCharts(); cur = this.value; load(cur); };

init();
setInterval(function() { if (cur && currentView !== 'trends') { destroyCharts(); load(cur); } }, 5000);
