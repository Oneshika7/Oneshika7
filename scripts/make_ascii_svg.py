import sys
import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"

def make_ascii_svg(input_path="data/source-prepped.png", output_path="avi-ascii.svg"):
    print(f"Converting {input_path} to ASCII SVG...")
    try:
        img = Image.open(input_path).convert("L")
    except Exception as e:
        print(f"Error loading {input_path}: {e}")
        return
        
    width = 100
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)) * 0.5)
    img = img.resize((width, hsize), Image.Resampling.LANCZOS)
    
    pixels = img.load()
    
    svg_lines = []
    
    font_size = 12
    line_height = 14
    total_height = hsize * line_height
    total_width = width * (font_size * 0.6)
    
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}">')
    svg_lines.append('<style>')
    svg_lines.append('  text { font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; fill: #c9d1d9; white-space: pre; }')
    svg_lines.append('  @keyframes wipe { 0% { clip-path: inset(0 100% 0 0); } 100% { clip-path: inset(0 0 0 0); } }')
    svg_lines.append('</style>')
    
    for y in range(hsize):
        row_str = ""
        for x in range(width):
            brightness = pixels[x, y]
            index = int((255 - brightness) / 255.0 * (len(RAMP) - 1))
            row_str += RAMP[index]
            
        row_str = row_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        
        delay = y * 0.05
        svg_lines.append(f'<g style="animation: wipe 0.5s forwards; animation-delay: {delay}s; clip-path: inset(0 100% 0 0);">')
        svg_lines.append(f'  <text x="0" y="{y * line_height + font_size}">{row_str}</text>')
        svg_lines.append('</g>')
        
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"ASCII SVG saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        make_ascii_svg(sys.argv[1])
    else:
        make_ascii_svg()
