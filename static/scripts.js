// ============================================================================
// ROBUST WATERMARKING
// ============================================================================

const API_URL = 'http://localhost:5001';


// ============================================================================
// TAB MANAGEMENT
// ============================================================================

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// ============================================================================
// SLIDER UPDATES
// ============================================================================

function updateThreshold() {
    const value = document.getElementById('threshold').value;
    document.getElementById('thresholdValue').textContent = value/1000;
}

// ============================================================================
// Analysis with many parameters
// ============================================================================

function collectAttackParams(containerId) {
    const container = document.getElementById(containerId);
    const params = {};

    if (!container) return params;

    const inputs = container.querySelectorAll("[data-param]");

    inputs.forEach(input => {
        const name = input.dataset.param;
        params[name] = parseFloat(input.value);
    });

    return params;
}

const attackParams = collectAttackParams("attack-params");



// ============================================================================
// CREATE WATERMARK
// ============================================================================

async function createWatermark() {
    const text = document.getElementById('originalText').value.trim();

    if (!text) {
        alert('Please enter text to watermark');
        return;
    }

    const resultDiv = document.getElementById('createResult');
    resultDiv.innerHTML = '<div class="loading active"><div class="spinner"></div><p style="margin-top: 15px; color: #666;">Creating robust watermark...</p></div>';

    try {
        const response = await fetch(`${API_URL}/api/watermark/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                user_id: 'default',
                metadata: { created_at: new Date().toISOString() }
            })
        });

        const data = await response.json();

        if (data.success) {
            const results = data.all_returned;
            const stats = data.stats;

            resultDiv.innerHTML = `
                <div class="result-box success">
                    <span class="badge badge-success">ROBUST WATERMARK CREATED</span>
                    <p><strong>${data.message}</strong></p>
                </div>

                <div class="text-comparison">
                    <div class="text-box">
                        <h3>Original Text</h3>
                        <p>${text}</p>
                    </div>
                    <div class="text-box">
                        <h3>Watermarked Text</h3>
                        <p style="color: #28a745; font-weight: 600;">${data.watermarked_text}</p>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">P-value of watermarked text</div>
                        <div class="stat-value" style="color: #28a745;">${stats["evaluation_metrics"]["p_value"]}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Texts Similarity</div>
                        <div class="stat-value" style="color: #28a745;">${results["quality"]["semantic_similarity"]}%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Original Character Count</div>
                        <div class="stat-value">${stats["text_original_length"]}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Watermarked Character Count</div>
                        <div class="stat-value">${stats["text_wm_length"]}</div>
                    </div>
                </div>

                <div class="certificate">
                    <div"><strong>Execution Time: ${data.seconds_exec} s</div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${error.message}<br><small>Make sure the backend is running on port 5001</small></div>`;
    }
}

// ============================================================================
// DETECT WATERMARK
// ============================================================================

async function detectWatermark() {
    const text = document.getElementById('detectText').value.trim();
    const threshold = parseFloat(document.getElementById('threshold').value)/1000;

    if (!text) {
        alert('Please enter text to check');
        return;
    }

    const resultDiv = document.getElementById('detectResult');
    const chartsDiv = document.getElementById('detectCharts');
    resultDiv.innerHTML = '<div class="loading active"><div class="spinner"></div><p style="margin-top: 15px; color: #666;">Detecting watermark with statistical analysis...</p></div>';
    chartsDiv.innerHTML = '';

    try {
        const response = await fetch(`${API_URL}/api/watermark/detect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, threshold: threshold })
        });

        const data = await response.json();

        if (data.success) {
            const detected = data.is_watermarked;
            const details = data.details;

            if (detected) {

                resultDiv.innerHTML = `
                    <div class="result-box success">
                        <span class="badge badge-success">WATERMARK DETECTED</span>
                        <p><strong>P-value: ${details["p-value"]}</strong></p>
                        <p><strong>because p-value threshold (${details["threshold"]}) is higher</p>
                    </div>`;

            } else {
       
                    resultDiv.innerHTML = `
                        <div class="result-box error">
                            <span class="badge badge-danger">NO WATERMARK DETECTED</span>
                        <p><strong>P-value: ${details["p-value"]}</strong></p>
                        <p><strong>because p-value threshold (${details["threshold"]}) is lower</p>
                        </div>`;

           }
        } else {
            resultDiv.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${error.message}</div>`;
    }
}

// ============================================================================
// ATTACK PARAMETER UI
// ============================================================================

function slider(name, id, min, max, value, step = 0.01) {
    return `
    <div class="slider-container">
        <label>
            ${name}: <span class="slider-value" id="${id}Value">${value}</span>
        </label>
        <input type="range" class="slider"
            id="${id}"
            min="${min}" max="${max}" step="${step}" value="${value}"
            oninput="document.getElementById('${id}Value').innerText = this.value">
    </div>`;
}

function numberInput(name, id, min, value) {
    return `
    <div class="form-group">
        <label>${name}</label>
        <input type="number" id="${id}" min="${min}" value="${value}">
    </div>`;
}

function updateAttackParameters() {
    const type = document.getElementById("attackType").value;
    const container = document.getElementById("attackParameters");
    let html = "";

    switch (type) {

        case "copy_paste":
            html += slider("Dilution Rate", "cp_dilution", 0.01, 1, 0.3);
            html += slider("Position", "cp_position", 0, 1, 0.3);
            break;

        case "insert":
            html += slider("Insertion Coefficient", "insert_coef", 0, 1, 0.3);
            break;

        case "insert_noise":
            html += slider("Noise Coefficient", "noise_coef", 0, 1, 0.3);
            break;

        case "delete":
            html += slider("Deletion Coefficient", "delete_coef", 0, 1, 0.3);
            break;

        case "generative":
            html += numberInput("Token Addition Frequency", "gen_freq", 1, 5);
            break;

        case "synonym":
            html += slider("Max Replace Ratio", "syn_max_ratio", 0, 1, 0.3);
            html += slider("Replace Probability", "syn_prob", 0, 1, 0.5);
            break;

        case "reorder":
            html += slider("Strength", "reorder_strength", 0.01, 1, 0.3);
            html += numberInput("Distance (max words)", "reorder_distance", 0, 5);
            break;

        case "syn_transform":
            html += slider("Strength", "syn_transform_strength", 0, 1, 0.3);
            break;

        case "paraphrase":
            html += slider("Temperature", "para_temp", 0, 1, 0.8);
            break;

        case "translation":
            html += `<div class="form-group">
                    <label for="langtype">Language</label>
                    <select id="langtype">
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="it">Italian</option>
                        <option value="pt">Portuguese</option>
                        <option value="de">German</option>
                        <option value="zh-CN">Chinese Simplified</option>
                        <option value="ja">Japanese</option>
                        <option value="ko">Korean</option>
                        <option value="ru">Russian</option>
                        <option value="ar">Arabic</option>
                    </select>
                </div>`;
            break;
    }

    container.innerHTML = html;
}

// initialize when page loads
document.addEventListener("DOMContentLoaded", updateAttackParameters);


// ============================================================================
// TEST ATTACK
// ============================================================================

async function testAttack() {
    const text = document.getElementById('testText').value.trim();
    const attackType = document.getElementById('attackType').value;
    const threshold = 0.01;

    if (!text) {
        alert('Please enter text to test');
        return;
    }

    // Collect parameters dynamically
    let params = {};

    switch (attackType) {
        case "copy_paste":
            params.dilution_rate = parseFloat(document.getElementById("cp_dilution").value);
            params.position = parseInt(document.getElementById("cp_position").value);
            break;

        case "insert":
            params.coefficient = parseFloat(document.getElementById("insert_coef").value);
            break;

        case "insert_noise":
            params.coefficient = parseFloat(document.getElementById("noise_coef").value);
            break;

        case "delete":
            params.coefficient = parseFloat(document.getElementById("delete_coef").value);
            break;

        case "generative":
            params.token_frequency = parseInt(document.getElementById("gen_freq").value);
            break;

        case "synonym":
            params.max_replace_ratio = parseFloat(document.getElementById("syn_max_ratio").value);
            params.replace_prob = parseFloat(document.getElementById("syn_prob").value);
            break;

        case "reorder":
            params.strength = parseFloat(document.getElementById("reorder_strength").value);
            params.distance = parseInt(document.getElementById("reorder_distance").value);
            break;

        case "syn_transform":
            params.strength = parseFloat(document.getElementById("syn_transform_strength").value);
            break;

        case "paraphrase":
            params.temperature = parseFloat(document.getElementById("para_temp").value);
            break;

        case "translation":
            params.lang = document.getElementById("langtype").value;
            break;
    }

    const resultDiv = document.getElementById('testResult');
    const chartsDiv = document.getElementById('testCharts');
    resultDiv.innerHTML = '<div class="loading active"><div class="spinner"></div><p style="margin-top: 15px; color: #666;">Launching attack and testing detection...</p></div>';
    chartsDiv.innerHTML = '';

    try {
        const response = await fetch(`${API_URL}/api/watermark/test-attack`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                attack_type: attackType,
                parameters: params,
                threshold: threshold
            })
        });

        const data = await response.json();

        if (data.success) {
            const detected = data.is_detected;
            const attack = data.attack_analysis;
            const details = data.detection_details;

            resultDiv.innerHTML = `
                <div class="result-box ${detected ? 'success' : 'error'}">
                    <span class="badge ${detected ? 'badge-success' : 'badge-danger'}">
                        ${detected ? 'WATERMARK SURVIVED ATTACK' : 'WATERMARK NOT DETECTED'}
                    </span>
                    <p><strong>Attack: ${attackType}</strong></p>
                    <p>Detection P-value: ${details['p-value']} </p>
                </div>

                <div class="text-comparison">
                    <div class="text-box">
                        <h3>Original Text</h3>
                        <p>${data.original_text}</p>
                    </div>
                    <div class="text-box">
                        <h3>Attacked Text</h3>
                        <p style="color: #dc3545;">${data.attacked_text}</p>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Words Deleted</div>
                        <div class="stat-value" style="color: #dc3545;">${attack.deletions}</div>
                        <small>${attack.deletion_rate.toFixed(1)}%</small>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Words Inserted</div>
                        <div class="stat-value" style="color: #ffc107;">${attack.insertions}</div>
                        <small>${attack.insertion_rate.toFixed(1)}%</small>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Words Substituted</div>
                        <div class="stat-value" style="color: #fd7e14;">${attack.substitutions}</div>
                        <small>${attack.substitution_rate.toFixed(1)}%</small>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Words Preserved</div>
                        <div class="stat-value" style="color: #28a745;">${attack.unchanged}</div>
                        <small>${attack.preservation_rate.toFixed(1)}%</small>
                    </div>
                </div>
            `;

            // Create attack analysis chart
            createAttackBreakdownChart(chartsDiv, attack);
        } else {
            resultDiv.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${error.message}</div>`;
    }
}

// ============================================================================
// ANALYZE ROBUSTNESS
// ============================================================================

function Test_Chart(y_waterm, y_clean, params, attack){

	const canvas=document.getElementById('analysisCharts')

const Number_Axis=Object.keys(params).length

if (Number_Axis==1){



const firstKey = Object.keys(params)[0];

x=params[firstKey]

const min = Math.min(...y_waterm);
const max = Math.max(...y_clean);
const padding = (max - min) * 0.1;


if (attack == "Translation") { // Exception, Bar graph for Translation attack

var lang = {'es': 'Spanish', 'fr' : "French", 'de' : "German", 'it' : "Italian", 'pt' : "Portuguese", 'zh-CN' : "Chinese",
 'ja' : "Japanese", 'ko' : "Korean", 'ru' : "Russian", 'ar' : "Arabic"}

var trace1 = {
  x: x.map(i => lang[i]),
  y: y_waterm,
  name: 'Watermarked text',
  type: 'bar'
};
var trace2 = {
  x: x.map(i => lang[i]),
  y: y_clean,
  name: 'Not watermarked (clean) text',
  type: 'bar'
};
var data1 = [trace1, trace2];

var layout = {
  barmode: 'group',
  title: {
    text:`<b>${attack} attack. P-value vs Attack parameters</b>`,
	font: {
	family: 'Segoe UI',
      size: 24
    },
  },
  shapes:[ {
        type: 'line',
        xref: 'paper',
        x0: 0,
        y0: 0.01,
        x1: 1,
        y1: 0.01,
        showlegend:true,
        name: "Decision threshold 0.01",
      line:{
            color: 'lightgreen',
            width: 5,
            dash:'dot'
            }
  }],
  xaxis: {
    title: {
      text: `${firstKey}`,
	  family: 'Segoe UI',
	  size: 12
    },
  },
  yaxis: {
    title: {
      text: 'P-Value',
	  family: 'Segoe UI',
	  size: 12

    },
  range: [0 , max + padding],
  tick0: -0.2,
  dtick: 0.1,
  tickformat: '.2f'
  }
};

}
else { // 2D Graph for attacks with 1 parameter
var trace1 = {
  x: x,
  y: y_waterm,
  name: 'Watermarked text',
  type: 'scatter'
};
var trace2 = {
  x: x,
  y: y_clean,
  name: 'Not watermarked (clean) text',
  type: 'scatter'
};
var data1 = [trace1, trace2];

var layout = {
  title: {
    text:`<b>${attack} attack. P-value vs Attack parameters</b>`,
	font: {
	family: 'Segoe UI',
      size: 24
    },
  },
  shapes:[ {
        type: 'line',
        xref: 'paper',
        x0: 0,
        y0: 0.01,
        x1: 1,
        y1: 0.01,
        showlegend:true,
        name: "Decision threshold 0.01",
      line:{
            color: 'lightgreen',
            width: 5,
            dash:'dot'
            }
  }],
  xaxis: {
    title: {
      text: `${firstKey}`,
	  family: 'Segoe UI',
	  size: 12
    },
  },
  yaxis: {
    title: {
      text: 'P-Value',
	  family: 'Segoe UI',
	  size: 12
     
    },
  range: [-0.1 , max + padding],
  tick0: -0.2,      
  dtick: 0.1,    
  tickformat: '.1f'
  }
};
}
}else{ // 3D Graph for attacks with 2 parameters

	let x=params[Object.keys(params)[1]];
	let y= params[Object.keys(params)[0]];
	
	let x_num_values=y_waterm.length/y.length;
	
	let Z_waterm=[];
	let Z_clean=[];
	for (let i = 0; i < y.length; i++) {
		 let currentXRow = y_waterm.slice(i*x_num_values, (i+1)*x_num_values);
		 Z_waterm.push(currentXRow);
		 let currentXRow_cl = y_clean.slice(i*x_num_values, (i+1)*x_num_values);
		 Z_clean.push(currentXRow_cl);	  
	};
	
	const colorMatrixWater = Z_waterm.map(row => row.map(v => Math.sqrt(v)));
	const targetScaled = Math.sqrt(0.01); // This is 0.1
		
	const trace1 = {
	  z: Z_waterm,
	  x: x,
	  y: y,
	  type: 'surface',
	  name:"Watermarked text",
	   surfacecolor: colorMatrixWater,
	     colorscale: [
    [0, 'rgb(0,0,128)'],
    [targetScaled/1, 'rgb(255, 255, 0)'],
    [1, 'rgb (255,0,0)']
  ], colorbar: {
    tickvals: [0, targetScaled, 1],
    ticktext: ['0 ', '0.01 (Threshold)', '1']
  },
  cmin: 0,
  cmax: 1,
   showscale: true,
	 hovertemplate: 
    'x: %{x:.1f}<br>' +
    'y: %{y:.1f}<br>' +    
    'z: %{z:.3f}' 
	};
	
const colorMatrixClean = Z_clean.map(row => row.map(v => Math.sqrt(v)));

		const trace2 = {
	  z: Z_clean,
	  x: x,
	  y: y,
	  type: 'surface',
	  surfacecolor: colorMatrixClean,
	  colorscale: [
	[0, 'rgb(0,0,128)'],
    [targetScaled/1, 'rgb(255, 255, 0)'],
    [1, 'rgb (255,0,0)']
  ],
  cmin: 0,
  cmax: 1,

    colorbar: {
    tickvals: [0, targetScaled, 1],
    ticktext: ['0 ', '0.01 (Threshold)', '1']
  },
	  name:"Not watermarked (clean) text",
	 hovertemplate: 
    'x: %{x:.1f}<br>' +
    'y: %{y:.1f}<br>' +    
    'z: %{z:.3f}' 
	};
	
	var data1 = [trace1, trace2];
const min = Math.min(...y_waterm);
const max = Math.max(...y_clean);
const padding = (max - min) * 0.1;


if (attack == "Reorder") {
	y_dtick = 1
}
else {
	y_dtick = 0.2
}


var layout = {
  title: {
    text:`<b>${attack} attack. P-value vs Attack parameters</b>`,
	font: {
	family: 'Segoe UI',
      size: 24
    },
  },
  updatemenus: [{
    type: 'dropdown',
    direction: 'down',
    x: 0.1,
    y: 1.1,
    buttons: [
      {
        label: 'Show All',
        method: 'restyle',
        args: ['visible', [true, true]]
      },
      {
        label: 'Watermarked Only',
        method: 'restyle',
        args: ['visible', [true, false]]
      },
      {
        label: 'Non-Watermarked Only',
        method: 'restyle',
        args: ['visible', [false, true]]
      }
    ]
  }],
 autosize: false,
  width: 1200,
  height: 700,
  margin: {
    l: 65,
    r: 50,
    b: 65,
    t: 90
  },
  
  
  //surface 0.01
  scene: {
	  
  xaxis: {
    title: {
      text: `x (${Object.keys(params)[1]})`,
	  family: 'Segoe UI',
	  size: 12
    },
	tick0: 0,      
  dtick: 0.2,    
  tickformat: '.1f'
  },
  yaxis: {
    title: {
      text: `y (${Object.keys(params)[0]})`,
	  family: 'Segoe UI',
	  size: 12
     
    },
	tick0: 0,      
  dtick: y_dtick,    
  tickformat: '.1f'
  },
    zaxis: {
    title: {
      text: 'z (P-value)',
	  family: 'Segoe UI',
	  size: 12
     
    },
  range: [0 , max + padding],
  tick0: -0.2,      
  dtick: 0.1,    
  tickformat: '.1f'
  }
  }
};
}
Plotly.newPlot(canvas, data1, layout);
}

function Run_Charts(){
		const attack=document.getElementById('attackType2').value;
		const resultDiv  = document.getElementById('analysisResult');
		
        const results = data['results'][attack];   // dictionary of huge resutls
        const metrics1 = results['metrics'];   // {TPR, FPR, F1}
        // ── Metrics cards (TPR / FPR / F1 ) ──
        renderMetrics(metrics1);
        // ── Summary card ──
        const totalDetected = metrics1['detected_total'];
	
        resultDiv.innerHTML = `
            <div class="result-box success">
                <span class="badge badge-success">ANALYSIS COMPLETE</span>
                <p><strong>${metrics1['total']} attack scenarios evaluated &nbsp;|&nbsp;
                   ${totalDetected} detected &nbsp;|&nbsp;
                   ${metrics1['total']- totalDetected} evaded</strong></p>
			   <p><strong> ${Math.floor(data["analysis_time_sec"]/60)} min ${Math.round(data["analysis_time_sec"] % 60 * 100) / 100} sec </strong></p>
            </div>`;

		Test_Chart( results['P_value_watermarked'],results['P_value_clean'],results['params'],document.getElementById(document.getElementById('attackType2').value).innerHTML )
}

// Chart instances — destroyed before each re-render to avoid "canvas in use" errors
let _strengthChartInst = null;


async function analyzeRobustness() {

    const clean_text = document.getElementById('cleanText').value.trim();
    const wm_text = document.getElementById('watermarkedText').value.trim();

    if (!clean_text || !wm_text) {
        alert('Please enter both texts to analyze');
        return;
    }

    const loadingDiv = document.getElementById('analysisLoading');
    const resultDiv  = document.getElementById('analysisResult');

    loadingDiv.style.display = 'block';
    resultDiv.innerHTML = '';

    const metricsPanel = document.getElementById('metricsPanel');
    if (metricsPanel) metricsPanel.innerHTML = '';
	const ChoiceButton  = document.getElementById('showChoiceButton');

    // Destroy old chart instances, then rebuild the canvas elements fresh
    if (_strengthChartInst) { _strengthChartInst.destroy(); _strengthChartInst = null; }

    try {
        const response = await fetch(`${API_URL}/api/watermark/analyze-robustness`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ watermarked_text: wm_text, clean_text: clean_text})
        });

        globalThis.data = await response.json();

		
        loadingDiv.style.display = 'none';
        if (!data.success) {
            resultDiv.innerHTML =
                `<div class="result-box error"><strong>Error:</strong> ${data.error}</div>`;
            return;
        }
		
		//innnerHTML - 
		ChoiceButton.innerHTML=`<br><br>
				<div class="form-group">
                    <h3 for="attackType2">Attack Type</h3><br>
                    <select id="attackType2" onchange="Run_Charts()">
                        <option id="copy_paste" selected="selected" value="copy_paste"> Copy-Paste</option>
                        <option id="insert" value="insert">Insert</option>
                        <option id="insert_noise" value="insert_noise">Insert Noise</option>
                        <option id="delete" value="delete">Delete</option>
                        <option id="generative" value="generative">Generative</option>
                        <option id="synonym" value="synonym">Synonym</option>
                        <option id="reorder" value="reorder">Reorder</option>
                        <option id="syn_transform" value="syn_transform">Syn Transform</option>
                        <option id="paraphrase" value="paraphrase">Paraphrase</option>
                        <option id="translation" value="translation">Translation</option>
                    </select>
                </div>`;
		
		Run_Charts();

		
		
    } catch (error) {

        loadingDiv.style.display = 'none';
        resultDiv.innerHTML =
            `<div class="result-box error"><strong>Error:</strong> ${error.message}</div>`;
    }
}

// ============================================================================
// CHART CREATION FUNCTIONS
// ============================================================================

function createAttackBreakdownChart(container, attack) {
    const chartDiv = document.createElement('div');
    chartDiv.className = 'chart-container';
    chartDiv.innerHTML = '<div class="chart-title">Attack Breakdown</div>';

    const canvas = document.createElement('canvas');
    chartDiv.appendChild(canvas);
    container.appendChild(chartDiv);

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: ['Deletions', 'Insertions', 'Substitutions', 'Unchanged'],
            datasets: [{
                label: 'Word Count',
                data: [attack.deletions, attack.insertions, attack.substitutions, attack.unchanged],
                backgroundColor: ['#dc3545', '#ffc107', '#fd7e14', '#28a745']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Number of Words' }
                }
            }
        }
    });
}

function renderMetrics(metrics) {

    const panel = document.getElementById("metricsPanel");

    panel.innerHTML = `
        <div class="metric-card">
            <div class="metric-value">${metrics.TPR.toFixed(3)}</div>
            <div class="metric-label">TPR</div>
        </div>

        <div class="metric-card">
            <div class="metric-value">${metrics.FPR.toFixed(3)}</div>
            <div class="metric-label">FPR</div>
        </div>

        <div class="metric-card">
            <div class="metric-value">${metrics.F1.toFixed(3)}</div>
            <div class="metric-label">F1 Score</div>
        </div>
    `;
}