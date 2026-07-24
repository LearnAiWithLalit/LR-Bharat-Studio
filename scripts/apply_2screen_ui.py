import os, re

html_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS Injection before </style>
css_to_add = """
  /* 2-Screen Studio Architecture */
  .screen-tabs{ display:flex; gap:6px; background:var(--bg-card); padding:4px; border-radius:999px; border:1px solid var(--line); }
  .nav-screen-btn{ background:none; border:none; color:var(--text-dim); padding:6px 14px; border-radius:999px; font-family:var(--display); font-size:12.5px; font-weight:600; cursor:pointer; transition:all .15s; }
  .nav-screen-btn.active{ background:var(--orange); color:#fff; box-shadow:0 0 10px rgba(255,122,26,0.4); }
  .nav-screen-btn:hover:not(.active){ color:var(--text); }

  .screen-view{ display:none; width:100%; min-height:calc(100vh - 70px); padding:20px 24px; position:relative; z-index:10; }
  .screen-view.active{ display:block; }

  /* Screen 1: Settings Sidebar + Centered Chat Section */
  .screen1-grid{ display:grid; grid-template-columns:420px 1fr; gap:24px; max-width:1600px; margin:0 auto; }
  .screen1-sidebar{ display:flex; flex-direction:column; gap:20px; }
  .screen1-main{ display:flex; flex-direction:column; gap:20px; }

  .panel-chat-hero{ background:var(--bg-card); border:1px solid var(--line); border-radius:16px; padding:24px; display:flex; flex-direction:column; gap:16px; box-shadow:0 20px 50px rgba(0,0,0,0.5); }
  .badge-advisor{ background:rgba(255,122,26,0.15); border:1px solid rgba(255,122,26,0.3); color:var(--orange-2); padding:4px 10px; border-radius:999px; font-family:var(--mono); font-size:11px; }

  .chat-thread-container.hero-chat{ height:440px; border-radius:14px; padding:16px; background:var(--bg); border:1px solid var(--line); }
  textarea.prompt-input.hero-prompt{ height:90px; font-size:14px; padding:12px; }

  /* Screen 2: Topbar + Workspace + Sidebar */
  .screen2-topbar{ display:flex; align-items:center; justify-content:space-between; background:var(--bg-card); border:1px solid var(--line); border-radius:12px; padding:12px 20px; margin-bottom:20px; }
  .btn-back-screen{ background:var(--bg-card-2); border:1px solid var(--line); color:var(--orange-2); padding:8px 16px; border-radius:8px; font-family:var(--display); font-weight:600; font-size:13px; cursor:pointer; display:flex; align-items:center; gap:8px; transition:all .15s; }
  .btn-back-screen:hover{ border-color:var(--orange); background:rgba(255,122,26,0.1); transform:translateX(-2px); }

  .screen2-grid{ display:grid; grid-template-columns:1fr 380px; gap:20px; }
  .screen2-sidebar{ display:flex; flex-direction:column; gap:20px; }
"""

if '.screen-tabs' not in content:
    content = content.replace('</style>', css_to_add + '\n</style>')

# 2. Update Header status with Screen navigation tabs
new_header_status = """  <div class="header-status">
    <div class="screen-tabs">
      <button class="nav-screen-btn active" id="navBtnScreen1" onclick="showScreen(1)">💬 1. Story Chat & Settings</button>
      <button class="nav-screen-btn" id="navBtnScreen2" onclick="showScreen(2)">🚀 2. Pipeline & Workspace</button>
    </div>
    <div class="status-badge">
      <div class="dot-green" id="serverDot"></div>
      <span id="serverText">Server Ready (port 8080)</span>
    </div>
    <div class="status-badge">
      <span id="activeAgentChip">State: Idle</span>
    </div>
  </div>"""

content = re.sub(r'<div class="header-status">.*?</div>\s*</header>', new_header_status + '\n</header>', content, flags=re.DOTALL)

# 3. Restructure HTML Body for 2 Screens
new_body_structure = """
<!-- Screen 1: Chat & Settings View -->
<div class="screen-view active" id="screen1">
  <div class="screen1-grid">

    <!-- Left Sidebar: Controls & Settings -->
    <div class="screen1-sidebar" id="screen1Sidebar">
      <div class="panel-input">
        <div class="panel-title">
          <span>⚙️ Studio Settings & Models</span>
          <span style="font-size:11px; font-family:var(--mono); color:var(--orange-2);">Config Panel</span>
        </div>

        <!-- Language & Aspect Ratio Selectors -->
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

        <!-- Searchable Chat Advisor Combo -->
        <div class="form-group">
          <div class="form-label">
            <span>💬 Chat Advisor Combo:</span>
            <span class="form-subnote">Search or Select</span>
          </div>
          <div class="combo-input-wrap">
            <input type="text" id="chatComboInput" class="form-input" list="omniCombosDatalist" placeholder="Search or type combo (e.g. auto/claude/opus)..." value="auto/claude/opus">
          </div>
        </div>

        <!-- Searchable Pipeline Primary Combo -->
        <div class="form-group">
          <div class="form-label">
            <span>🚀 Pipeline Primary Combo (Agents 1-7):</span>
            <span class="form-subnote">Search or Select</span>
          </div>
          <div class="combo-input-wrap">
            <input type="text" id="pipelineComboInput" class="form-input" list="omniCombosDatalist" placeholder="Search or type combo..." value="antigravity/gemini-3.5-flash-low">
          </div>
        </div>

        <!-- Fallback Combo & Target Duration -->
        <div class="form-row">
          <div class="form-group">
            <div class="form-label">Fallback Combo / Model:</div>
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

        <!-- OmniRoute Config & Inspector -->
        <div class="omni-card">
          <div>
            <span style="color:var(--orange-2); font-weight:600;">🔌 OmniRoute Router</span>
            <div style="color:var(--text-dim); font-size:11px;" id="omniStatusText">Checking Docker on :20128...</div>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="omni-btn" id="btnInspectModels">🔍 Inspect 280+ Models</button>
            <a class="omni-btn" href="http://localhost:3000" target="_blank">Setup ↗</a>
          </div>
        </div>

        <!-- Voice Cast Selection -->
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

      <!-- Universal Hardware Box -->
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

      <!-- AI Models & Agent Matrix Box -->
      <div class="models-box" id="modelsBox">
        <div class="models-header">
          <span>🤖 AI Models & Agent Matrix</span>
          <span class="cost-badge" id="matrixCostBadge">$0.00 API Cost</span>
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
          <div class="agent-model-primary">Engine: Content Analyzer Rules</div>
        </div>
        <div class="agent-model-card" id="cardAg4">
          <div class="agent-model-title">
            <span><span class="led-dot" id="ledAg4"></span> Agent 4 · Audio & Music</span>
            <span style="color:var(--green)">$0 Local</span>
          </div>
          <div class="agent-model-primary">TTS: Chatterbox (Voice Clone)</div>
          <div class="agent-model-fallback">Music: Procedural Generator</div>
        </div>
        <div class="agent-model-card" id="cardAg5">
          <div class="agent-model-title">
            <span><span class="led-dot" id="ledAg5"></span> Agent 5 · Audio QA</span>
            <span style="color:var(--blue)">Local</span>
          </div>
          <div class="agent-model-primary">Inspector: Strict VAD & RMS</div>
        </div>
        <div class="agent-model-card" id="cardAg6">
          <div class="agent-model-title">
            <span><span class="led-dot" id="ledAg6"></span> Agent 6 · 4K Image Gen</span>
            <span style="color:var(--green)">$0 Local</span>
          </div>
          <div class="agent-model-primary">Hero: FLUX.1 Schnell</div>
          <div class="agent-model-fallback">Scenes: DreamShaperXL + IP-Adapter</div>
        </div>
        <div class="agent-model-card" id="cardAg7">
          <div class="agent-model-title">
            <span><span class="led-dot" id="ledAg7"></span> Agent 7 · Video Master</span>
            <span style="color:var(--blue)">Local</span>
          </div>
          <div class="agent-model-primary">Muxer: FFmpeg 4K Encoder</div>
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

    <!-- Center Main: Interactive AI Story Architect Chat Section -->
    <div class="screen1-main">
      <div class="panel-chat-hero">
        <div class="panel-title" style="font-size:18px; margin-bottom:12px;">
          <span>💬 Interactive AI Story Architect</span>
          <span class="badge-advisor">Advisor Mode Active</span>
        </div>

        <!-- Big Hero Chat Thread -->
        <div class="chat-thread-container hero-chat" id="chatThread">
          <div class="chat-msg assistant">
            <span class="chat-sender">🤖 AI Story Architect</span>
            <div class="chat-bubble">👋 Hello! Describe your initial video idea or topic below. We can discuss and refine the concept interactively until you're 100% satisfied!</div>
          </div>
        </div>

        <!-- Input Box -->
        <div class="prompt-box-wrap" style="margin-top:16px;">
          <div class="prompt-label">
            <span style="font-size:13px; font-weight:600; color:var(--text);">Discuss or Refine Story Requirement:</span>
            <span class="prompt-hint">↵ Enter to Discuss · Shift+↵ Newline</span>
          </div>
          <textarea id="promptInput" class="prompt-input hero-prompt" placeholder="e.g. I want a story about Chintu finding a magic key in Sundarvan forest. What moral should we add?"></textarea>
        </div>

        <!-- Dual Action Buttons -->
        <div class="action-btn-row hero-actions" style="margin-top:14px;">
          <button id="btnChatSend" class="btn-chat-send">
            💬 Send & Refine Concept
          </button>
          <button id="btnLaunch" class="btn-launch">
            ✅ Approve & Launch Pipeline 🚀
          </button>
        </div>

        <!-- Smart Pre-Analysis Detector -->
        <div class="auto-detector" style="margin-top:16px;">
          <div class="detector-header">
            <span>🧠 Smart Pre-Analysis</span>
            <span id="detectorStatus">Ready</span>
          </div>
          <div class="detector-tags" id="detectorTags">
            <span class="tag">kids_story</span>
            <span class="tag">Hindi</span>
            <span class="tag">mystical_forest</span>
          </div>
        </div>

      </div>
    </div>

  </div>
</div>

<!-- Screen 2: Pipeline Execution & Workspace View -->
<div class="screen-view" id="screen2">

  <!-- Screen 2 Top Bar -->
  <div class="screen2-topbar">
    <button class="btn-back-screen" onclick="showScreen(1)">
      ← Back to Story Chat & Settings
    </button>
    <div style="font-family:var(--display); font-weight:600; font-size:15px; color:var(--orange-2);">
      🚀 Live Pipeline Execution & 7-Agent Workspace
    </div>
  </div>

  <!-- 7-Agent Stepper -->
  <div class="stepper-bar">
    <div class="agent-step" id="step1">
      <div class="step-icon">1</div>
      <div class="step-name">Topic</div>
    </div>
    <div class="agent-step" id="step2">
      <div class="step-icon">2</div>
      <div class="step-name">Script</div>
    </div>
    <div class="agent-step" id="step3">
      <div class="step-icon">3</div>
      <div class="step-name">Config</div>
    </div>
    <div class="agent-step" id="step4">
      <div class="step-icon">4</div>
      <div class="step-name">Audio</div>
    </div>
    <div class="agent-step" id="step5">
      <div class="step-icon">5</div>
      <div class="step-name">QA</div>
    </div>
    <div class="agent-step" id="step6">
      <div class="step-icon">6</div>
      <div class="step-name">Images</div>
    </div>
    <div class="agent-step" id="step7">
      <div class="step-icon">7</div>
      <div class="step-name">Video</div>
    </div>
  </div>

  <!-- Screen 2 Grid: Workspace (Left) + Sidebar (Right) -->
  <div class="screen2-grid">

    <!-- Workspace Column: Terminal + Step Reviews -->
    <div class="panel-workspace">

      <!-- Live Terminal Box -->
      <div class="terminal-box">
        <div class="terminal-header">
          <span>CONSOLE OUTPUT</span>
          <span id="logCounter">0 logs</span>
        </div>
        <div class="terminal-body" id="terminalBody">
          <div class="log-line"><span class="agent-tag">[SYSTEM]</span> Studio Console Ready. Brainstorm in chat or click Approve...</div>
        </div>
      </div>

      <!-- Step Review Tabs -->
      <div class="tabs-header">
        <button class="tab-btn active" data-tab="tab1">📋 Topic Plan</button>
        <button class="tab-btn" data-tab="tab2">✍️ Script Review</button>
        <button class="tab-btn" data-tab="tab3">⚙️ Config</button>
        <button class="tab-btn" data-tab="tab4">🎙️ Audio & QA</button>
        <button class="tab-btn" data-tab="tab5">🖼️ 4K Scene Images</button>
        <button class="tab-btn" data-tab="tab6">🎬 Final Video</button>
      </div>

      <!-- Review Content Cards -->
      <div class="review-card active" id="tab1">
        <h3 style="font-family:var(--display); margin-bottom:12px;">📋 Agent 1: Story Topic Concept</h3>
        <div id="topicContent" style="font-size:14px; line-height:1.7; color:var(--text-dim);">
          <p>No pipeline run started yet. Brainstorm with the AI Advisor and click Approve to generate Agent 1's story concept plan.</p>
        </div>
      </div>

      <div class="review-card" id="tab2">
        <h3 style="font-family:var(--display); margin-bottom:12px;">✍️ Agent 2: Narration Script</h3>
        <div id="scriptContent">
          <p style="color:var(--text-dim);">Generated character dialogues and scene prompts will appear here after Agent 2 completes.</p>
        </div>
      </div>

      <div class="review-card" id="tab3">
        <h3 style="font-family:var(--display); margin-bottom:12px;">⚙️ Agent 3: Story Configuration</h3>
        <pre id="configContent" style="font-family:var(--mono); font-size:13px; color:var(--orange-2); background:var(--bg); padding:16px; border-radius:10px; overflow-x:auto;">{}</pre>
      </div>

      <div class="review-card" id="tab4">
        <h3 style="font-family:var(--display); margin-bottom:12px;">🎙️ Agent 4 & 5: Audio Master & QA Inspection</h3>
        <div class="audio-player-wrap">
          <div style="font-size:14px; font-weight:600;">Master Audio Mix (Chatterbox TTS + Procedural Music + Wind SFX):</div>
          <audio id="audioMasterPlayer" controls></audio>
        </div>
        <div id="qaReportContent" style="font-family:var(--mono); font-size:13px; color:var(--text-dim);">
          <p>Audio QA inspection report will display here after audio generation.</p>
        </div>
      </div>

      <div class="review-card" id="tab5">
        <h3 style="font-family:var(--display); margin-bottom:12px;">🖼️ Agent 6: 4K Scene Images Gallery (Option C)</h3>
        <div class="image-grid" id="imageGrid">
          <p style="color:var(--text-dim);">Generated 4K scene keyframes will render here once Agent 6 completes.</p>
        </div>
      </div>

      <div class="review-card" id="tab6">
        <h3 style="font-family:var(--display); margin-bottom:12px;">🎬 Agent 7: Final Rendered Video</h3>
        <div class="video-player-wrap">
          <video id="videoPlayer" controls poster=""></video>
        </div>
      </div>

    </div>

    <!-- Right Sidebar on Screen 2 (Widgets are moved here when Screen 2 is active) -->
    <div class="screen2-sidebar" id="screen2Sidebar">
    </div>

  </div>

</div>
"""

# Replace studio-container with new 2-screen structure
content = re.sub(r'<div class="studio-container">.*?</div>\s*<!-- Modal Overlay', new_body_structure + '\n\n<!-- Modal Overlay', content, flags=re.DOTALL)

# 4. Add JS showScreen function & update btnLaunch click handler
show_screen_js = """
  // Screen Switcher Function
  function showScreen(num) {
    const s1 = document.getElementById('screen1');
    const s2 = document.getElementById('screen2');
    const nav1 = document.getElementById('navBtnScreen1');
    const nav2 = document.getElementById('navBtnScreen2');
    const sysBox = document.getElementById('sysBox');
    const modelsBox = document.getElementById('modelsBox');
    const s1Sidebar = document.getElementById('screen1Sidebar');
    const s2Sidebar = document.getElementById('screen2Sidebar');

    if(num === 1){
      if(s1) s1.classList.add('active');
      if(s2) s2.classList.remove('active');
      if(nav1) nav1.classList.add('active');
      if(nav2) nav2.classList.remove('active');
      if(s1Sidebar && sysBox && modelsBox){
        s1Sidebar.appendChild(sysBox);
        s1Sidebar.appendChild(modelsBox);
      }
    } else {
      if(s2) s2.classList.add('active');
      if(s1) s1.classList.remove('active');
      if(nav2) nav2.classList.add('active');
      if(nav1) nav1.classList.remove('active');
      if(s2Sidebar && sysBox && modelsBox){
        s2Sidebar.appendChild(sysBox);
        s2Sidebar.appendChild(modelsBox);
      }
    }
  }
"""

if 'function showScreen' not in content:
    content = content.replace('<script>', '<script>\n' + show_screen_js)

# Add showScreen(2) into btnLaunch click listener
if 'btnLaunch.addEventListener' in content and 'showScreen(2)' not in content:
    content = content.replace("btnLaunch.addEventListener('click', () => {", "btnLaunch.addEventListener('click', () => {\n    showScreen(2);")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied 2-screen UI architecture!")
