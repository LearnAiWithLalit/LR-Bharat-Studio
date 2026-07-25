import re

html_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web/index.html'
studio_py_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web_studio.py'

# ── 1. Update web_studio.py stream_pipeline signature and agent execution ──
with open(studio_py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

old_sig = """@app.get("/api/pipeline/stream")
async def stream_pipeline(
    prompt: str,
    language: str = "auto",
    format: str = "auto",
    duration: float = 5.0,
    llm_mode: str = "fast",
    fallback_mode: str = "auto/claude",
):"""

new_sig = """@app.get("/api/pipeline/stream")
async def stream_pipeline(
    prompt: str,
    language: str = "auto",
    format: str = "auto",
    duration: float = 5.0,
    llm_mode: str = "fast",
    fallback_mode: str = "auto/claude",
    agent1_llm: str = "auto",
    agent2_llm: str = "auto",
    agent4_tts: str = "chatterbox",
    agent6_img: str = "flux",
):"""

if "@app.get(\"/api/pipeline/stream\")" in py_content:
    py_content = py_content.replace(old_sig, new_sig)

# In Agent 1, use mode = (agent1_llm if agent1_llm != "auto" else llm_mode)
old_ag1_call = """plan_raw, resolved_model, backend_used = call_llm(
                plan_prompt,
                system_prompt="You are an expert story planner. Always return valid raw JSON.",
                mode=llm_mode,
                fallback_mode=fallback_mode,
                return_meta=True,
            )"""

new_ag1_call = """ag1_mode = agent1_llm if (agent1_llm and agent1_llm != "auto") else llm_mode
            plan_raw, resolved_model, backend_used = call_llm(
                plan_prompt,
                system_prompt="You are an expert story planner. Always return valid raw JSON.",
                mode=ag1_mode,
                fallback_mode=fallback_mode,
                return_meta=True,
            )"""

py_content = py_content.replace(old_ag1_call, new_ag1_call)

# In Agent 2, use mode = (agent2_llm if agent2_llm != "auto" else llm_mode)
old_ag2_call = """script_raw, resolved_model_2, backend_used_2 = call_llm(
                script_prompt,
                system_prompt="You are a professional children's story scriptwriter. Return raw JSON array only.",
                mode=llm_mode if llm_mode != "fast" else "pro",
                fallback_mode=fallback_mode,
                return_meta=True,
            )"""

new_ag2_call = """ag2_mode = agent2_llm if (agent2_llm and agent2_llm != "auto") else (llm_mode if llm_mode != "fast" else "pro")
            script_raw, resolved_model_2, backend_used_2 = call_llm(
                script_prompt,
                system_prompt="You are a professional children's story scriptwriter. Return raw JSON array only.",
                mode=ag2_mode,
                fallback_mode=fallback_mode,
                return_meta=True,
            )"""

py_content = py_content.replace(old_ag2_call, new_ag2_call)

with open(studio_py_path, 'w', encoding='utf-8') as f:
    f.write(py_content)

print("Updated web_studio.py with per-agent stream parameters successfully!")

# ── 2. Update web/index.html with Collapsible Accordion Cards & Per-Agent Selectors ──
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add CSS for Collapsible Accordion Cards
accordion_css = """
  /* Collapsible Accordion Cards in Sidebar */
  .accordion-card{ background:var(--bg-card); border:1px solid var(--line); border-radius:14px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.3); transition:border-color .2s; }
  .accordion-card:hover{ border-color:rgba(255,122,26,0.3); }

  .accordion-header{ padding:14px 18px; background:var(--bg-card-2); display:flex; align-items:center; justify-content:space-between; cursor:pointer; font-family:var(--display); font-weight:600; font-size:13.5px; user-select:none; transition:background .15s; border-bottom:1px solid var(--line); }
  .accordion-header:hover{ background:rgba(255,122,26,0.08); }

  .accordion-icon{ font-size:11px; color:var(--orange-2); transition:transform .2s; font-family:var(--mono); }

  .accordion-body{ padding:18px; display:flex; flex-direction:column; gap:14px; }
  .accordion-body.collapsed{ display:none!important; }
"""

if '.accordion-card' not in html_content:
    html_content = html_content.replace('</style>', accordion_css + '\n</style>')

# Add toggleAccordion JS function
toggle_js = """
  // Collapsible Accordion Toggle Helper
  function toggleAccordion(id){
    const body = document.getElementById('body-' + id);
    const icon = document.getElementById('icon-' + id);
    if(body){
      body.classList.toggle('collapsed');
      if(icon){
        icon.textContent = body.classList.contains('collapsed') ? '▶' : '▼';
      }
    }
  }
"""

if 'function toggleAccordion' not in html_content:
    html_content = html_content.replace('<script>', '<script>\n' + toggle_js)

# Replace Screen 1 Sidebar with Collapsible Accordion Cards
new_sidebar = """    <!-- Left Sidebar: Controls & Settings -->
    <div class="screen1-sidebar" id="screen1Sidebar">

      <!-- Card 1: Language & Voice Cast (Expanded by default) -->
      <div class="accordion-card">
        <div class="accordion-header" onclick="toggleAccordion('langSection')">
          <span>🌐 Language & Voice Cast</span>
          <span class="accordion-icon" id="icon-langSection">▼</span>
        </div>
        <div class="accordion-body" id="body-langSection">
          <div class="form-row">
            <div class="form-group">
              <div class="form-label">Language (Chatterbox v3):</div>
              <select id="langSelect" class="form-select">
                <optgroup label="⭐ Primary Supported">
                  <option value="Hindi" selected>🇮🇳 Hindi (हिन्दी) [hi]</option>
                  <option value="English">🇬🇧 English [en]</option>
                  <option value="Both">🇮🇳 Both (Hinglish)</option>
                </optgroup>
                <optgroup label="🌐 23 Chatterbox v3 Multilingual Languages">
                  <option value="Arabic">🇸🇦 Arabic [ar]</option>
                  <option value="Chinese">🇨🇳 Chinese / Mandarin [zh]</option>
                  <option value="Danish">🇩🇰 Danish [da]</option>
                  <option value="Dutch">🇳🇱 Dutch [nl]</option>
                  <option value="Finnish">🇫🇮 Finnish [fi]</option>
                  <option value="French">🇫🇷 French [fr]</option>
                  <option value="German">🇩🇪 German [de]</option>
                  <option value="Greek">🇬🇷 Greek [el]</option>
                  <option value="Hebrew">🇮🇱 Hebrew [he]</option>
                  <option value="Italian">🇮🇹 Italian [it]</option>
                  <option value="Japanese">🇯🇵 Japanese [ja]</option>
                  <option value="Korean">🇰🇷 Korean [ko]</option>
                  <option value="Malay">🇲🇾 Malay [ms]</option>
                  <option value="Norwegian">🇳🇴 Norwegian [no]</option>
                  <option value="Polish">🇵🇱 Polish [pl]</option>
                  <option value="Portuguese">🇵🇹 Portuguese [pt]</option>
                  <option value="Russian">🇷🇺 Russian [ru]</option>
                  <option value="Spanish">🇪🇸 Spanish [es]</option>
                  <option value="Swahili">🇰🇪 Swahili [sw]</option>
                  <option value="Swedish">🇸🇪 Swedish [sv]</option>
                  <option value="Turkish">🇹🇷 Turkish [tr]</option>
                </optgroup>
              </select>
            </div>
            <div class="form-group">
              <div class="form-label">Output Aspect Ratio:</div>
              <select id="formatSelect" class="form-select">
                <option value="youtube_long_form" selected>YouTube Long (16:9 4K)</option>
                <option value="youtube_shorts">YouTube Shorts (9:16 4K)</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <div class="form-label">Available Voice Cast (Voice Registry):</div>
            <div class="cast-chips">
              <div class="chip selected" data-voice="kid_young_1">👦 Chintu (~5yr)</div>
              <div class="chip selected" data-voice="kid_young_2">🧒 Pappu (~7yr)</div>
              <div class="chip selected" data-voice="kid_elder_sister">👧 Meena (Elder Sister)</div>
              <div class="chip selected" data-voice="narrator">🎙️ Narrator (Male)</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Card 2: Global Model Combos (Expanded by default) -->
      <div class="accordion-card">
        <div class="accordion-header" onclick="toggleAccordion('combosSection')">
          <span>💬 & 🚀 Global Model Combos</span>
          <span class="accordion-icon" id="icon-combosSection">▼</span>
        </div>
        <div class="accordion-body" id="body-combosSection">
          <!-- 1. Chat Advisor Combo -->
          <div class="form-group">
            <div class="form-label">
              <span>1. 💬 Chat Advisor Combo:</span>
              <span class="form-subnote" id="chatComboCountTag">OmniRoute Combos</span>
            </div>
            <div class="combo-input-wrap">
              <select id="chatComboSelect" class="form-select" onchange="handleComboChange('chat')">
                <option value="auto/claude/opus" selected>Loading dashboard combos...</option>
              </select>
              <input type="text" id="chatComboInput" class="form-input" style="display:none; margin-top:6px;" placeholder="Type custom combo...">
            </div>
          </div>

          <!-- 2. Pipeline Primary Combo -->
          <div class="form-group">
            <div class="form-label">
              <span>2. 🚀 Pipeline Primary Combo (Agents 1-7):</span>
              <span class="form-subnote" id="pipelineComboCountTag">OmniRoute Combos</span>
            </div>
            <div class="combo-input-wrap">
              <select id="pipelineComboSelect" class="form-select" onchange="handleComboChange('pipeline')">
                <option value="antigravity/gemini-3.5-flash-low" selected>Loading dashboard combos...</option>
              </select>
              <input type="text" id="pipelineComboInput" class="form-input" style="display:none; margin-top:6px;" placeholder="Type custom combo...">
            </div>
          </div>

          <!-- 3. Fallback Combo & Target Duration -->
          <div class="form-row">
            <div class="form-group">
              <div class="form-label">3. Fallback Combo / Model:</div>
              <select id="fallbackSelect" class="form-select">
                <option value="auto/claude" selected>Combo: auto/claude</option>
                <option value="antigravity/gemini-3.5-flash-low">Gemini 3.5 Flash</option>
                <option value="free">FreeBuff (100% Free)</option>
              </select>
            </div>
            <div class="form-group">
              <div class="form-label">Target Duration (~Mins):</div>
              <input type="number" id="durationInput" class="form-input" min="1" max="120" value="5" step="1" placeholder="5">
            </div>
          </div>
          <div style="font-size:11px; color:var(--text-faint); font-family:var(--mono); margin-top:-4px;">
            💡 <i>Target duration is approximate (~4 to 6 min flexible audio pacing).</i>
          </div>
        </div>
      </div>

      <!-- Card 3: Per-Agent Model & Engine Assignment (Collapsed by default) -->
      <div class="accordion-card">
        <div class="accordion-header" onclick="toggleAccordion('agentOverrideSection')">
          <span>🤖 Per-Agent Model & Engine Assignment</span>
          <span class="accordion-icon" id="icon-agentOverrideSection">▶</span>
        </div>
        <div class="accordion-body collapsed" id="body-agentOverrideSection">
          <!-- Agent 1 Override -->
          <div class="form-group">
            <div class="form-label">
              <span>Agent 1 · Topic Planner Combo:</span>
              <span class="form-subnote">Specific Combo</span>
            </div>
            <select id="ag1ComboSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="auto" selected>⚡ Pipeline Primary Combo (Default)</option>
            </select>
          </div>

          <!-- Agent 2 Override -->
          <div class="form-group">
            <div class="form-label">
              <span>Agent 2 · Script Writer Combo:</span>
              <span class="form-subnote">Specific Combo</span>
            </div>
            <select id="ag2ComboSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="auto" selected>⚡ Pipeline Primary Combo (Default)</option>
            </select>
          </div>

          <!-- Agent 3 Engine -->
          <div class="form-group">
            <div class="form-label">Agent 3 · Story Config Engine:</div>
            <select id="ag3EngineSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="local" selected>🖥️ Local Content Rules Engine (Default)</option>
              <option value="llm">⚡ Cloud LLM Combo</option>
            </select>
          </div>

          <!-- Agent 4 Audio / TTS -->
          <div class="form-group">
            <div class="form-label">Agent 4 · Audio & TTS Engine:</div>
            <select id="ag4TtsSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="chatterbox" selected>🎙️ Chatterbox Local Voice Clone (GPU - Default)</option>
              <option value="edge_tts">☁️ Edge-TTS (Free Neural Cloud)</option>
              <option value="cloud_combo">🌩️ Cloud Audio Combo</option>
            </select>
          </div>

          <!-- Agent 5 Audio QA -->
          <div class="form-group">
            <div class="form-label">Agent 5 · Audio QA Engine:</div>
            <select id="ag5QaSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="local" selected>🔍 Local VAD & RMS Inspector (Default)</option>
              <option value="cloud">☁️ Cloud Audio QA Inspector</option>
            </select>
          </div>

          <!-- Agent 6 Image Gen -->
          <div class="form-group">
            <div class="form-label">Agent 6 · 4K Image Gen Engine:</div>
            <select id="ag6ImageSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="flux" selected>🖼️ FLUX.1 Schnell Local (GPU - Default)</option>
              <option value="dreamshaper">🎨 DreamShaper XL (Local SDXL)</option>
              <option value="omniroute_combo">⚡ OmniRoute Image-Model Combo</option>
            </select>
          </div>

          <!-- Agent 7 Video Master -->
          <div class="form-group">
            <div class="form-label">Agent 7 · Video Master Engine:</div>
            <select id="ag7VideoSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="ffmpeg" selected>🎬 FFmpeg 4K Local Muxer (Default)</option>
              <option value="cloud">☁️ Cloud Video Encoder</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Card 4: OmniRoute Router (Collapsed by default) -->
      <div class="accordion-card">
        <div class="accordion-header" onclick="toggleAccordion('omniSection')">
          <span>4. 🔌 OmniRoute Router <span style="font-size:11px; color:var(--green); margin-left:6px;" id="omniOnlineTag">✓ Online (2585 Models Live)</span></span>
          <span class="accordion-icon" id="icon-omniSection">▶</span>
        </div>
        <div class="accordion-body collapsed" id="body-omniSection">
          <div class="omni-card">
            <div>
              <span style="color:var(--orange-2); font-weight:600;">🔌 OmniRoute Router</span>
              <div style="color:var(--text-dim); font-size:11px;" id="omniStatusText">Online · 2585 Models Available</div>
            </div>
            <div style="display:flex; gap:6px;">
              <button class="omni-btn" id="btnInspectModels">🔍 Inspect 280+ Models</button>
              <a class="omni-btn" href="http://localhost:3000" target="_blank">Setup ↗</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Card 5: System Hardware Watcher (Collapsed by default) -->
      <div class="accordion-card" id="sysBoxCard">
        <div class="accordion-header" onclick="toggleAccordion('sysSection')">
          <span>⚙️ Universal Hardware & Resource Box</span>
          <span class="accordion-icon" id="icon-sysSection">▶</span>
        </div>
        <div class="accordion-body collapsed" id="body-sysSection">
          <div class="sys-box" id="sysBox">
            <div class="sys-title">
              <span>⚙️ Universal Hardware & Resource Box</span>
              <span style="font-family:var(--mono); font-size:11px; color:var(--text-faint);" id="gpuStatusTag">Auto-detecting...</span>
            </div>
            <div class="sys-metric">
              <div class="sys-metric-head">
                <span id="gpuNameHead">🎮 GPU VRAM Utilization</span>
                <span id="vramLabel">0.0 / 0.0 GB (0%)</span>
              </div>
              <div class="progress-bg">
                <div class="progress-fill" id="vramBar" style="width: 0%;"></div>
              </div>
            </div>
            <div class="sys-metric">
              <div class="sys-metric-head">
                <span>🖥️ System RAM</span>
                <span id="ramLabel">0.0 / 0.0 GB (0%)</span>
              </div>
              <div class="progress-bg">
                <div class="progress-fill-blue" id="ramBar" style="width: 0%;"></div>
              </div>
            </div>
            <div class="sys-metric">
              <div class="sys-metric-head">
                <span>⚡ CPU: <b id="cpuBrandText" style="color:var(--text)">Auto-detecting CPU...</b> (<b id="cpuLabel">0%</b>)</span>
                <span>💾 Disk: <b id="diskLabel" style="color:var(--text)">0 GB free</b></span>
              </div>
            </div>
            <div class="sys-tags">
              <span class="sys-tag" id="backendTag">Auto Backend</span>
              <span class="sys-tag">Audio 24kHz</span>
              <span class="sys-tag">Real-ESRGAN 4K</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Card 6: AI Models & Agent Matrix Box (Collapsed by default) -->
      <div class="accordion-card" id="modelsBoxCard">
        <div class="accordion-header" onclick="toggleAccordion('matrixSection')">
          <span>5. 🤖 AI Models & Agent Matrix <span class="cost-badge" id="matrixCostBadge" style="margin-left:8px;">$0.00 API Cost</span></span>
          <span class="accordion-icon" id="icon-matrixSection">▶</span>
        </div>
        <div class="accordion-body collapsed" id="body-matrixSection">
          <div class="models-box" id="modelsBox">
            <div class="models-header">
              <span>🤖 AI Models & Agent Matrix</span>
            </div>
            <div class="agent-model-card" id="cardChat">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledChat"></span> 💬 Chat Advisor (Brainstorm)</span>
                <span style="color:var(--orange-2)">Live</span>
              </div>
              <div class="agent-model-primary" id="chatModelText">Combo: auto/claude/opus</div>
            </div>
            <div class="agent-model-card" id="cardAg1">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg1"></span> Agent 1 · Topic Planner</span>
                <span style="color:var(--green)">$0</span>
              </div>
              <div class="agent-model-primary" id="ag1ModelText">Primary: antigravity/gemini-3.5-flash-low</div>
              <div class="agent-model-fallback" id="ag1FallbackText">Fallback: auto/claude</div>
            </div>
            <div class="agent-model-card" id="cardAg2">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg2"></span> Agent 2 · Script Writer</span>
                <span style="color:var(--green)">$0</span>
              </div>
              <div class="agent-model-primary" id="ag2ModelText">Primary: antigravity/gemini-3.5-flash-low</div>
              <div class="agent-model-fallback" id="ag2FallbackText">Fallback: auto/claude</div>
            </div>
            <div class="agent-model-card" id="cardAg3">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg3"></span> Agent 3 · Story Config</span>
                <span style="color:var(--blue)">Local</span>
              </div>
              <div class="agent-model-primary" id="ag3ModelText">Engine: Content Analyzer Rules</div>
            </div>
            <div class="agent-model-card" id="cardAg4">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg4"></span> Agent 4 · Audio & Music</span>
                <span style="color:var(--green)">$0 Local</span>
              </div>
              <div class="agent-model-primary" id="ag4ModelText">TTS: Chatterbox (Voice Clone)</div>
              <div class="agent-model-fallback">Music: Procedural Generator</div>
            </div>
            <div class="agent-model-card" id="cardAg5">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg5"></span> Agent 5 · Audio QA</span>
                <span style="color:var(--blue)">Local</span>
              </div>
              <div class="agent-model-primary" id="ag5ModelText">Inspector: Strict VAD & RMS</div>
            </div>
            <div class="agent-model-card" id="cardAg6">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg6"></span> Agent 6 · 4K Image Gen</span>
                <span style="color:var(--green)">$0 Local</span>
              </div>
              <div class="agent-model-primary" id="ag6ModelText">Hero: FLUX.1 Schnell</div>
              <div class="agent-model-fallback">Scenes: DreamShaperXL + IP-Adapter</div>
            </div>
            <div class="agent-model-card" id="cardAg7">
              <div class="agent-model-title">
                <span><span class="led-dot" id="ledAg7"></span> Agent 7 · Video Master</span>
                <span style="color:var(--blue)">Local</span>
              </div>
              <div class="agent-model-primary" id="ag7ModelText">Muxer: FFmpeg 4K Encoder</div>
            </div>
            <div style="font-size:12px; font-weight:600; color:var(--text-dim); margin-top:6px;">Active Live Combos & Engines:</div>
            <div class="free-combos-wrap" id="combosList">
              <div class="combo-item">
                <span>FreeBuff CLI</span>
                <span class="badge-free">No Key Required</span>
              </div>
              <div class="combo-item">
                <span>Chatterbox Voice</span>
                <span class="badge-free">Local GPU</span>
              </div>
              <div class="combo-item">
                <span>FLUX + SDXL</span>
                <span class="badge-free">Local GPU</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>"""

# Replace Screen 1 sidebar
html_content = re.sub(
    r'<!-- Left Sidebar: Controls & Settings -->.*?<!-- Center Main:',
    new_sidebar + '\n\n    <!-- Center Main:',
    html_content,
    flags=re.DOTALL
)

# Update showScreen JS to move accordion cards sysBoxCard and modelsBoxCard when switching screens
new_show_screen = """  // Screen Switcher Function
  function showScreen(num) {
    const s1 = document.getElementById('screen1');
    const s2 = document.getElementById('screen2');
    const nav1 = document.getElementById('navBtnScreen1');
    const nav2 = document.getElementById('navBtnScreen2');
    const sysCard = document.getElementById('sysBoxCard');
    const modelsCard = document.getElementById('modelsBoxCard');
    const s1Sidebar = document.getElementById('screen1Sidebar');
    const s2Sidebar = document.getElementById('screen2Sidebar');

    if(num === 1){
      if(s1) s1.classList.add('active');
      if(s2) s2.classList.remove('active');
      if(nav1) nav1.classList.add('active');
      if(nav2) nav2.classList.remove('active');
      if(s1Sidebar && sysCard && modelsCard){
        s1Sidebar.appendChild(sysCard);
        s1Sidebar.appendChild(modelsCard);
      }
    } else {
      if(s2) s2.classList.add('active');
      if(s1) s1.classList.remove('active');
      if(nav2) nav2.classList.add('active');
      if(nav1) nav1.classList.remove('active');
      if(s2Sidebar && sysCard && modelsCard){
        s2Sidebar.appendChild(sysCard);
        s2Sidebar.appendChild(modelsCard);
        // Automatically expand Matrix section on Screen 2 for easy viewing!
        const matrixBody = document.getElementById('body-matrixSection');
        const matrixIcon = document.getElementById('icon-matrixSection');
        if(matrixBody) matrixBody.classList.remove('collapsed');
        if(matrixIcon) matrixIcon.textContent = '▼';
      }
    }
  }"""

html_content = re.sub(
    r'// Screen Switcher Function.*?function showScreen\(num\)\s*\{.*?\n  \}',
    new_show_screen,
    html_content,
    flags=re.DOTALL
)

# Update fetchOmniRouteCombos JS to populate ag1ComboSelect and ag2ComboSelect
old_fetch_js = """      if(chatSelect) chatSelect.innerHTML = fullHtml;
      if(pipelineSelect) pipelineSelect.innerHTML = fullHtml;"""

new_fetch_js = """      const ag1Select = document.getElementById('ag1ComboSelect');
      const ag2Select = document.getElementById('ag2ComboSelect');

      if(chatSelect) chatSelect.innerHTML = fullHtml;
      if(pipelineSelect) pipelineSelect.innerHTML = fullHtml;

      const agentOptionHtml = '<option value="auto" selected>⚡ Pipeline Primary Combo (Default)</option>' + fullHtml;
      if(ag1Select) ag1Select.innerHTML = agentOptionHtml;
      if(ag2Select) ag2Select.innerHTML = agentOptionHtml;"""

html_content = html_content.replace(old_fetch_js, new_fetch_js)

# Update updateModelMatrix JS to handle per-agent overrides
new_matrix_func = """  function updateModelMatrix(){
    const chatModelText = document.getElementById('chatModelText');
    const ag1ModelText = document.getElementById('ag1ModelText');
    const ag2ModelText = document.getElementById('ag2ModelText');
    const ag3ModelText = document.getElementById('ag3ModelText');
    const ag4ModelText = document.getElementById('ag4ModelText');
    const ag5ModelText = document.getElementById('ag5ModelText');
    const ag6ModelText = document.getElementById('ag6ModelText');
    const ag7ModelText = document.getElementById('ag7ModelText');

    const chatLlm = getComboValue('chat') || "auto/claude/opus";
    const primary = getComboValue('pipeline') || "antigravity/gemini-3.5-flash-low";
    const fallback = document.getElementById('fallbackSelect') ? document.getElementById('fallbackSelect').value : "auto/claude";

    const ag1Select = document.getElementById('ag1ComboSelect');
    const ag2Select = document.getElementById('ag2ComboSelect');
    const ag3Select = document.getElementById('ag3EngineSelect');
    const ag4Select = document.getElementById('ag4TtsSelect');
    const ag5Select = document.getElementById('ag5QaSelect');
    const ag6Select = document.getElementById('ag6ImageSelect');
    const ag7Select = document.getElementById('ag7VideoSelect');

    const ag1Val = (ag1Select && ag1Select.value !== 'auto') ? ag1Select.value : primary;
    const ag2Val = (ag2Select && ag2Select.value !== 'auto') ? ag2Select.value : primary;

    if(chatModelText) chatModelText.textContent = `Combo: ${chatLlm}`;
    if(ag1ModelText) ag1ModelText.textContent = `Primary: ${ag1Val}`;
    if(ag2ModelText) ag2ModelText.textContent = `Primary: ${ag2Val}`;

    if(ag3ModelText) ag3ModelText.textContent = (ag3Select && ag3Select.value === 'llm') ? `Combo: ${primary}` : "Engine: Content Analyzer Rules";
    if(ag4ModelText) ag4ModelText.textContent = (ag4Select && ag4Select.value === 'edge_tts') ? "TTS: Edge-TTS (Free Cloud)" : ((ag4Select && ag4Select.value === 'cloud_combo') ? "TTS: Cloud Audio Combo" : "TTS: Chatterbox (Voice Clone)");
    if(ag5ModelText) ag5ModelText.textContent = (ag5Select && ag5Select.value === 'cloud') ? "Inspector: Cloud QA Inspector" : "Inspector: Strict VAD & RMS";
    if(ag6ModelText) ag6ModelText.textContent = (ag6Select && ag6Select.value === 'dreamshaper') ? "Hero: DreamShaper XL (Local SDXL)" : ((ag6Select && ag6Select.value === 'omniroute_combo') ? "Hero: Image-Model Combo" : "Hero: FLUX.1 Schnell");
    if(ag7ModelText) ag7ModelText.textContent = (ag7Select && ag7Select.value === 'cloud') ? "Muxer: Cloud Video Encoder" : "Muxer: FFmpeg 4K Encoder";

    const ag1FallbackText = document.getElementById('ag1FallbackText');
    const ag2FallbackText = document.getElementById('ag2FallbackText');
    if(ag1FallbackText) ag1FallbackText.textContent = `Fallback: ${fallback}`;
    if(ag2FallbackText) ag2FallbackText.textContent = `Fallback: ${fallback}`;
  }"""

html_content = re.sub(
    r'function updateModelMatrix\(\)\{.*?\n  \}',
    new_matrix_func,
    html_content,
    flags=re.DOTALL
)

# Update btnLaunch click event to pass per-agent params to SSE stream
old_launch_url = "const sseUrl = `/api/pipeline/stream?prompt=${encodeURIComponent(approvedPrompt)}&language=${encodeURIComponent(langSelect.value)}&format=${encodeURIComponent(formatSelect.value)}&duration=${encodeURIComponent(durationInput.value)}&llm_mode=${encodeURIComponent(pipelineComboInput.value.trim())}&fallback_mode=${encodeURIComponent(fallbackSelect.value)}`;"

new_launch_url = """    const ag1Sel = document.getElementById('ag1ComboSelect');
    const ag2Sel = document.getElementById('ag2ComboSelect');
    const ag4Sel = document.getElementById('ag4TtsSelect');
    const ag6Sel = document.getElementById('ag6ImageSelect');

    const sseUrl = `/api/pipeline/stream?prompt=${encodeURIComponent(approvedPrompt)}&language=${encodeURIComponent(langSelect.value)}&format=${encodeURIComponent(formatSelect.value)}&duration=${encodeURIComponent(durationInput.value)}&llm_mode=${encodeURIComponent(getComboValue('pipeline'))}&fallback_mode=${encodeURIComponent(fallbackSelect.value)}&agent1_llm=${encodeURIComponent(ag1Sel ? ag1Sel.value : 'auto')}&agent2_llm=${encodeURIComponent(ag2Sel ? ag2Sel.value : 'auto')}&agent4_tts=${encodeURIComponent(ag4Sel ? ag4Sel.value : 'chatterbox')}&agent6_img=${encodeURIComponent(ag6Sel ? ag6Sel.value : 'flux')}`;"""

html_content = html_content.replace(old_launch_url, new_launch_url)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Applied collapsible accordions & per-agent selection to index.html successfully!")
