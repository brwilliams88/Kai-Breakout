#!/usr/bin/env python3
"""Generate the Kai Breakout revision history PDF.

Each version corresponds to a substantive prompt-driven update. Numbering
aligns with the CACHE_VERSION in sw.js (currently v10).  Add new rows to the
top of `VERSIONS` and re-run this script after each push.

Run:  python3 generate_revision_history.py
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ---- Data: newest at the top, oldest at the bottom ----
VERSIONS = [
    {
        "version": "v12",
        "date":    "May 25, 2026",
        "summary": (
            "Akhil ball SLOWER (9.3 → 7.6) — constant homing made the v11.1 "
            "ball feel faster than older versions; this restores the old "
            "perceived pace. "
            "Akhil collision priority FIXED: damage non-steel bricks first, "
            "skip the steel check if we damaged one this tick — kills the "
            "'steel clang sound + brick not breaking' oscillation between "
            "adjacent steel + tough bricks. "
            "Akhil-steel angle randomization: ±20° rotation on each steel "
            "hit so the ball doesn't bounce back-and-forth into the same "
            "steel from the same angle. "
            "Mode HUD pill shifted up (y 36 → 22 when no boss) so the "
            "bottom edge no longer touches the top brick row. "
            "Boss music transitions FIXED: when Big G dies with a mode "
            "active, that mode's music starts back up (was leaving silence); "
            "no-mode case still restores chill. "
            "Big G hit 'ghost image' artifact REMOVED — was the random "
            "flinch-teleport flashing her at a different position for one "
            "frame before figure-8 update snapped her back. Now she stays "
            "on the figure-8 path; sparks + hit sprite + screen shake carry "
            "all the impact. "
            "Revived TOUGH bricks now also use the purple cursed palette + "
            "pulsing border + sparkles (was showing original color tint). "
            "BIG G HAS ARRIVED! purple stroked banner during the intro "
            "state — fade-in/hold/fade-out, gentle scale pulse. Ball is "
            "fully frozen during the boss intro so the player can't lose "
            "during the entrance cinematic. "
            "On level 7 she now waits to spawn until the ball is launched "
            "(carryover from round-2 polish, calling it out explicitly). "
            "sw.js CACHE_VERSION bumped to v12 — required to invalidate "
            "stale service-worker caches on already-installed clients."
        ),
    },
    {
        "version": "v11",
        "date":    "May 24-25, 2026",
        "summary": (
            "BIG G BOSS FIGHT (Akhil's mom Geetanjali). 15 HP, 3 phases, "
            "revives bricks, fires purple orbs at paddle (phase 2+). "
            "Auto-spawns level 7 + manual '0' / 5s logo long-press. "
            "Akhil-meets-mom reaction: ball grows + 'Mom?!' bubble. "
            "Akhil+steel redesigned with per-session blocklist + force-"
            "redirect on repeat hits + 3-strike teleport failsafe. "
            "Polish pass: HP bar in top band (y=8-32, never overlaps "
            "bricks), 'BIG G' label pixel-stroked, ouch shake on hit "
            "(frozen while paused). Mode HUDs shift down to y=60 with "
            "dark pill background when boss is active. "
            "Sprite 20% bigger (face readable on phone). Constant purple "
            "shadowBlur halo. Removed source-atop white-square artifact; "
            "now 14-particle purple energy burst + 4 trailing sparks + "
            "brightness boost via ctx.filter. "
            "Elaborate entrance portal: rotating gradient void + 5 thick "
            "rings + 8 crackling lightning bolts + edge vignette + drop-in "
            "from above + overshoot. Get-ready audio beat before sting. "
            "Revived bricks clearly CURSED: purple gradient base, pulsing "
            "border with glow, rune hatches, drifting sparkles. Ghost-to-"
            "solid: 18-spark burst + twinkle SFX + 10-frame scale bounce. "
            "Cast visible: crackling wand beam to ghost brick + 16 bright "
            "sparkles drifting along. "
            "Boss music PRIORITY: chill + mode music silenced when boss "
            "active; gameplay still works. Chill restored on death. "
            "Paddle stun bumped to 1.2s, blocks key/touch/MOUSE motion, "
            "no fillRect overlay (was creating PAPA-paddle purple block "
            "artifact). 'Tink' SFX on invuln hits. Phase-shift sting + "
            "purple flash at 66% / 33% HP. "
            "Boss death: +50 per revived brick (staggered popups) + flat "
            "+1000 BOSS BONUS. No revival while ball is stuck on paddle. "
            "Cinematic state cleared on level transition (no banner bleed). "
            "Pause disabled during cinematic. Items + manual summon "
            "blocked during 1.75s boss intro. "
            "Round-2 polish: Big G now waits to spawn on level 7 until "
            "the player launches the ball (no longer fires 600ms after the "
            "intro card). Boss collision rewritten with MIN-OVERLAP "
            "resolution — fixes 'ball teleports up through bricks' when "
            "boss slid into ball (old directional nudge pushed ball into "
            "brick row). Akhil-vs-steel logic SIMPLIFIED: no more "
            "blocklist / repeat-hit counter / failsafe teleport — on "
            "steel hit, min-overlap nudge ball out + brief 10-tick drift + "
            "re-pick target preferring one whose line doesn't cross the "
            "just-hit steel. No more stuck-on-same-steel loops or "
            "teleports. Mode HUD pill background now ALWAYS shown "
            "(consistent with-or-without boss). BIG G label bumped to 18px "
            "and moved to the LEFT of the bar (was small 12px above). "
            "BLOCKING FIX (pre-push): setupBigGSummon IIFE referenced "
            "logoEl before its const declaration — TDZ ReferenceError "
            "crashed the script at load. Converted to a named function "
            "called after logoEl is initialized."
        ),
    },
    {
        "version": "v10",
        "date":    "May 19, 2026",
        "summary": (
            "Akhil ball: stronger anti-stall (3-strike escalating recovery, "
            "failsafe teleport to open sky after ~1.5s stuck). "
            "Title footer: JS-driven wrap detection — bullet only shows when "
            "ARR is inline with the rest. "
            "High-score flash auto-dismisses when level-complete or endgame "
            "popups open (no overlap). "
            "Commit title now carries the version number."
        ),
    },
    {
        "version": "v9",
        "date":    "May 19, 2026",
        "summary": (
            "Akhil unstuck: line-of-sight target selection through steel + "
            "stagnation watchdog. "
            "Title footer one-line when room, two-line with no leading dot when "
            "narrow; matched inline-dot spacing. "
            "New-high flash moved to mid-canvas (below bricks). "
            "Paddle hit SFX louder. "
            "GAME OVER keeps red title even on new high — added gold pulsing "
            "'NEW HIGH SCORE!' badge instead. "
            "Reset-hi-score confirmation modal +30%."
        ),
    },
    {
        "version": "v8",
        "date":    "May 18, 2026",
        "summary": (
            "Akhil mode: +15% homing speed, -30% bounce distance, steering "
            "forces curve the ball around steel bricks. "
            "MAD MAMA explosions: screen-shake with chain-count scaling. "
            "PWA: service worker (sw.js) for offline play and instant cache "
            "loads. "
            "Per-level intro card (LEVEL N fade in/out, ~1.3s). "
            "Paddle hit SFX (woody 'thock'). "
            "High-score break flash (gold banner + stat-box pulse). "
            "Hold-the-HI-SCORE-5s to open reset confirmation modal. "
            "Touch paddle: id-tracked drag (immune to logo taps) + distance-"
            "scaled speed. "
            "'BRICKS SCORE' label on level complete. "
            "Combo callout enlarged (only at x2/x3 thresholds). "
            "SuperKai item: bigger, papa-style green glow. "
            "Item-spawn 60s timer freezes while ball is on paddle."
        ),
    },
    {
        "version": "v7",
        "date":    "May 18, 2026",
        "summary": (
            "Win screen: CONGRATULATIONS! card now sits in front of the "
            "firework bursts (z-index fix). "
            "Level-complete popup: larger BRICKS/BONUS/TIME/TOTAL text, +25% "
            "longer count animation, denser tick blips. "
            "Paddle control area extended below the canvas (X bounded by "
            "canvas edges). "
            "All inputs locked while paused or pre-launch. "
            "Falling items +15% speed. "
            "Logo tap cycle wraps past 5 (no auto-Nozomi at exact 5). "
            "iPhone title screen: portrait copyright no longer clipped, "
            "landscape logo bumped and footer no longer crashes the START "
            "button."
        ),
    },
    {
        "version": "v6",
        "date":    "May 18, 2026",
        "summary": (
            "Logo activation feedback split: small 'tap' pulse on each touch, "
            "bigger 'fire' pulse + dah-ding chime when an item commits. "
            "Title screen: BRICKS · BALLS · POWERUPS forced to one line; "
            "copyright '© 2026 · A PAPA & KAI PRODUCTION' stays paired; phone-"
            "landscape logo bumped to 70vh. "
            "Bigger PAUSED canvas text and 'PRESS SPACE OR CLICK TO LAUNCH' "
            "wording on one line. "
            "Webapp icon updated (transparent border trimmed) and switched to "
            "apple-touch-icon-precomposed."
        ),
    },
    {
        "version": "v5",
        "date":    "May 18, 2026",
        "summary": (
            "Pause button (top-right canvas corner) wired across mouse, "
            "keyboard, and touch. "
            "Procedural level-clear and game-win jingles. Score-counter tick "
            "sounds during number rolls. "
            "+10% launch ball speed. Title screen now works in portrait. "
            "Separate orientation prompts: phone-rotate vs. desktop widen-"
            "window. iPad-mini standalone cutoff fixed. "
            "apple-touch-icon uses webapp icon.png. "
            "Sidebar logo can be tapped 1-5 times to spawn power-ups (touch-"
            "testing aid). "
            "Bottom hint strip removed."
        ),
    },
    {
        "version": "v4",
        "date":    "May 17–18, 2026",
        "summary": (
            "Brick hit SFX restored in SuperKai (extras) and Nozomi modes. "
            "Level-complete jingle longer / more celebratory with a pause "
            "before the score-counter starts. Win jingle expanded to ~4s "
            "with sub-bass and cymbal swell. "
            "Akhil mode: +25% homing speed, ball-velocity restore on mode end "
            "now uses the current level's speed (no more 'feels like level 1')."
        ),
    },
    {
        "version": "v3",
        "date":    "May 17, 2026",
        "summary": (
            "PAPA mode (custom paddle skin) and AKHIL mode (homing yellow "
            "ball) added. "
            "7-level progression with tough (2-hp) and steel (indestructible) "
            "bricks. "
            "GitHub Pages deployment so the game is playable at a public URL."
        ),
    },
    {
        "version": "v2",
        "date":    "May 15–16, 2026",
        "summary": (
            "Nozomi mode (snake paddle, pass-through ball). MAD MAMA "
            "explosion mode (radius destroys neighbors). SuperKai multi-ball "
            "mode. Per-mode music, full power-up item system (heart, bomb, "
            "superKai, papa, akhil)."
        ),
    },
    {
        "version": "v1",
        "date":    "May 13–14, 2026",
        "summary": (
            "Initial Kai Breakout build: HTML5 canvas, kaiball-as-ball, "
            "paddle, multi-row brick wall, lives + score, basic combo "
            "multiplier, retro arcade visual style."
        ),
    },
]


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "TitleBig",
        parent=styles["Title"],
        fontSize=26,
        spaceAfter=4,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0a3a72"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444"),
        spaceAfter=18,
    )
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
    )
    version_cell_style = ParagraphStyle(
        "VersionCell",
        parent=styles["BodyText"],
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0a3a72"),
        fontName="Helvetica-Bold",
    )
    date_cell_style = ParagraphStyle(
        "DateCell",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#333"),
    )

    story = []
    story.append(Paragraph("Kai Breakout", title_style))
    story.append(Paragraph("Revision History · newest at top", subtitle_style))

    # Build the table data with Paragraph cells so text wraps.
    header = [
        Paragraph("<b>Version</b>", cell_style),
        Paragraph("<b>Date</b>", cell_style),
        Paragraph("<b>Summary</b>", cell_style),
    ]
    rows = [header]
    for v in VERSIONS:
        rows.append([
            Paragraph(v["version"], version_cell_style),
            Paragraph(v["date"],    date_cell_style),
            Paragraph(v["summary"], cell_style),
        ])

    col_widths = [0.85 * inch, 1.4 * inch, 4.55 * inch]
    # splitByRow + splitInRow allow long summary cells to break across pages so
    # a single dense version row never crashes the layout (was a v11 issue).
    tbl = Table(rows, colWidths=col_widths, repeatRows=1, splitByRow=1, splitInRow=True)
    tbl.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#0a3a72")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 11),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 8),
        ("TOPPADDING",   (0, 0), (-1, 0), 8),
        # Body
        ("VALIGN",       (0, 1), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 1), (-1, -1), 8),
        # Zebra striping
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f4f7fb"), colors.white]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#cdd5e0")),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 14))
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#888"),
    )
    story.append(Paragraph(
        "Version numbers match the CACHE_VERSION string in sw.js. Pre-v8 "
        "entries were back-filled retroactively after that file was introduced.",
        footer_style,
    ))

    doc.build(story)


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "revision_history.pdf")
    build_pdf(out)
    print(f"Wrote {out}")
