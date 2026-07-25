import re

html_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML dropdown elements in Screen 1
old_chat_combo_block = r'<!-- Searchable Chat Advisor Combo -->.*?</div>\s*</div>'
new_chat_combo_block = """<!-- OmniRoute Dashboard Combos (Chat Advisor) -->
        <div class="form-group">
          <div class="form-label">
            <span>💬 Chat Advisor Combo:</span>
            <span class="form-subnote" id="chatComboCountTag">OmniRoute Combos</span>
          </div>
          <div class="combo-input-wrap">
            <select id="chatComboSelect" class="form-select" onchange="handleComboChange('chat')">
              <option value="auto/claude/opus" selected>Loading dashboard combos...</option>
            </select>
            <input type="text" id="chatComboInput" class="form-input" style="display:none; margin-top:6px;" placeholder="Type custom combo (e.g. my-custom-combo)...">
          </div>
        </div>"""

old_pipeline_combo_block = r'<!-- Searchable Pipeline Primary Combo -->.*?</div>\s*</div>'
new_pipeline_combo_block = """<!-- OmniRoute Dashboard Combos (Pipeline Primary) -->
        <div class="form-group">
          <div class="form-label">
            <span>🚀 Pipeline Primary Combo (Agents 1-7):</span>
            <span class="form-subnote" id="pipelineComboCountTag">OmniRoute Combos</span>
          </div>
          <div class="combo-input-wrap">
            <select id="pipelineComboSelect" class="form-select" onchange="handleComboChange('pipeline')">
              <option value="antigravity/gemini-3.5-flash-low" selected>Loading dashboard combos...</option>
            </select>
            <input type="text" id="pipelineComboInput" class="form-input" style="display:none; margin-top:6px;" placeholder="Type custom combo (e.g. my-custom-combo)...">
          </div>
        </div>"""

content = re.sub(old_chat_combo_block, new_chat_combo_block, content, flags=re.DOTALL)
content = re.sub(old_pipeline_combo_block, new_pipeline_combo_block, content, flags=re.DOTALL)

# 2. Add helper JS functions handleComboChange and getComboValue
combo_helper_js = """
  // Combo Select Helpers
  function handleComboChange(type){
    const select = document.getElementById(type === 'chat' ? 'chatComboSelect' : 'pipelineComboSelect');
    const input = document.getElementById(type === 'chat' ? 'chatComboInput' : 'pipelineComboInput');
    if(select.value === 'custom'){
      input.style.display = 'block';
      input.focus();
    } else {
      input.style.display = 'none';
      input.value = select.value;
    }
    updateModelMatrix();
  }

  function getComboValue(type){
    const select = document.getElementById(type === 'chat' ? 'chatComboSelect' : 'pipelineComboSelect');
    const input = document.getElementById(type === 'chat' ? 'chatComboInput' : 'pipelineComboInput');
    if(!select) return input ? input.value : '';
    if(select.value === 'custom'){
      return input.value.trim() || select.value;
    }
    return select.value;
  }
"""

if 'function handleComboChange' not in content:
    content = content.replace('<script>', '<script>\n' + combo_helper_js)

# 3. Update fetchOmniRouteCombos function in JS
new_fetch_combos_func = """  async function fetchOmniRouteCombos(){
    try {
      const res = await fetch('/api/omniroute_models');
      const d = await res.json();
      
      const chatSelect = document.getElementById('chatComboSelect');
      const pipelineSelect = document.getElementById('pipelineComboSelect');
      const chatInput = document.getElementById('chatComboInput');
      const pipelineInput = document.getElementById('pipelineComboInput');

      let userCombosHtml = '<optgroup label="👑 Your OmniRoute Dashboard Combos">';
      let firstLiveCombo = null;

      if(d.user_combos && d.user_combos.length > 0){
        firstLiveCombo = d.user_combos[0].id;
        d.user_combos.forEach(c => {
          userCombosHtml += `<option value="${c.id}">${c.id}</option>`;
        });
      } else {
        userCombosHtml += `<option value="" disabled>No custom combos found</option>`;
      }
      userCombosHtml += '</optgroup>';

      let providerModelsHtml = '<optgroup label="⚡ Provider Models & Defaults">';
      providerModelsHtml += `<option value="auto/claude/opus">auto/claude/opus</option>`;
      providerModelsHtml += `<option value="auto/claude">auto/claude</option>`;
      if(d.gemini_combos && d.gemini_combos.length > 0){
        d.gemini_combos.forEach(c => {
          providerModelsHtml += `<option value="${c.id}">${c.id}</option>`;
        });
      }
      providerModelsHtml += `<option value="free">FreeBuff (100% Free)</option>`;
      providerModelsHtml += '</optgroup>';

      let customHtml = '<optgroup label="✏️ Custom"><option value="custom">✏️ Type Custom Combo...</option></optgroup>';

      const fullHtml = userCombosHtml + providerModelsHtml + customHtml;

      if(chatSelect) chatSelect.innerHTML = fullHtml;
      if(pipelineSelect) pipelineSelect.innerHTML = fullHtml;

      // Auto-select first genuine live combo if available
      if(firstLiveCombo){
        if(pipelineSelect) pipelineSelect.value = firstLiveCombo;
        if(chatSelect) chatSelect.value = firstLiveCombo;
        if(chatInput) chatInput.value = firstLiveCombo;
        if(pipelineInput) pipelineInput.value = firstLiveCombo;
      }

      updateModelMatrix();

      // Update right column matrix combos list
      const combosList = document.getElementById('combosList');
      if(combosList && d.user_combos && d.user_combos.length > 0){
        let itemsHtml = '';
        d.user_combos.forEach(c => {
          itemsHtml += `<div class="combo-item"><span>${c.id}</span><span class="badge-free">OmniRoute Dashboard</span></div>`;
        });
        combosList.innerHTML = itemsHtml;
      }
    } catch (e) {
      console.warn("Could not fetch OmniRoute combos:", e);
    }
  }"""

content = re.sub(
    r'async function fetchOmniRouteCombos\(\)\{.*?\n  \}',
    new_fetch_combos_func,
    content,
    flags=re.DOTALL
)

# 4. Update updateModelMatrix to use getComboValue
content = content.replace("chatComboInput.value.trim()", "getComboValue('chat')")
content = content.replace("pipelineComboInput.value.trim()", "getComboValue('pipeline')")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html dropdown select elements successfully!")
