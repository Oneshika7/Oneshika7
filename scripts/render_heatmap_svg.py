import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap_svg(input_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    try:
        with open(input_path, "r") as f:
            days = json.load(f)
    except Exception as e:
        print(f"Error loading {input_path}: {e}")
        return
        
    if not days:
        print("No days to render")
        return
        
    cell_size = 11
    cell_spacing = 3
    
    # GitHub shows roughly 53 weeks. Let's calculate based on the data length.
    total_days = len(days)
    weeks = (total_days + 6) // 7
    days_in_week = 7
    
    total_width = (cell_size + cell_spacing) * weeks + 20
    total_height = (cell_size + cell_spacing) * days_in_week + 20
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}">')
    svg_lines.append('<style>')
    svg_lines.append('  rect { rx: 2; ry: 2; }')
    svg_lines.append('  @keyframes slideIn { 0% { opacity: 0; transform: translateY(-10px); } 100% { opacity: 1; transform: translateY(0); } }')
    svg_lines.append('</style>')
    
    for i, day in enumerate(days):
        week = i // days_in_week
        day_of_week = i % days_in_week
        
        x = week * (cell_size + cell_spacing) + 10
        y = day_of_week * (cell_size + cell_spacing) + 10
        
        level = day["level"]
        color = PALETTE[level] if level < len(PALETTE) else PALETTE[-1]
        
        delay = (week + day_of_week) * 0.03
        
        svg_lines.append(f'<g style="opacity: 0; animation: slideIn 0.5s forwards; animation-delay: {delay}s;">')
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" />')
        svg_lines.append('</g>')
        
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Heatmap SVG saved to {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
