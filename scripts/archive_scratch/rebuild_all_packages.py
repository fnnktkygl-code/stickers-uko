import os
import zipfile
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWN_DIR = f"{BASE_DIR}/downloads"
MASCOTS_DIR = f"{BASE_DIR}/mascots"

os.makedirs(DOWN_DIR, exist_ok=True)

mascots = [
    {"key": "aituko", "name": "AItuko", "dir": f"{BASE_DIR}/assets"},
    {"key": "owluko", "name": "Owluko", "dir": f"{MASCOTS_DIR}/owluko/assets"},
    {"key": "luneko", "name": "Luneko", "dir": f"{MASCOTS_DIR}/luneko/assets"},
    {"key": "hatoko", "name": "Hatoko", "dir": f"{MASCOTS_DIR}/hatoko/assets"},
    {"key": "usako", "name": "Usako", "dir": f"{MASCOTS_DIR}/usako/assets"},
    {"key": "inuko", "name": "Inuko", "dir": f"{MASCOTS_DIR}/inuko/assets"},
]

def make_tsx_component(mascot_name, mascot_key):
    return f"""import React from 'react';

export type {mascot_name}State = 
  | '01_waving'
  | '02_celebrating'
  | '03_ai_thinking'
  | '04_error_404'
  | '05_thumbs_up'
  | '06_sleeping'
  | '07_pointing'
  | '08_searching'
  | '09_loading'
  | '10_idea'
  | '11_security'
  | '12_goodbye';

interface {mascot_name}Props {{
  state?: {mascot_name}State;
  format?: 'webp' | 'gif' | 'png';
  size?: number;
  className?: string;
  alt?: string;
}}

export const {mascot_name}: React.FC<{mascot_name}Props> = ({{
  state = '01_waving',
  format = 'webp',
  size = 256,
  className = '',
  alt = '{mascot_name} 3D Mascot'
}}) => {{
  const filename = format === 'png' ? 'static.png' : `animated.${{format}}`;
  const src = `/assets/{mascot_key}/${{state}}/${{filename}}`;
  return (
    <div 
      className={{`relative inline-flex items-center justify-center ${{className}}`}}
      style={{{{ width: size, height: size }}}}
    >
      <img
        src={{src}}
        alt={{alt}}
        width={{size}}
        height={{size}}
        className="w-full h-full object-contain select-none"
        loading="lazy"
        decoding="async"
      />
    </div>
  );
}};

export default {mascot_name};
"""

all_12 = [
    '01_waving', '02_celebrating', '03_ai_thinking', '04_error_404',
    '05_thumbs_up', '06_sleeping', '07_pointing', '08_searching',
    '09_loading', '10_idea', '11_security', '12_goodbye'
]

starter_6 = [
    '01_waving', '02_celebrating', '03_ai_thinking',
    '04_error_404', '05_thumbs_up', '06_sleeping'
]

for m in mascots:
    m_key = m["key"]
    m_name = m["name"]
    assets_dir = m["dir"]
    
    print(f"📦 Packaging ZIPs for {m_name} ({m_key})...")
    
    # 1. Free Sample (01_waving)
    for free_name in [f"{m_name}-Free-Sample.zip", "Uko-Free-Sample.zip" if m_key == "aituko" else None]:
        if not free_name: continue
        free_zip = f"{DOWN_DIR}/{free_name}"
        with zipfile.ZipFile(free_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            waving_files = glob.glob(f"{assets_dir}/01_waving/*")
            for f in sorted(waving_files):
                if f.endswith(".webp") or f.endswith(".gif") or f.endswith(".png"):
                    zf.write(f, arcname=f"01_waving/{os.path.basename(f)}")
            zf.writestr(f"components/{m_name}.tsx", make_tsx_component(m_name, m_key))
            zf.writestr("README.md", f"# {m_name} 3D Free Sample\n\n- State: 01_waving\n- Formats: WebP (60fps transparent), APNG, GIF, PNG static (512x512)\n- License: Commercial Uko UI")
    
    # 2. Starter Pack (6 States or Starter Pack)
    for start_name in [f"{m_name}-Starter-6-States.zip", f"{m_name}-Starter-Pack.zip", "Uko-Starter-6-States.zip" if m_key == "aituko" else None]:
        if not start_name: continue
        starter_zip = f"{DOWN_DIR}/{start_name}"
        with zipfile.ZipFile(starter_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for state in starter_6:
                state_files = glob.glob(f"{assets_dir}/{state}/*")
                for f in sorted(state_files):
                    if f.endswith(".webp") or f.endswith(".gif") or f.endswith(".png"):
                        zf.write(f, arcname=f"{state}/{os.path.basename(f)}")
            zf.writestr(f"components/{m_name}.tsx", make_tsx_component(m_name, m_key))
            zf.writestr("README.md", f"# {m_name} 3D Starter Pack\n\n- 6 Core States: {', '.join(starter_6)}\n- Formats: WebP (60fps transparent), APNG, GIF, PNG static (512x512)\n- License: Commercial Uko UI")
    
    # 3. Pro Pack (All 12 states)
    for pro_name in [f"{m_name}-Pro-12-States.zip", "Uko-Pro-12-States.zip" if m_key == "aituko" else None]:
        if not pro_name: continue
        pro_zip = f"{DOWN_DIR}/{pro_name}"
        with zipfile.ZipFile(pro_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for state in all_12:
                state_files = glob.glob(f"{assets_dir}/{state}/*")
                for f in sorted(state_files):
                    if f.endswith(".webp") or f.endswith(".gif") or f.endswith(".png"):
                        zf.write(f, arcname=f"{state}/{os.path.basename(f)}")
            zf.writestr(f"components/{m_name}.tsx", make_tsx_component(m_name, m_key))
            zf.writestr("README.md", f"# {m_name} 3D Pro Pack (12 States)\n\n- 12 Universal States\n- Formats: WebP (60fps transparent), APNG, GIF, PNG static (512x512)\n- License: Commercial Uko UI")

print("\n🎉 ALL PACKAGES SUCCESSFULLY REBUILT IN /downloads!")
