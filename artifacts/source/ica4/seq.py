"""Sequence diagram: Deliver context into an AI session (PersonaSync Phase 3).
Hand-laid SVG following Dennis/Wixom/Tegarden conventions."""
import cairosvg

W, H = 1500, 1100
FONT = "Inter, Helvetica, Arial, sans-serif"
INK = "#111827"; GREY = "#6B7280"; LINE = "#9CA3AF"; BOX = "#FFFFFF"; BLUE = "#4A3FD1"

# participants: (key, label, x)
P = [
    ("user", "User", 90),
    ("app", ":ClientApp", 300),
    ("pref", ":ToolPreference", 520),
    ("sync", ":SyncAdapter", 740),
    ("persona", ":Persona", 940),
    ("tool", ":AITool", 1130),
    ("log", ":ShareLogEntry", 1360),
]
X = {k: x for k, _, x in P}
TOP = 60; BOXH = 44; LIFE_TOP = TOP + BOXH + 10

out = []
def t(x, y, s, size=13, anchor="middle", fill=INK, weight=400, italic=False, bg=False):
    if bg:
        w = len(s) * size * 0.56 + 8
        bx = x - 4 if anchor == "start" else (x - w + 4 if anchor == "end" else x - w/2)
        out.append(f'<rect x="{bx}" y="{y-size+1}" width="{w}" height="{size+2}" fill="white"/>')
    st = f"font-family:{FONT};font-size:{size}px;font-weight:{weight};fill:{fill}" + (";font-style:italic" if italic else "")
    out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{st}">{s}</text>')

out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
out.append(f'<rect width="{W}" height="{H}" fill="white"/>')
out.append('<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#111827"/></marker>'
           '<marker id="oarr" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,1 L9,5 L0,9" fill="none" stroke="#111827" stroke-width="1.4"/></marker></defs>')

# title inside figure
t(W/2, 30, "Sequence Diagram: Deliver Context into an AI Session", 17, weight=700)

# participants
for k, label, x in P:
    if k == "user":
        # stick figure actor
        cx, cy = x, TOP + 6
        out.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<line x1="{cx}" y1="{cy+8}" x2="{cx}" y2="{cy+28}" stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<line x1="{cx-14}" y1="{cy+16}" x2="{cx+14}" y2="{cy+16}" stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<line x1="{cx}" y1="{cy+28}" x2="{cx-11}" y2="{cy+44}" stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<line x1="{cx}" y1="{cy+28}" x2="{cx+11}" y2="{cy+44}" stroke="{INK}" stroke-width="1.6"/>')
        t(cx, TOP + 66, "User", 13, weight=600)
    elif k == "log":
        pass  # created later
    else:
        w = 150
        out.append(f'<rect x="{x-w/2}" y="{TOP}" width="{w}" height="{BOXH}" fill="{BOX}" stroke="{INK}" stroke-width="1.4"/>')
        t(x, TOP + 28, label, 14, weight=600)
        out.append(f'<line x1="{x-len(label)*4.2}" y1="{TOP+33}" x2="{x+len(label)*4.2}" y2="{TOP+33}" stroke="{INK}" stroke-width="1"/>')

y = LIFE_TOP + 50
LOG_CREATE_Y = None
msgs = []  # (kind, from, to, label, y)

def msg(frm, to, label, kind="sync", dy=42):
    global y
    msgs.append((kind, frm, to, label, y))
    y += dy

# --- message script ---
msg("user", "app", "1: openAITool()  (e.g., opens Claude)")
msg("app", "app", "2: detectActiveTool()", "self", 52)
msg("app", "pref", "3: suggestPersona(tool)")
msg("pref", "app", "suggested persona", "ret")
msg("app", "user", "4: showPersonaPicker(suggested)")
msg("user", "app", "5: choosePersona(persona)")
msg("app", "sync", "6: deliver(persona, tool)")
msg("sync", "persona", "7: getKeptBlocks(lanes)")
msg("persona", "sync", "confirmed blocks only", "ret")
msg("sync", "tool", "8: getFormat()")
msg("tool", "sync", "prompt format, character limit", "ret")
msg("sync", "sync", "9: render(blocks, format)", "self", 52)
OPT_START = y - 2
y += 30
msg("sync", "sync", "10: trimByPriority(limit)", "self", 44)
OPT_END = y - 2
y += 24
msg("sync", "tool", "11: inject(renderedText)")
msg("tool", "sync", "status", "ret")
LOG_CREATE_Y = y
msg("sync", "log", "12: <<create>> ShareLogEntry(persona, tool, blocks, time)", "create", 50)
msg("sync", "pref", "13: recordUse(persona, tool)")
msg("sync", "app", "delivery status", "ret")
msg("app", "user", "14: notify(“Context delivered to Claude”)")
y += 10
BOTTOM = y

# lifelines
for k, label, x in P:
    y0 = LIFE_TOP if k != "log" else LOG_CREATE_Y + BOXH/2 + 2
    out.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{BOTTOM}" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="6,5"/>')

# activation bars (execution occurrences)
acts = {
    "app":  [(msgs[0][4]-6, msgs[-1][4]+10)],
    "pref": [(msgs[2][4]-6, msgs[3][4]+6), (msgs[16][4]-6, msgs[16][4]+14)],
    "sync": [(msgs[6][4]-6, msgs[17][4]+6)],
    "persona": [(msgs[7][4]-6, msgs[8][4]+6)],
    "tool": [(msgs[9][4]-6, msgs[10][4]+6), (msgs[13][4]-6, msgs[14][4]+6)],
    "log": [(LOG_CREATE_Y + BOXH/2 + 2, LOG_CREATE_Y + BOXH/2 + 30)],
}
for k, spans in acts.items():
    for a, b in spans:
        out.append(f'<rect x="{X[k]-6}" y="{a}" width="12" height="{b-a}" fill="#EEF0FF" stroke="{INK}" stroke-width="1.2"/>')

# opt fragment around trim
fx1, fx2 = X["sync"] - 110, X["tool"] + 10
out.append(f'<rect x="{fx1}" y="{OPT_START}" width="{fx2-fx1}" height="{OPT_END-OPT_START}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
out.append(f'<path d="M{fx1},{OPT_START} h44 v18 l-8,8 h-36 z" fill="#F3F4F6" stroke="{INK}" stroke-width="1.2"/>')
t(fx1 + 22, OPT_START + 14, "opt", 12, weight=700)
t(X["sync"] + 16, OPT_START + 16, "[rendered text > tool character limit]", 12, anchor="start", italic=True)

# created object box
lx = X["log"]; w = 150
out.append(f'<rect x="{lx-w/2}" y="{LOG_CREATE_Y-BOXH/2}" width="{w}" height="{BOXH}" fill="{BOX}" stroke="{INK}" stroke-width="1.4"/>')
t(lx, LOG_CREATE_Y + 6, ":ShareLogEntry", 14, weight=600)
out.append(f'<line x1="{lx-58}" y1="{LOG_CREATE_Y+11}" x2="{lx+58}" y2="{LOG_CREATE_Y+11}" stroke="{INK}" stroke-width="1"/>')

# messages
for kind, frm, to, label, my in msgs:
    x1, x2 = X[frm], X[to]
    if kind == "self":
        out.append(f'<path d="M{x1+6},{my} h40 v26 h-40" fill="none" stroke="{INK}" stroke-width="1.4" marker-end="url(#arr)"/>')
        t(x1 + 52, my + 17, label, 13, anchor="start", bg=True)
        continue
    sx = x1 + (6 if x2 > x1 else -6)
    ex = x2 - (6 if x2 > x1 else -6)
    if kind == "create":
        ex = lx - w/2
    dash = ' stroke-dasharray="7,5"' if kind == "ret" else ""
    marker = "url(#oarr)" if kind == "ret" else "url(#arr)"
    out.append(f'<line x1="{sx}" y1="{my}" x2="{ex}" y2="{my}" stroke="{INK}" stroke-width="1.4"{dash} marker-end="{marker}"/>')
    t(min(sx, ex) + 14, my - 9, label, 13, anchor="start", fill=(GREY if kind == "ret" else INK), italic=(kind == "ret"), bg=True)

# legend
ly = BOTTOM + 18
out.append(f'<line x1="60" y1="{ly}" x2="120" y2="{ly}" stroke="{INK}" stroke-width="1.4" marker-end="url(#arr)"/>')
t(128, ly + 4, "message (operation call)", 12, anchor="start", fill=GREY)
out.append(f'<line x1="330" y1="{ly}" x2="390" y2="{ly}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="7,5" marker-end="url(#oarr)"/>')
t(398, ly + 4, "return value", 12, anchor="start", fill=GREY)
out.append(f'<rect x="520" y="{ly-8}" width="12" height="16" fill="#EEF0FF" stroke="{INK}" stroke-width="1.2"/>')
t(540, ly + 4, "execution occurrence (object is active)", 12, anchor="start", fill=GREY)
t(820, ly + 4, "<<create>> places the new object at the point it is created", 12, anchor="start", fill=GREY)

out.append("</svg>")
svg = "\n".join(out).replace("<<", "&lt;&lt;").replace(">>", "&gt;&gt;").replace("> tool", "&gt; tool")
# undo escaping inside tags: only text nodes used << >> and "> tool"
open("seq.svg", "w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to="seq.png", scale=2)
print("H used", BOTTOM, "of", H)
