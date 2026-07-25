import re

studio_py_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web_studio.py'
index_html_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web/index.html'

# 1. Update web_studio.py to robustly fetch user combos from all local endpoints
new_omniroute_models_func = """@app.get("/api/omniroute_models")
def get_omniroute_models():
    \"\"\"
    Fetches live user-created Combos directly from OmniRoute (/v1/combos & /api/combos)
    and connected provider models (/v1/models).
    \"\"\"
    user_combos = []
    gemini_combos = []
    seen_ids = set()

    # Try both port 20128 and 3000
    combo_endpoints = [
        "http://localhost:20128/v1/combos",
        "http://localhost:3000/v1/combos",
        "http://localhost:3000/api/combos"
    ]

    for url in combo_endpoints:
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {OMNIROUTE_KEY}"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode())
                    items = data.get("data", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                    for c in items:
                        c_name = c.get("name") if isinstance(c, dict) else str(c)
                        if c_name and c_name not in seen_ids:
                            seen_ids.add(c_name)
                            user_combos.append({"id": c_name, "name": f"Combo: {c_name}", "type": "user_combo"})
        except Exception:
            pass

    # Fetch connected models from /v1/models
    models_endpoints = [
        "http://localhost:20128/v1/models",
        "http://localhost:3000/v1/models"
    ]
    for url in models_endpoints:
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {OMNIROUTE_KEY}"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode())
                    for m in data.get("data", []):
                        m_id = m.get("id", "")
                        if m_id and m_id not in seen_ids:
                            seen_ids.add(m_id)
                            gemini_combos.append({"id": m_id, "name": f"Model: {m_id}", "type": "model"})
        except Exception:
            pass

    return {
        "user_combos": user_combos,
        "gemini_combos": gemini_combos,
        "fallback_freebuff": {"id": "free", "name": "FreeBuff (100% Free Fallback)", "type": "free"},
    }"""

with open(studio_py_path, 'r', encoding='utf-8') as f:
    studio_code = f.read()

# Replace get_omniroute_models function in web_studio.py
studio_code = re.sub(
    r'@app\.get\("/api/omniroute_models"\)\s*def get_omniroute_models\(\):.*?(?=\n@app|\Z)',
    new_omniroute_models_func + '\n\n\n',
    studio_code,
    flags=re.DOTALL
)

with open(studio_py_path, 'w', encoding='utf-8') as f:
    f.write(studio_code)

print("Updated web_studio.py get_omniroute_models endpoint successfully!")
