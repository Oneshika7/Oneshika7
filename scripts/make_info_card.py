import sys

def make_info_card(output_path="info-card.svg"):
    width = 490
    height = 250
    font_size = 14
    line_height = 28
    
    # Content based on user's input
    lines = [
        ("title", "oneshika7@github"),
        ("role", "Software Developer"),
        ("stack", "Python, JavaScript, React, SQL"),
        ("projects", "Animated Profile README"),
        ("contact", "vanshika7320@gmail.com")
    ]
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('<style>')
    svg_lines.append('  .bg { fill: #0d1117; }')
    svg_lines.append('  text { font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 14px; fill: #c9d1d9; }')
    svg_lines.append('  .key { fill: #58a6ff; font-weight: bold; }')
    svg_lines.append('  .title { fill: #3fb950; font-weight: bold; }')
    svg_lines.append('  @keyframes fadein { 0% { opacity: 0; transform: translateX(-10px); } 100% { opacity: 1; transform: translateX(0); } }')
    svg_lines.append('</style>')
    
    svg_lines.append(f'<rect width="{width}" height="{height}" class="bg" rx="10"/>')
    
    y_start = 40
    x_start = 20
    
    for i, (key, value) in enumerate(lines):
        y = y_start + (i * line_height)
        delay = i * 0.2
        
        svg_lines.append(f'<g style="opacity: 0; animation: fadein 0.5s forwards; animation-delay: {delay}s;">')
        if key == "title":
            svg_lines.append(f'  <text x="{x_start}" y="{y}" class="title">{value}</text>')
            svg_lines.append(f'  <text x="{x_start}" y="{y + 10}" class="title">-----------------</text>')
            y_start += 16
        else:
            svg_lines.append(f'  <text x="{x_start}" y="{y}">')
            svg_lines.append(f'    <tspan class="key">{key}</tspan>: {value}')
            svg_lines.append(f'  </text>')
        svg_lines.append('</g>')
        
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Info card SVG saved to {output_path}")

if __name__ == "__main__":
    make_info_card()
