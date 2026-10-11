"""Behavioral state machine for ContextBlock — hand-laid SVG, straight/orthogonal transitions."""
import cairosvg, re
W, H = 1380, 960
FONT = "Inter, Helvetica, Arial, sans-serif"; INK = "#111827"; GREY = "#4B5563"
o = []
def t(x, y, s, size=13, anchor="middle", fill=INK, weight=400):
    o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font-family:{FONT};font-size:{size}px;font-weight:{weight};fill:{fill}">{s}</text>')
def state(cx, cy, w, h, name, sub):
    o.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="14" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    o.append(f'<line x1="{cx-w/2}" y1="{cy-h/2+30}" x2="{cx+w/2}" y2="{cy-h/2+30}" stroke="{INK}" stroke-width="1"/>')
    t(cx, cy-h/2+21, name, 15, weight=700)
    for i, l in enumerate(sub.split("|")):
        t(cx, cy-h/2+48+i*16, l, 11.5, fill=GREY)
def arrow(path, label=None, lx=0, ly=0, anchor="middle"):
    o.append(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="1.5" marker-end="url(#arr)"/>')
    if label: t(lx, ly, label, 12.5, anchor=anchor)
def initial(x, y): o.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{INK}"/>')
def final(x, y):
    o.append(f'<circle cx="{x}" cy="{y}" r="12" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{INK}"/>')

o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append(f'<rect width="{W}" height="{H}" fill="white"/>')
o.append('<defs><marker id="arr" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="12" refY="6.5" orient="auto">'
         '<path d="M0,0 L13,6.5 L0,13 z" fill="#111827"/></marker></defs>')
t(W/2, 32, "Behavioral State Machine: ContextBlock", 17, weight=700)

S = 60  # x shift
initial(300+S, 90)
state(300+S, 230, 230, 90, "Draft", "user is writing or editing|the block")
final(630+S, 230)
state(960+S, 230, 320, 90, "Proposed", "suggested by an AI or a connected tool;|tagged as a suggestion; visible, never delivered")
state(630+S, 480, 320, 90, "Kept", "reviewed and confirmed by the user;|the only state that can be delivered")
state(300+S, 740, 320, 90, "Shared", "included in at least one delivery;|a ShareLogEntry exists for it")
state(960+S, 740, 320, 90, "Archived", "hidden from the lane;|kept on record, never delivered")
final(960+S, 920)

def A(path, label, lx, ly, anchor="middle"):
    def sh(m): return f"{float(m.group(1))+S:g},{m.group(2)}"
    arrow(re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", sh, path), label, lx+S, ly, anchor)

# entries
A("M300,99 L300,184", "user adds a block", 312, 145, "start")
A("M309,90 L960,90 L960,184", "AI or connected tool suggests a block / tag as suggestion", 640, 82)
# to final (cancel / discard)
A("M415,230 L617,230", "cancel", 516, 222)
A("M800,230 L643,230", "review: discard", 722, 222)
# Draft <-> Kept (parallel pair)
A("M335,275 L565,435", "save [user confirms] / mark as confirmed", 478, 348, "start")
A("M495,435 L265,275", "edit", 362, 358, "end")
# Proposed -> Kept
A("M930,275 L700,435", "review: keep / clear tag, mark as confirmed", 835, 360, "start")
# Kept <-> Shared (parallel pair)
A("M565,525 L335,695", "deliver to tool / create ShareLogEntry", 500, 585, "start")
A("M265,695 L495,525", "revoke [no active ShareLogEntry remains]", 326, 646, "end")
# Kept <-> Archived (parallel pair)
A("M700,525 L930,695", "archive", 842, 646, "end")
A("M1000,695 L770,525", "restore", 870, 585, "start")
# Shared -> Archived
A("M460,740 L800,740", "archive", 630, 732)
# Shared self-loop
A("M230,785 C200,870 300,870 275,786", "deliver to another tool / add ShareLogEntry", 318, 852, "start")
# Shared -> Draft (edit), orthogonal around the left
A("M140,760 L70,760 L70,250 L184,250", "edit", 60, 500, "end")
# Archived -> final
A("M960,785 L960,907", "delete [user confirms]", 972, 850, "start")

t(60, 940, "Notation: rounded box = state, filled circle = initial state, bullseye = final state. Transition labels read event [guard] / action.", 12, anchor="start", fill=GREY)
o.append("</svg>")
svg = "\n".join(o)
open("state.svg", "w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to="state.png", scale=2)
