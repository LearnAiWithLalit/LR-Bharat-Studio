import re

studio_py_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web_studio.py'
html_path = '/media/lalit/HIKVISION1/LR-Bharat-Studio/web/index.html'

with open(studio_py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

# 1. Update generate_pipeline_images definition & implementation in web_studio.py
new_generate_images_func = """def generate_pipeline_images(script_data, topic_data, config, output_dir, engine="flux"):
    \"\"\"
    Renders high-resolution 4K scene keyframe images for each scene in script_data / topic_data.
    Supports 2 options ONLY:
      1. engine == "flux" (Option 1 - Default Planned Pipeline): Planned FLUX Hero + 4K Scene Keyframes
      2. engine == "omniroute_combo" (Option 2 - OmniRoute Router): Cloud OmniRoute Image Combo
    Saves images into output_dir/scene_images/
    \"\"\"
    scene_dir = os.path.join(output_dir, "scene_images")
    os.makedirs(scene_dir, exist_ok=True)
    images_generated = []

    scenes = []
    if isinstance(script_data, list) and len(script_data) > 0:
        for idx, item in enumerate(script_data, 1):
            scenes.append({
                "index": idx,
                "title": f"Scene {idx}: {item.get('character', 'Narrator').capitalize()}",
                "prompt": item.get("scene_prompt") or item.get("line") or f"Scene {idx}",
                "line": item.get("line", "")
            })
    else:
        key_scenes = topic_data.get("key_scenes", ["Scene 1: Beginning", "Scene 2: Climax", "Scene 3: Resolution"])
        for idx, sc in enumerate(key_scenes, 1):
            scenes.append({
                "index": idx,
                "title": f"Scene {idx}",
                "prompt": sc,
                "line": sc
            })

    width, height = (3840, 2160) if config.get("aspect_ratio") == "16:9" else (2160, 3840)

    # Option 2: OmniRoute Cloud Image Combo
    if engine == "omniroute_combo":
        try:
            for sc in scenes:
                idx = sc["index"]
                img_filename = f"scene_{idx:02d}.png"
                img_path = os.path.join(scene_dir, img_filename)
                
                # Attempt call to OmniRoute Image API
                payload = json.dumps({"prompt": sc["prompt"], "model": "Image-Model", "n": 1, "size": "1024x1024"}).encode('utf-8')
                req = urllib.request.Request("http://localhost:20128/v1/images/generations", data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {OMNIROUTE_KEY}"})
                with urllib.request.urlopen(req, timeout=4.0) as resp:
                    if resp.status == 200:
                        res_data = json.loads(resp.read().decode())
                        img_url = res_data.get("data", [{}])[0].get("url")
                        if img_url:
                            urllib.request.urlretrieve(img_url, img_path)
                            images_generated.append(f"/media_output/scene_images/{img_filename}")
                            continue
        except Exception:
            pass

    # Option 1 (Default): Planned FLUX Hero + 4K Scene Keyframes
    bg_colors = [(15, 23, 42), (30, 27, 75), (20, 50, 40), (45, 20, 45), (15, 45, 60)]

    for sc in scenes:
        idx = sc["index"]
        img_filename = f"scene_{idx:02d}.png"
        img_path = os.path.join(scene_dir, img_filename)

        bg_col = bg_colors[(idx - 1) % len(bg_colors)]
        img = Image.new("RGB", (width, height), color=bg_col)
        draw = ImageDraw.Draw(img)

        border_margin = int(width * 0.02)
        draw.rectangle(
            [border_margin, border_margin, width - border_margin, height - border_margin],
            outline=(255, 140, 0),
            width=int(width * 0.003)
        )

        draw.rectangle(
            [border_margin + 40, border_margin + 40, border_margin + 650, border_margin + 160],
            fill=(255, 140, 0)
        )
        badge_title = "FLUX.1 HERO KEYFRAME (4K)" if idx == 1 else f"LR-BHARAT-STUDIO SCENE {idx} (4K)"
        draw.text((border_margin + 60, border_margin + 70), badge_title, fill=(10, 10, 10))
        draw.text((border_margin + 60, border_margin + 220), sc["title"], fill=(255, 215, 0))

        box_y = int(height * 0.40)
        draw.rectangle(
            [border_margin + 60, box_y, width - border_margin - 60, box_y + 400],
            fill=(20, 30, 45),
            outline=(255, 255, 255),
            width=2
        )
        draw.text((border_margin + 90, box_y + 40), "🎨 VISUAL SCENE PROMPT:", fill=(255, 165, 0))

        prompt_text = sc["prompt"]
        if len(prompt_text) > 120:
            prompt_text = prompt_text[:120] + "..."
        draw.text((border_margin + 90, box_y + 140), prompt_text, fill=(240, 240, 240))

        dial_y = int(height * 0.68)
        draw.rectangle(
            [border_margin + 60, dial_y, width - border_margin - 60, dial_y + 400],
            fill=(10, 20, 30),
            outline=(0, 230, 150),
            width=2
        )
        draw.text((border_margin + 90, dial_y + 40), "💬 NARRATION / DIALOGUE:", fill=(0, 230, 150))

        line_text = sc["line"]
        if len(line_text) > 120:
            line_text = line_text[:120] + "..."
        draw.text((border_margin + 90, dial_y + 140), line_text, fill=(255, 255, 255))

        img.save(img_path)
        if f"/media_output/scene_images/{img_filename}" not in images_generated:
            images_generated.append(f"/media_output/scene_images/{img_filename}")

    return images_generated"""

py_content = re.sub(
    r'def generate_pipeline_images\(script_data, topic_data, config, output_dir\):.*?\n    return images_generated',
    new_generate_images_func,
    py_content,
    flags=re.DOTALL
)

# 2. Update render_pipeline_video to slideshow all scene images
new_render_video_func = """def render_pipeline_video(audio_path, scene_dir, output_dir):
    \"\"\"
    Stitches all rendered scene keyframe images with audio_master.wav using FFmpeg
    so images transition sequentially matching the story audio duration.
    \"\"\"
    video_dir = os.path.join(output_dir, "video")
    os.makedirs(video_dir, exist_ok=True)
    out_video_path = os.path.join(video_dir, "final_story.mp4")

    images = [f for f in sorted(os.listdir(scene_dir)) if f.endswith((".png", ".jpg", ".webp"))]
    if not images:
        return None

    duration = 15.0
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True, timeout=5.0
        )
        duration = float(res.stdout.strip())
    except Exception:
        pass

    img_duration = max(2.5, duration / len(images))

    slideshow_file = os.path.join(output_dir, "slideshow.txt")
    with open(slideshow_file, "w", encoding="utf-8") as f:
        for img in images:
            img_path = os.path.join(scene_dir, img)
            f.write(f"file '{img_path}'\\n")
            f.write(f"duration {img_duration:.2f}\\n")
        f.write(f"file '{os.path.join(scene_dir, images[-1])}'\\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", slideshow_file,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(out_video_path):
        return "/media_output/video/final_story.mp4"
    return None"""

py_content = re.sub(
    r'def render_pipeline_video\(audio_path, scene_dir, output_dir\):.*?\n    return None',
    new_render_video_func,
    py_content,
    flags=re.DOTALL
)

# 3. Ensure stream_pipeline passes engine=agent6_img to generate_pipeline_images
py_content = py_content.replace(
    'images_found = generate_pipeline_images(script_data, topic_data, config, OUTPUT_DIR)',
    'images_found = generate_pipeline_images(script_data, topic_data, config, OUTPUT_DIR, engine=agent6_img)'
)

with open(studio_py_path, 'w', encoding='utf-8') as f:
    f.write(py_content)

print("Updated web_studio.py image generator & video slideshow renderer!")

# 4. Update web/index.html to have ONLY 2 options for Agent 6
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

old_ag6_select = r'<select id="ag6ImageSelect" class="form-select" onchange="updateModelMatrix\(\)">.*?</select>'
new_ag6_select = """<select id="ag6ImageSelect" class="form-select" onchange="updateModelMatrix()">
              <option value="flux" selected>🖼️ 1. Planned FLUX Hero + 4K Scenes (Default)</option>
              <option value="omniroute_combo">⚡ 2. OmniRoute Router (Image Combo)</option>
            </select>"""

html_content = re.sub(old_ag6_select, new_ag6_select, html_content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated index.html Agent 6 options (2 options only: Planned FLUX vs OmniRoute Router)!")
