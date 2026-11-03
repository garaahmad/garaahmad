#!/usr/bin/env python3
"""Generate the self-contained, theme-aware SVGs used by the profile README.

No third-party packages, remote fonts, JavaScript, or animation services required.
Run from any directory: python3 scripts/generate_profile_assets.py
"""

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str
    panel: str
    text: str
    muted: str
    faint: str
    border: str
    mint: str
    blue: str
    coral: str
    gold: str


DARK = Theme("dark", "#0B111B", "#111C2A", "#F2F6FC", "#A5B5C9", "#71839B",
             "#263548", "#79E8C5", "#83B8FF", "#FF927F", "#E9C98D")
LIGHT = Theme("light", "#F5F8FC", "#FFFFFF", "#142338", "#4D617B", "#64748B",
              "#D5DFEB", "#087F69", "#245FBB", "#BE4434", "#886019")


def document(t: Theme, height: int, title: str, description: str,
             defs: str, css: str, body: str, width: int = 1200) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title description">
<title id="title">{escape(title)}</title>
<desc id="description">{escape(description)}</desc>
<defs>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" stroke="{t.border}" stroke-opacity=".32" stroke-width=".6"/></pattern>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{t.mint}"/><stop offset=".55" stop-color="{t.blue}"/><stop offset="1" stop-color="{t.coral}"/></linearGradient>
  <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t.panel}"/><stop offset="1" stop-color="{t.bg}"/></linearGradient>
  <radialGradient id="halo"><stop stop-color="{t.blue}" stop-opacity=".14"/><stop offset="1" stop-color="{t.blue}" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="{width}" height="{height}" rx="22"/></clipPath>
{defs}</defs>
<style>
text {{ font-family: {FONT}; }}
.mono {{ font-family: {MONO}; }}
.label {{ font-size: 11px; font-weight: 600; letter-spacing: 2px; }}
.muted {{ fill: {t.muted}; }}
.faint {{ fill: {t.faint}; }}
{css}
@media (prefers-reduced-motion: reduce) {{
  .motion {{ animation: none !important; }}
  .role {{ animation: none !important; transform: none !important; opacity: 0 !important; }}
  .role-1 {{ opacity: 1 !important; }}
  .packet-motion {{ display: none; }}
}}
</style>
<g clip-path="url(#frame)">
<rect width="{width}" height="{height}" fill="{t.bg}"/>
{body}
</g>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="21.5" stroke="{t.border}"/>
</svg>'''


def flutter_mark(x: float, y: float, scale: float, t: Theme) -> str:
    """Flutter's geometric mark, drawn locally rather than fetched at runtime."""
    return f'''<g transform="translate({x} {y}) scale({scale})">
<path d="M29 0H47L18 29L9 20Z" fill="{t.blue}"/>
<path d="M29 30H47L29 48L38 57H20L11 48Z" fill="{t.blue}"/>
<path d="M20 39L29 30L38 39L29 48Z" fill="{t.mint}"/>
</g>'''


def react_mark(x: float, y: float, t: Theme) -> str:
    return f'''<g transform="translate({x} {y})" stroke="{t.blue}" stroke-width="1.6">
<ellipse rx="23" ry="8"/><ellipse rx="23" ry="8" transform="rotate(60)"/><ellipse rx="23" ry="8" transform="rotate(120)"/><circle r="3.3" fill="{t.blue}" stroke="none"/>
</g>'''


def hero(t: Theme) -> str:
    css = f'''
.float-phone {{ animation: float-phone 7s ease-in-out infinite; }}
.float-browser {{ animation: float-browser 8s ease-in-out infinite; }}
.orbit {{ animation: orbit 36s linear infinite; transform-origin: 0px 0px; }}
.status-dot {{ animation: breathe 3s ease-in-out infinite; }}
.scan {{ animation: scan 6s ease-in-out infinite; }}
.cursor {{ animation: cursor 1.2s step-end infinite; }}
.role {{ opacity: 0; }}
.role-1 {{ opacity: 1; animation: role-one 18s infinite; }}
.role-2 {{ animation: role-two 18s infinite; }}
.role-3 {{ animation: role-three 18s infinite; }}
@keyframes float-phone {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-9px); }} }}
@keyframes float-browser {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(7px); }} }}
@keyframes orbit {{ to {{ transform: rotate(360deg); }} }}
@keyframes breathe {{ 0%,100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
@keyframes scan {{ 0%,100% {{ transform: translateY(0); opacity: 0; }} 20%,70% {{ opacity: .55; }} 85% {{ transform: translateY(175px); opacity: 0; }} }}
@keyframes cursor {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
@keyframes role-one {{ 0%,28% {{ opacity:1; transform:translateY(0); }} 33%,95% {{ opacity:0; transform:translateY(-7px); }} 100% {{ opacity:1; transform:translateY(0); }} }}
@keyframes role-two {{ 0%,28% {{ opacity:0; transform:translateY(7px); }} 33%,61% {{ opacity:1; transform:translateY(0); }} 66%,100% {{ opacity:0; transform:translateY(-7px); }} }}
@keyframes role-three {{ 0%,61% {{ opacity:0; transform:translateY(7px); }} 66%,95% {{ opacity:1; transform:translateY(0); }} 100% {{ opacity:0; transform:translateY(7px); }} }}
'''
    body = f'''
<rect width="1200" height="440" fill="url(#grid)"/>
<ellipse cx="980" cy="208" rx="335" ry="285" fill="url(#halo)"/>
<path d="M56 0H400" stroke="url(#accent)" stroke-width="3"/>
<rect x="54" y="34" width="38" height="38" rx="11" fill="{t.panel}" stroke="{t.border}"/>
<path d="M64 60L72 44L80 60M67 55H77" stroke="{t.mint}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<text x="106" y="58" fill="{t.muted}" class="mono" font-size="12" letter-spacing="1.4">AHMAD / SOFTWARE ENGINEER</text>
<rect x="939" y="39" width="205" height="29" rx="14.5" fill="{t.panel}" stroke="{t.border}"/>
<circle class="motion status-dot" cx="957" cy="53.5" r="3.5" fill="{t.mint}"/>
<text x="971" y="57.5" fill="{t.muted}" class="mono" font-size="10.5" letter-spacing="1">MOBILE × WEB × AI</text>
<text x="56" y="118" fill="{t.mint}" class="label">BUILDING ACROSS THE STACK</text>
<text x="51" y="190" fill="{t.text}" font-size="72" font-weight="750" letter-spacing="-3">Ahmad</text>
<text x="51" y="260" fill="{t.text}" font-size="72" font-weight="750" letter-spacing="-3">Al-Garably<tspan fill="{t.mint}">.</tspan></text>
<g font-size="19" class="mono">
<text x="56" y="305" fill="{t.mint}" class="mono motion role role-1">Flutter experiences, engineered.</text>
<text x="56" y="305" fill="{t.mint}" class="mono motion role role-2">React interfaces. Laravel backends.</text>
<text x="56" y="305" fill="{t.mint}" class="mono motion role role-3">From first pixel to production API.</text>
</g>
<rect class="motion cursor" x="56" y="319" width="10" height="2" rx="1" fill="{t.mint}"/>
<g font-size="10.5" class="mono" letter-spacing="1">
<rect x="56" y="347" width="183" height="29" rx="6" fill="{t.panel}" stroke="{t.border}"/>
<text x="70" y="366" fill="{t.text}" class="mono">4+ YEARS IN FLUTTER</text>
<rect x="249" y="347" width="180" height="29" rx="6" fill="{t.panel}" stroke="{t.border}"/>
<text x="263" y="366" fill="{t.text}" class="mono">FULL-STACK MINDSET</text>
</g>
<g transform="translate(964 222)">
  <circle r="156" stroke="{t.border}" stroke-dasharray="3 8"/>
  <circle r="188" stroke="{t.border}" stroke-opacity=".45"/>
  <g class="motion orbit"><circle cx="156" r="4" fill="{t.mint}"/><circle cx="-156" r="3" fill="{t.blue}"/><circle cy="-188" r="3" fill="{t.coral}"/></g>
</g>
<path d="M805 154L849 154L849 320L1100 320" stroke="{t.border}" stroke-width="1.5" stroke-dasharray="5 6"/>
<g transform="translate(786 191) rotate(-7 155 85)"><g class="motion float-browser">
<rect width="322" height="174" rx="13" fill="{t.bg}" stroke="{t.border}" stroke-width="1.5"/>
<path d="M0 33H322" stroke="{t.border}"/>
<circle cx="16" cy="16" r="3" fill="{t.coral}"/><circle cx="28" cy="16" r="3" fill="{t.gold}"/><circle cx="40" cy="16" r="3" fill="{t.mint}"/>
<rect x="68" y="10" width="185" height="12" rx="6" fill="{t.panel}"/>
{react_mark(48, 77, t)}
<text x="84" y="73" fill="{t.text}" font-size="16" font-weight="650">React</text>
<text x="84" y="92" fill="{t.muted}" class="mono" font-size="9">INTERFACES THAT FEEL RIGHT</text>
<path d="M19 110H303" stroke="{t.border}"/>
<rect x="19" y="124" width="86" height="29" rx="6" fill="{t.panel}" stroke="{t.border}"/>
<text x="32" y="143" fill="{t.coral}" class="mono" font-size="12" font-weight="600">Laravel</text>
<path d="M116 138H145M140 134L145 138L140 142" stroke="{t.faint}" stroke-width="1.5"/>
<rect x="156" y="127" width="64" height="5" rx="2.5" fill="{t.blue}" fill-opacity=".65"/>
<rect x="156" y="140" width="104" height="5" rx="2.5" fill="{t.border}"/>
<rect x="230" y="127" width="62" height="5" rx="2.5" fill="{t.border}"/>
</g></g>
<g transform="translate(956 73) rotate(10 79 137)"><g class="motion float-phone">
<rect x="-5" y="-5" width="168" height="280" rx="34" fill="{t.bg}" fill-opacity=".55"/>
<rect width="158" height="270" rx="29" fill="url(#screen)" stroke="{t.faint}" stroke-width="1.5"/>
<rect x="9" y="9" width="140" height="252" rx="23" stroke="{t.border}"/>
<rect x="56" y="14" width="46" height="10" rx="5" fill="{t.bg}"/>
<text x="23" y="53" fill="{t.muted}" class="mono" font-size="8" letter-spacing="1.2">CRAFTED TO MOVE</text>
{flutter_mark(49, 74, 1.04, t)}
<text x="79" y="156" fill="{t.text}" text-anchor="middle" font-size="21" font-weight="650">Flutter</text>
<text x="79" y="175" fill="{t.muted}" text-anchor="middle" class="mono" font-size="8.5">ONE CODEBASE. EVERY SCREEN.</text>
<rect x="24" y="195" width="110" height="26" rx="7" fill="{t.mint}" fill-opacity=".12" stroke="{t.mint}" stroke-opacity=".3"/>
<text x="79" y="212" fill="{t.mint}" text-anchor="middle" class="mono" font-size="9">iOS · Android · Web</text>
<rect x="57" y="247" width="44" height="3" rx="1.5" fill="{t.faint}"/>
<g clip-path="url(#phone-clip)"><rect class="motion scan" x="10" y="34" width="138" height="2" fill="{t.mint}"/></g>
</g></g>
<path d="M56 400H1144" stroke="{t.border}"/>
<text x="56" y="423" fill="{t.muted}" class="mono" font-size="9.5" letter-spacing="1.3">CLEAN ARCHITECTURE</text>
<circle cx="246" cy="419" r="2" fill="{t.mint}"/>
<text x="264" y="423" fill="{t.muted}" class="mono" font-size="9.5" letter-spacing="1.3">THOUGHTFUL MOTION</text>
<circle cx="453" cy="419" r="2" fill="{t.blue}"/>
<text x="471" y="423" fill="{t.muted}" class="mono" font-size="9.5" letter-spacing="1.3">REAL-WORLD PRODUCTS</text>
<text x="1144" y="423" text-anchor="end" fill="{t.faint}" class="mono" font-size="10">@garaahmad</text>
'''
    defs = '<clipPath id="phone-clip"><rect x="10" y="34" width="138" height="204" rx="16"/></clipPath>'
    return document(t, 440, "Ahmad Al-Garably — Flutter & Full-Stack Developer",
                    "4+ years in Flutter. Full-stack web development with React and Laravel. Animated phone and browser illustrations.",
                    defs, css, body)


def stack(t: Theme) -> str:
    items = [("Flutter", t.blue), ("Dart", t.blue), ("React", t.blue),
             ("Laravel", t.coral), ("PHP", t.blue), ("TypeScript", t.blue),
             ("Firebase", t.gold), ("SQL", t.blue), ("REST APIs", t.mint),
             ("Clean Architecture", t.mint), ("AI Integrations", t.gold)]
    chips = []
    x = 0
    for label, color in items:
        width = len(label) * 8 + 52
        chips.append(f'''<g transform="translate({x} 18)"><rect width="{width}" height="44" rx="9" fill="{t.panel}" stroke="{t.border}"/><circle cx="19" cy="22" r="3.5" fill="{color}"/><text x="32" y="27" fill="{t.text}" class="mono" font-size="13">{escape(label)}</text></g>''')
        x += width + 14
    css = f'''.marquee {{ animation: marquee 42s linear infinite; }}
@keyframes marquee {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{x}px); }} }}'''
    defs = f'''<clipPath id="window"><rect width="1200" height="80"/></clipPath>
<linearGradient id="fade"><stop stop-color="white" stop-opacity="0"/><stop offset=".055" stop-color="white"/><stop offset=".945" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
<mask id="edges"><rect width="1200" height="80" fill="url(#fade)"/></mask>'''
    body = f'''<g clip-path="url(#window)"><g mask="url(#edges)"><g class="motion marquee">{''.join(chips)}<g transform="translate({x} 0)">{''.join(chips)}</g></g></g></g>'''
    return document(t, 80, "My engineering toolkit",
                    "Flutter, Dart, React, Laravel, PHP, TypeScript, Firebase, SQL, REST APIs, Clean Architecture and AI integrations. The moving labels are decorative; the same skills are listed in the README.",
                    defs, css, body)


def flow(t: Theme) -> str:
    cards = [
        ("01 / EXPERIENCE", "Flutter · React", "Interfaces people enjoy", t.blue),
        ("02 / APPLICATION", "BLoC · Riverpod", "Predictable app state", t.mint),
        ("03 / SERVICE", "Laravel · REST", "Secure business logic", t.coral),
        ("04 / DATA", "SQL · Firebase", "Reliable persistence", t.gold),
    ]
    parts = []
    for index, (label, value, caption, color) in enumerate(cards):
        x = 36 + index * 294
        parts.append(f'''<g transform="translate({x} 35)">
<rect width="246" height="124" rx="12" fill="{t.panel}" stroke="{t.border}"/>
<path d="M18 0H72" stroke="{color}" stroke-width="2"/>
<text x="18" y="29" fill="{color}" class="mono" font-size="9.5" letter-spacing="1.2">{label}</text>
<text x="18" y="64" fill="{t.text}" font-size="20" font-weight="650" letter-spacing="-.4">{value}</text>
<text x="18" y="91" fill="{t.muted}" font-size="12">{caption}</text>
</g>''')
        if index < 3:
            parts.append(f'''<path d="M{x + 254} 97H{x + 284}M{x + 279} 93L{x + 284} 97L{x + 279} 101" stroke="{t.faint}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>''')
    css = '''.packet { animation: packet 6s linear infinite; }
.packet-two { animation-delay: -3s; }
@keyframes packet { 0% { transform: translateX(0); opacity: 0; } 5%,90% { opacity: 1; } 100% { transform: translateX(1070px); opacity: 0; } }
.endpoint { animation: endpoint 4s ease-in-out infinite; }
@keyframes endpoint { 0%,100% { opacity: .35; } 50% { opacity: .9; } }'''
    body = f'''<rect width="1200" height="210" fill="url(#grid)" opacity=".5"/>
{''.join(parts)}
<g class="packet-motion"><circle class="motion packet" cx="65" cy="169" r="2.5" fill="{t.mint}"/><circle class="motion packet packet-two" cx="65" cy="169" r="2.5" fill="{t.blue}"/></g>
<path d="M65 169H1135" stroke="{t.border}" stroke-dasharray="2 6"/>
<text x="600" y="195" text-anchor="middle" fill="{t.muted}" class="mono" font-size="9.5" letter-spacing="1.7">ONE PRODUCT. EVERY LAYER CONSIDERED.</text>'''
    return document(t, 210, "From interface to infrastructure",
                    "Experience: Flutter and React. Application: BLoC and Riverpod. Service: Laravel and REST. Data: SQL and Firebase. This diagram describes capabilities, not a single project's architecture.",
                    "", css, body)


def footer(t: Theme) -> str:
    css = '''.pulse { animation: pulse 3s ease-out infinite; transform-origin: 1090px 77px; }
@keyframes pulse { 0% { transform: scale(.9); opacity: .6; } 85%,100% { transform: scale(1.35); opacity: 0; } }
.arrow { animation: arrow 3s ease-in-out infinite; }
@keyframes arrow { 0%,100% { transform: translate(0,0); } 50% { transform: translate(3px,-3px); } }'''
    body = f'''<rect width="1200" height="154" fill="url(#grid)" opacity=".5"/>
<ellipse cx="1090" cy="77" rx="180" ry="140" fill="url(#halo)"/>
<path d="M56 0H300" stroke="url(#accent)" stroke-width="2"/>
<text x="56" y="39" fill="{t.mint}" class="label">HAVE AN IDEA? LET’S MAKE IT REAL.</text>
<text x="54" y="85" fill="{t.text}" font-size="32" font-weight="650" letter-spacing="-.8">Good products are built end to end.</text>
<text x="56" y="117" fill="{t.muted}" font-size="14">Mobile, web, and the systems behind them. Let’s build something that matters.</text>
<circle class="motion pulse" cx="1090" cy="77" r="35" stroke="{t.mint}"/>
<circle cx="1090" cy="77" r="31" fill="{t.panel}" stroke="{t.border}"/>
<g class="motion arrow"><path d="M1080 87L1100 67M1082 67H1100V85" stroke="{t.mint}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>'''
    return document(t, 154, "Let's build something that matters",
                    "Contact Ahmad about mobile and full-stack web development using the email and LinkedIn links below.",
                    "", css, body)


def hero_mobile(t: Theme) -> str:
    css = f'''
.float-phone {{ animation: phone 7s ease-in-out infinite; }}
.float-browser {{ animation: browser 8s ease-in-out infinite; }}
.status-dot {{ animation: breathe 3s ease-in-out infinite; }}
.role {{ opacity: 0; }}
.role-1 {{ opacity: 1; animation: role-one 18s infinite; }}
.role-2 {{ animation: role-two 18s infinite; }}
.role-3 {{ animation: role-three 18s infinite; }}
@keyframes phone {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
@keyframes browser {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(6px); }} }}
@keyframes breathe {{ 0%,100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
@keyframes role-one {{ 0%,28% {{ opacity:1; }} 33%,95% {{ opacity:0; }} 100% {{ opacity:1; }} }}
@keyframes role-two {{ 0%,28% {{ opacity:0; }} 33%,61% {{ opacity:1; }} 66%,100% {{ opacity:0; }} }}
@keyframes role-three {{ 0%,61% {{ opacity:0; }} 66%,95% {{ opacity:1; }} 100% {{ opacity:0; }} }}
'''
    body = f'''
<rect width="640" height="680" fill="url(#grid)"/>
<ellipse cx="450" cy="485" rx="300" ry="235" fill="url(#halo)"/>
<path d="M32 0H240" stroke="url(#accent)" stroke-width="3"/>
<text x="32" y="49" fill="{t.muted}" class="mono" font-size="16" letter-spacing="1.5">AHMAD / SOFTWARE ENGINEER</text>
<circle class="motion status-dot" cx="591" cy="43" r="5" fill="{t.mint}"/>
<text x="32" y="107" fill="{t.mint}" class="mono" font-size="15" letter-spacing="2">BUILDING ACROSS THE STACK</text>
<text x="28" y="180" fill="{t.text}" font-size="70" font-weight="750" letter-spacing="-3">Ahmad</text>
<text x="28" y="251" fill="{t.text}" font-size="70" font-weight="750" letter-spacing="-3">Al-Garably<tspan fill="{t.mint}">.</tspan></text>
<g font-size="22" class="mono">
<text x="32" y="298" fill="{t.mint}" class="mono motion role role-1">Flutter experiences, engineered.</text>
<text x="32" y="298" fill="{t.mint}" class="mono motion role role-2">React interfaces. Laravel backends.</text>
<text x="32" y="298" fill="{t.mint}" class="mono motion role role-3">From first pixel to production API.</text>
</g>
<rect x="32" y="327" width="239" height="38" rx="7" fill="{t.panel}" stroke="{t.border}"/>
<text x="47" y="352" fill="{t.text}" class="mono" font-size="16">4+ YEARS IN FLUTTER</text>
<rect x="283" y="327" width="237" height="38" rx="7" fill="{t.panel}" stroke="{t.border}"/>
<text x="298" y="352" fill="{t.text}" class="mono" font-size="16">FULL-STACK MINDSET</text>
<g transform="translate(34 434) rotate(-5 150 85)"><g class="motion float-browser">
<rect width="322" height="174" rx="13" fill="{t.bg}" stroke="{t.border}" stroke-width="1.5"/>
<path d="M0 33H322" stroke="{t.border}"/>
<circle cx="16" cy="16" r="3" fill="{t.coral}"/><circle cx="28" cy="16" r="3" fill="{t.gold}"/><circle cx="40" cy="16" r="3" fill="{t.mint}"/>
{react_mark(48, 77, t)}
<text x="84" y="73" fill="{t.text}" font-size="20" font-weight="650">React</text>
<text x="84" y="94" fill="{t.muted}" class="mono" font-size="11">FRONTEND ENGINEERING</text>
<path d="M19 110H303" stroke="{t.border}"/>
<rect x="19" y="124" width="108" height="31" rx="6" fill="{t.panel}" stroke="{t.border}"/>
<text x="33" y="145" fill="{t.coral}" class="mono" font-size="17" font-weight="600">Laravel</text>
<path d="M140 139H169M164 135L169 139L164 143" stroke="{t.faint}" stroke-width="1.5"/>
<rect x="184" y="129" width="104" height="5" rx="2.5" fill="{t.blue}" fill-opacity=".65"/>
<rect x="184" y="143" width="74" height="5" rx="2.5" fill="{t.border}"/>
</g></g>
<g transform="translate(410 397) rotate(8 79 125)"><g class="motion float-phone">
<rect width="158" height="250" rx="29" fill="url(#screen)" stroke="{t.faint}" stroke-width="1.5"/>
<rect x="9" y="9" width="140" height="232" rx="23" stroke="{t.border}"/>
<rect x="56" y="14" width="46" height="10" rx="5" fill="{t.bg}"/>
{flutter_mark(49, 53, 1.04, t)}
<text x="79" y="138" fill="{t.text}" text-anchor="middle" font-size="23" font-weight="650">Flutter</text>
<text x="79" y="160" fill="{t.muted}" text-anchor="middle" class="mono" font-size="10">EVERY SCREEN.</text>
<rect x="19" y="180" width="120" height="30" rx="7" fill="{t.mint}" fill-opacity=".12" stroke="{t.mint}" stroke-opacity=".3"/>
<text x="79" y="200" fill="{t.mint}" text-anchor="middle" class="mono" font-size="10">iOS · Android · Web</text>
<rect x="57" y="231" width="44" height="3" rx="1.5" fill="{t.faint}"/>
</g></g>
<path d="M32 646H608" stroke="{t.border}"/>
<text x="32" y="668" fill="{t.muted}" class="mono" font-size="12" letter-spacing="1">CLEAN CODE. THOUGHTFUL MOTION.</text>
<text x="608" y="668" text-anchor="end" fill="{t.faint}" class="mono" font-size="12">@garaahmad</text>
'''
    return document(t, 680, "Ahmad Al-Garably — Flutter & Full-Stack Developer",
                    "4+ years in Flutter. Full-stack web development with React and Laravel. Animated phone and browser illustrations.",
                    "", css, body, width=640)


def stack_mobile(t: Theme) -> str:
    items = [("Flutter", t.blue), ("React", t.blue), ("Laravel", t.coral),
             ("Dart", t.blue), ("PHP", t.blue), ("TypeScript", t.blue),
             ("Firebase", t.gold), ("SQL", t.blue), ("REST APIs", t.mint),
             ("Clean Architecture", t.mint), ("AI Integrations", t.gold)]
    chips = []
    x = 0
    for label, color in items:
        width = len(label) * 12 + 64
        chips.append(f'''<g transform="translate({x} 16)"><rect width="{width}" height="64" rx="11" fill="{t.panel}" stroke="{t.border}"/><circle cx="24" cy="32" r="4.5" fill="{color}"/><text x="41" y="40" fill="{t.text}" class="mono" font-size="22">{escape(label)}</text></g>''')
        x += width + 18
    css = f'''.marquee {{ animation: marquee 42s linear infinite; }}
@keyframes marquee {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{x}px); }} }}'''
    defs = '''<linearGradient id="fade"><stop stop-color="white" stop-opacity="0"/><stop offset=".055" stop-color="white"/><stop offset=".945" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient><mask id="edges"><rect width="640" height="96" fill="url(#fade)"/></mask>'''
    body = f'''<g mask="url(#edges)"><g class="motion marquee">{''.join(chips)}<g transform="translate({x} 0)">{''.join(chips)}</g></g></g>'''
    return document(t, 96, "My engineering toolkit",
                    "Flutter, React, Laravel, Dart, PHP, TypeScript, Firebase, SQL, REST APIs, Clean Architecture and AI integrations.",
                    defs, css, body, width=640)


def flow_mobile(t: Theme) -> str:
    cards = [
        ("01 / EXPERIENCE", "Flutter · React", "Interfaces people enjoy", t.blue),
        ("02 / APPLICATION", "BLoC · Riverpod", "Predictable app state", t.mint),
        ("03 / SERVICE", "Laravel · REST", "Secure business logic", t.coral),
        ("04 / DATA", "SQL · Firebase", "Reliable persistence", t.gold),
    ]
    parts = []
    for index, (label, value, caption, color) in enumerate(cards):
        y = 20 + index * 124
        parts.append(f'''<g transform="translate(24 {y})"><rect width="592" height="104" rx="12" fill="{t.panel}" stroke="{t.border}"/><path d="M20 0H90" stroke="{color}" stroke-width="3"/><text x="20" y="28" fill="{color}" class="mono" font-size="14" letter-spacing="1.4">{label}</text><text x="20" y="61" fill="{t.text}" font-size="28" font-weight="650">{value}</text><text x="20" y="87" fill="{t.muted}" font-size="18">{caption}</text></g>''')
        if index < 3:
            parts.append(f'''<path d="M320 {y + 108}V{y + 119}M316 {y + 115}L320 {y + 119}L324 {y + 115}" stroke="{t.faint}" stroke-width="1.5" stroke-linecap="round"/>''')
    css = '''.packet { animation: packet 6s linear infinite; }
@keyframes packet { 0% { transform: translateY(0); opacity: 0; } 10%,90% { opacity: 1; } 100% { transform: translateY(470px); opacity: 0; } }'''
    body = f'''<rect width="640" height="548" fill="url(#grid)" opacity=".5"/>
{''.join(parts)}
<circle class="motion packet packet-motion" cx="12" cy="24" r="3" fill="{t.mint}"/>
<text x="320" y="529" text-anchor="middle" fill="{t.muted}" class="mono" font-size="13" letter-spacing="1.3">ONE PRODUCT. EVERY LAYER CONSIDERED.</text>'''
    return document(t, 548, "From interface to infrastructure",
                    "Experience: Flutter and React. Application: BLoC and Riverpod. Service: Laravel and REST. Data: SQL and Firebase. A capability map, not a single project's architecture.",
                    "", css, body, width=640)


def footer_mobile(t: Theme) -> str:
    css = '''.pulse { animation: pulse 3s ease-out infinite; transform-origin: 566px 66px; }
@keyframes pulse { 0% { transform: scale(.9); opacity: .6; } 85%,100% { transform: scale(1.35); opacity: 0; } }
.arrow { animation: arrow 3s ease-in-out infinite; }
@keyframes arrow { 0%,100% { transform: translate(0,0); } 50% { transform: translate(3px,-3px); } }'''
    body = f'''<rect width="640" height="252" fill="url(#grid)" opacity=".5"/>
<ellipse cx="565" cy="80" rx="180" ry="160" fill="url(#halo)"/>
<path d="M32 0H240" stroke="url(#accent)" stroke-width="3"/>
<text x="32" y="42" fill="{t.mint}" class="mono" font-size="14" letter-spacing="1.1">HAVE AN IDEA? LET’S MAKE IT REAL.</text>
<text x="30" y="103" fill="{t.text}" font-size="37" font-weight="650" letter-spacing="-1">Good products are</text>
<text x="30" y="148" fill="{t.text}" font-size="37" font-weight="650" letter-spacing="-1">built end to end.</text>
<text x="32" y="193" fill="{t.muted}" font-size="19">Mobile, web, and the systems behind them.</text>
<text x="32" y="222" fill="{t.muted}" font-size="19">Let’s build something that matters.</text>
<circle class="motion pulse" cx="566" cy="66" r="32" stroke="{t.mint}"/>
<circle cx="566" cy="66" r="28" fill="{t.panel}" stroke="{t.border}"/>
<g class="motion arrow"><path d="M556 76L576 56M558 56H576V74" stroke="{t.mint}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>'''
    return document(t, 252, "Let's build something that matters",
                    "Contact Ahmad about mobile and full-stack web development using the email and LinkedIn links below.",
                    "", css, body, width=640)


def static_variant(svg: str) -> str:
    """Guarantee a still image even in browsers that isolate SVG image media settings."""
    overrides = '''
.motion, .role { animation: none !important; }
.role { opacity: 0 !important; transform: none !important; }
.role-1 { opacity: 1 !important; }
.packet-motion { display: none !important; }
'''
    return svg.replace('</style>', overrides + '</style>')


def contact_badges() -> None:
    """Static link labels that remain readable in either GitHub theme."""
    t = DARK
    labels = [
        ("email", "Email me", t.mint, '<path d="M3 5H21V19H3ZM3 5L12 12L21 5" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'),
        ("linkedin", "LinkedIn", t.blue, '<rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.5"/><path d="M7 10V17M11 17V10M11 13C11 9 17 9 17 13V17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="7" cy="7" r="1" fill="currentColor"/>'),
        ("github", "GitHub", t.gold, '<path d="M12 2.5a9.5 9.5 0 0 0-3 18.51c.48.09.65-.2.65-.46v-1.77c-2.67.58-3.23-1.13-3.23-1.13-.44-1.1-1.07-1.4-1.07-1.4-.87-.6.07-.59.07-.59.96.07 1.47.99 1.47.99.86 1.47 2.25 1.05 2.8.8.09-.62.34-1.05.61-1.29-2.13-.24-4.37-1.07-4.37-4.71 0-1.04.37-1.89.98-2.56-.1-.24-.42-1.21.09-2.52 0 0 .8-.26 2.61.98A9.1 9.1 0 0 1 12 7.03c.81 0 1.62.11 2.38.32 1.81-1.24 2.61-.98 2.61-.98.51 1.31.19 2.28.09 2.52.61.67.98 1.52.98 2.56 0 3.65-2.24 4.46-4.38 4.7.34.3.65.88.65 1.78v2.62c0 .26.17.55.66.46A9.5 9.5 0 0 0 12 2.5Z" fill="currentColor"/>'),
    ]
    for name, label, color, icon in labels:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="132" height="34" viewBox="0 0 132 34" role="img" aria-labelledby="title"><title id="title">{label}</title><rect x=".5" y=".5" width="131" height="33" rx="7" fill="{t.panel}" stroke="{t.border}"/><g transform="translate(11 7) scale(.84)" color="{color}">{icon}</g><text x="40" y="22" fill="{t.text}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="13" font-weight="600">{label}</text><path d="M115 20L121 14M116 14H121V19" stroke="{t.muted}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
        ElementTree.fromstring(svg)
        (ASSETS / f"badge-{name}.svg").write_text(svg, encoding="utf-8")
        print(f"Generated badge-{name}.svg")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    contact_badges()
    generators = {
        "hero": hero, "stack": stack, "flow": flow, "connect": footer,
        "hero-mobile": hero_mobile, "stack-mobile": stack_mobile,
        "flow-mobile": flow_mobile, "connect-mobile": footer_mobile,
    }
    for theme in (DARK, LIGHT):
        for name, generator in generators.items():
            svg = generator(theme)
            ElementTree.fromstring(svg)
            destination = ASSETS / f"{name}-{theme.name}.svg"
            destination.write_text(svg, encoding="utf-8")
            print(f"Generated {destination.name} ({len(svg.encode('utf-8')):,} bytes)")
            still = static_variant(svg)
            ElementTree.fromstring(still)
            still_path = ASSETS / f"{name}-static-{theme.name}.svg"
            still_path.write_text(still, encoding="utf-8")
            print(f"Generated {still_path.name}")


if __name__ == "__main__":
    main()
