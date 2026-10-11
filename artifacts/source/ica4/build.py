from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
                                NextPageTemplate, PageBreak, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY

LOGO = "/mnt/user-data/uploads/projects/personasync/branding/assets/logo/personasync-lockup-tm.png"
OUT = "Bowman_ICA4_Sequence_and_State_Machine.pdf"

Body = ParagraphStyle('Body', fontName='Helvetica', fontSize=10.5, leading=14, spaceAfter=6)
H1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=14, leading=18, spaceBefore=8, spaceAfter=4, textColor=colors.black)
Title = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=20, leading=24, spaceAfter=2)
Sub = ParagraphStyle('Sub', fontName='Helvetica', fontSize=11.5, leading=15, textColor=colors.HexColor('#4B5563'), spaceAfter=8)
Cap = ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=10, leading=13, textColor=colors.HexColor('#374151'))
Call = ParagraphStyle('Call', fontName='Helvetica', fontSize=10.5, leading=14)
Bul = ParagraphStyle('Bul', parent=Body, leftIndent=18, bulletIndent=6, spaceAfter=3)
H2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=11, leading=13, spaceBefore=4, spaceAfter=2)
See = ParagraphStyle('See', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#4A3FD1'), spaceBefore=4, spaceAfter=6)

def P(s, st=Body): return Paragraph(s, st)
def callout(label, text):
    t = Table([[Paragraph(f"<b>{label}</b> {text}", Call)]], colWidths=[6.5*inch])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F3F4F6')),
                           ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#D1D5DB')),
                           ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
                           ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7)]))
    return t

doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=1*inch, rightMargin=1*inch, topMargin=0.7*inch, bottomMargin=0.7*inch,
                      title="In-Class Activity 4: Sequence and State Machine Diagrams", author="Artie Bowman")
pw, ph = letter
port = PageTemplate('port', [Frame(1*inch, 0.7*inch, pw-2*inch, ph-1.4*inch, id='f')])
lw, lh = landscape(letter)
land = PageTemplate('land', [Frame(0.5*inch, 0.5*inch, lw-1*inch, lh-1*inch, id='fl')], pagesize=landscape(letter))
doc.addPageTemplates([port, land])

story = []
story.append(P("In-Class Activity 4: Sequence and State Machine Diagrams", Title))
story.append(P("Artie Bowman \u00b7 CIS 641 \u00b7 October 11, 2026", Sub))

story.append(P("Task", H2))
story.append(P("The activity asks for a <b>sequence diagram</b> and a <b>state machine diagram</b> for the term project. Both are behavioral models from Chapter 6. "
               "A sequence diagram shows the order of messages between objects for one use case. A state machine shows the stages one object goes through in its life and what moves it from one stage to the next."))
story.append(P("Project Recap", H2))
story.append(P("My term project is PersonaSync<super><font size='6'>TM</font></super>. In one sentence: the user writes down who they are and what they are working on once, and PersonaSync carries that context into whatever AI tool they open, "
               "so they stop re-explaining themselves. The part I am building this semester is the delivery piece, the client that puts the context into the AI tool. "
               "One rule runs through the whole product: the user writes and confirms everything the system knows about them. Anything an AI guesses is tagged as a suggestion and stays out until the user approves it. Both diagrams show that rule in action."))
story.append(P("What Is Attached", H2))
story.append(P("The class names match the Week 5 CRC cards and class diagram, so the three activities line up. This document has four parts:"))
for n, d in [
    ("Section 1:", "the sequence diagram for the Deliver Context use case, with a short walkthrough (Figure 1)."),
    ("Section 2:", "the state machine for a ContextBlock, the object that carries the confirmation rule (Figure 2)."),
    ("Figures:", "the two diagrams on their own pages, plus Figure 3, the rough sequence diagram I drew by hand in class for a second use case, Create Persona."),
    ("Appendix:", "a template and rules for each diagram type. I am keeping it so the next diagrams for the SRS are faster to make and look the same as these."),
]:
    story.append(Paragraph(f"<b>{n}</b> {d}", Bul, bulletText="\u2022"))
story.append(Spacer(1, 4))

story.append(PageBreak())
story.append(P("1. Sequence Diagram: Deliver Context into an AI Session", H1))
story.append(P("What it shows", H2))
story.append(P("This is the main thing the project does. The user opens an AI tool. The client app notices and offers the persona they usually use there. The user picks one. "
               "The app then collects that persona's context, shapes it to fit the tool, and pastes it in. "
               "At the end it writes a log entry, so the user can always see what was shared and where."))
story.append(P("How to read it", H2))
story.append(P("The boxes across the top are the parts of the system. Time runs down the page. "
               "A solid arrow is one part asking another to do something. A dashed arrow is the answer coming back. "
               "The shaded bar under a box means that part is busy. "
               "The box labeled <i>opt</i> is a step that only happens when the text is too long for the tool. "
               "The log entry box sits lower than the others because it does not exist until that step creates it."))
story.append(P("Where the confirmation rule shows up", H2))
story.append(P("Step 7 only pulls context the user has confirmed, so nothing an AI guessed goes out. "
               "Step 12 writes the log as part of the delivery, so there is never a delivery without a record."))
story.append(KeepTogether([callout("Example:", "I open Claude. The client app offers my \u201cGrad School\u201d persona because that is the one I usually use there. I confirm. "
                     "The app pastes my context into Claude, and the log shows Grad School went to Claude at 6:05 PM."),
    P("See attached diagram, Figure 1 \u2193", See)]))

story.append(PageBreak())
story.append(P("2. Behavioral State Machine: ContextBlock", H1))
story.append(P("What it shows", H2))
story.append(P("A ContextBlock is one fact the user keeps about themselves, like \u201cworking on a master's in AI at GVSU.\u201d "
               "This diagram follows one fact through its life. A fact gets in one of two ways. The user types it, or an AI or a connected tool suggests it. "
               "Either way, the user has to confirm it before it counts. Only confirmed facts ever get sent to an AI tool. The states are:"))
for n, d in [
    ("Draft", "the user is typing or editing it."),
    ("Proposed", "an AI or a connected tool suggested it. The user can see it, but it is not sent anywhere until they keep it."),
    ("Kept", "the user confirmed it. This is the only state that can be sent to a tool."),
    ("Shared", "it has been sent at least once, and the log says where. Taking back the last share moves it back to Kept."),
    ("Archived", "hidden from view but still on record. It can come back, or be deleted after one more confirmation."),
]:
    story.append(Paragraph(f"<b>{n}:</b> {d}", Bul, bulletText="\u2022"))
story.append(Spacer(1, 4))
story.append(P("How to read it", H2))
story.append(P("The filled dot is where a fact starts. The bullseye is where it ends. Each arrow is labeled with what causes the move. "
               "Anything in square brackets is a condition, and in this diagram every condition is the user confirming something."))
story.append(KeepTogether([callout("Example:", "Wispr Flow, a voice note tool, suggests \u201cworking on CIS 641 term project\u201d from a meeting. It sits in Proposed until I keep it. "
                     "Once I keep it, it can go to Claude and becomes Shared. If I take that share back it returns to Kept, not Proposed, because I already confirmed it."),
    P("See attached diagram, Figure 2 \u2193", See)]))

def logo():
    return Image(LOGO, width=1.5*inch, height=1.5*inch*113/640, hAlign='LEFT')

# figure pages
story.append(NextPageTemplate('land'))
story.append(PageBreak())
fw = lw - 1*inch
story.append(logo())
story.append(Spacer(1, 4))
sh1 = 6.0*inch
story.append(Image("seq.png", width=sh1*1500/1100, height=sh1))
story.append(Spacer(1, 6))
story.append(P("Figure 1. Sequence diagram for the Deliver Context use case. Solid arrows are messages, dashed arrows are return values, and the shaded bars show when each object is active. "
               "The ShareLogEntry is drawn where it is created.", Cap))
story.append(PageBreak())
story.append(logo())
story.append(Spacer(1, 4))
sh = 960/1380
sh2 = 6.05*inch
story.append(Image("state.png", width=sh2/sh, height=sh2))
story.append(Spacer(1, 6))
story.append(P("Figure 2. Behavioral state machine for ContextBlock. Kept is the only state that can be delivered. Both entry paths pass through a user confirmation before reaching it.", Cap))
story.append(PageBreak())
story.append(logo())
story.append(Spacer(1, 4))
sh3 = 6.05*inch
story.append(Image("hand_crop.jpg", width=sh3*2750/1960, height=sh3))
story.append(Spacer(1, 6))
story.append(P("Figure 3. Hand-drawn sequence diagram from class for the Create Persona use case (persona library empty). Rough first pass; the activity-period sketch is a draft, so a few labels are shorthand.", Cap))

# appendix (portrait)
Cell = ParagraphStyle('Cell', fontName='Helvetica', fontSize=9, leading=11)
ABody = ParagraphStyle('ABody', parent=Body, fontSize=10, leading=13.5, spaceAfter=6)
CellB = ParagraphStyle('CellB', fontName='Helvetica-Bold', fontSize=9, leading=11)
def legend(rows):
    tb = Table([[P(a, CellB), P(b, Cell)] for a, b in rows], colWidths=[1.6*inch, 4.9*inch])
    tb.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.75,colors.black),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#f3f3f3')),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    return tb
story.append(NextPageTemplate('port'))
story.append(PageBreak())
story.append(P("Appendix: Templates and Rules", H1))
story.append(P("This is the recipe I used for the two diagrams, kept here so I can reuse it for the next ones. It follows the appendix in In-Class Activity 3.", ABody))
story.append(Spacer(1, 4))
story.append(P("A.1 Sequence diagram template", H2))
story.append(P("One use case per diagram. The pieces and what they mean:", ABody))
story.append(legend([
    ("Stick figure", "An actor. The person or outside system that starts the use case. Far left."),
    ("Box, underlined :ClassName", "An object. One per class that takes part, taken from the class diagram."),
    ("Dashed vertical line", "Lifeline. The object exists for as long as the line runs."),
    ("Thin shaded bar", "Execution occurrence. The object is busy during that span."),
    ("Solid arrow, filled head", "Message. One object asking another to do something. Numbered, named like an operation: verb()."),
    ("Dashed arrow, open head", "Return. The answer coming back. Only drawn when the value matters."),
    ("&lt;&lt;create&gt;&gt;", "The message that makes a new object. Its box is drawn at that height, not at the top."),
    ("Box labeled opt, alt, loop", "A fragment. opt runs once if its [condition] is true, alt picks one branch, loop repeats."),
]))
story.append(Spacer(1, 10))
story.append(P("Rules I follow: Time runs down. Put the actor first and the objects in the order they get called, so arrows stay short. "
               "Name each message like an operation from the class diagram. A part that calls itself gets an arrow that loops back to its own line. "
               "Past about fifteen messages, split the use case.", ABody))
story.append(Spacer(1, 8))
story.append(KeepTogether([P("A.2 Behavioral state machine template", H2),
P("One object per diagram. The pieces and what they mean:", ABody),
legend([
    ("Filled dot", "Initial state. Where the object's life starts. One per diagram."),
    ("Rounded box", "A state. Something true of the object for a while. Named with an adjective or past participle: Draft, Kept, Archived."),
    ("Arrow with label", "Transition. The label reads event [guard] / action: the event causes the move, the guard must be true, the action happens on the way."),
    ("Bullseye", "Final state. The object is done. There can be more than one."),
    ("Arrow back to its own box", "Self-transition. The event happens and the object stays where it is."),
])]))
story.append(Spacer(1, 10))
story.append(P("Rules I follow: Every state needs a way in and a way out, except the end states. Put the normal path top to bottom and the exceptions off to the sides. "
               "A condition in brackets is where a person decides something. Draw a two-way move as two parallel lines, not one line with two heads. "
               "Keep lines straight. A curve usually means two boxes are on the wrong side of each other.", ABody))
story.append(Spacer(1, 8))
story.append(KeepTogether([P("A.3 How the files were made", H2), P("Both diagrams are drawn as SVG from Python scripts, so every box and arrow has a set position and edits are text edits. The PDF is built with ReportLab. "
               "The sketch is a photo cropped to the notebook page. The scripts and images live in the course repo next to the SRS.", ABody)]))

doc.build(story)
print("built", OUT)
