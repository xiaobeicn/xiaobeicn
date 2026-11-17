#!/usr/bin/env python3
"""Generate the profile header SVG in dark/light variants.

Single source of truth for the header artwork: layout is shared, only the
palette differs between variants. `refresh.py` calls `generate()` to update
the starred count and date without hand-editing SVG.
"""
import argparse
import os

MONO = "ui-monospace,'SF Mono','JetBrains Mono','Fira Code',Menlo,Consolas,monospace"

PALETTES = {
    "dark": dict(bg="#0D1117", panel="#11161D", border="#30363D", grid="#161B22",
                 primary="#E6EDF3", secondary="#8B949E", accent="#FFB224",
                 dot="#3FB950", trace="#FFB224", trace_opacity="0.4"),
    "light": dict(bg="#FFFFFF", panel="#F6F8FA", border="#D0D7DE", grid="#EFF1F3",
                  primary="#1F2328", secondary="#656D76", accent="#9A6700",
                  dot="#1A7F37", trace="#BF8700", trace_opacity="0.65"),
}


def render(p, *, starred, date, verified):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="212" viewBox="0 0 880 212" role="img">
  <title>xiaobeicn — dissecting AI agent harnesses, curating signal since 2013</title>
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{p['grid']}" stroke-width="1"/>
    </pattern>
  </defs>
  <rect x="1" y="1" width="878" height="210" rx="8" fill="{p['bg']}"/>
  <rect x="1" y="1" width="878" height="210" rx="8" fill="url(#grid)"/>
  <rect x="1" y="1" width="878" height="210" rx="8" fill="none" stroke="{p['border']}" stroke-width="1"/>
  <g stroke="{p['accent']}" stroke-width="2" fill="none">
    <path d="M16 6H6V16"/>
    <path d="M864 6h10v10"/>
    <path d="M16 206H6v-10"/>
    <path d="M864 206h10v-10"/>
  </g>
  <text x="32" y="20" font-family="{MONO}" font-size="12" fill="{p['secondary']}"><tspan fill="{p['accent']}">$</tspan> cat README.md</text>
  <text x="848" y="20" text-anchor="end" font-family="{MONO}" font-size="12" fill="{p['secondary']}">main · {date}</text>
  <line x1="1" y1="30" x2="879" y2="30" stroke="{p['border']}" stroke-width="1"/>
  <text x="32" y="74" font-family="{MONO}" font-size="34" font-weight="700" letter-spacing="1" fill="{p['primary']}">xiaobeicn<tspan fill="{p['accent']}">▋</tspan></text>
  <text x="32" y="102" font-family="{MONO}" font-size="14" fill="{p['primary']}">Dissecting AI agent harnesses, curating signal since 2013.</text>
  <text x="32" y="126" font-family="{MONO}" font-size="13" fill="{p['secondary']}">backend → agents · PHP/Laravel · Go/ES/Redis · Python/FastAPI</text>
  <polyline points="32,151 92,151 104,139 116,151 196,151 208,163 220,151 320,151 332,141 344,151 452,151 464,159 476,151 560,151" fill="none" stroke="{p['trace']}" stroke-width="1.5" opacity="{p['trace_opacity']}"/>
  <rect x="592" y="44" width="256" height="112" rx="6" fill="{p['panel']}" stroke="{p['border']}" stroke-width="1"/>
  <line x1="720" y1="44" x2="720" y2="156" stroke="{p['border']}" stroke-width="1"/>
  <line x1="592" y1="100" x2="848" y2="100" stroke="{p['border']}" stroke-width="1"/>
  <text x="608" y="66" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{p['secondary']}">STARRED</text>
  <text x="608" y="92" font-family="{MONO}" font-size="24" font-weight="700" fill="{p['accent']}">{starred:,}</text>
  <text x="736" y="66" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{p['secondary']}">LISTS</text>
  <text x="736" y="92" font-family="{MONO}" font-size="24" font-weight="700" fill="{p['primary']}">11</text>
  <text x="608" y="122" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{p['secondary']}">SINCE</text>
  <text x="608" y="148" font-family="{MONO}" font-size="24" font-weight="700" fill="{p['primary']}">2013</text>
  <text x="736" y="122" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{p['secondary']}">STAGES</text>
  <text x="736" y="148" font-family="{MONO}" font-size="24" font-weight="700" fill="{p['primary']}">6</text>
  <line x1="1" y1="172" x2="879" y2="172" stroke="{p['border']}" stroke-width="1"/>
  <circle cx="38" cy="189" r="4" fill="{p['dot']}"/>
  <text x="50" y="194" font-family="{MONO}" font-size="12.5" fill="{p['secondary']}"><tspan fill="{p['primary']}">harness-learn</tspan> — 6 stages · evidence-graded · verified {verified}</text>
  <text x="848" y="194" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{p['secondary']}">unxai.top · @unxai</text>
</svg>
"""


def generate(out_dir, *, starred, date, verified):
    for variant, palette in PALETTES.items():
        path = os.path.join(out_dir, f"header-{variant}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(palette, starred=starred, date=date, verified=verified))
        print(f"wrote {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--starred", type=int, required=True)
    ap.add_argument("--date", required=True, help="YYYY-MM-DD, shown top-right")
    ap.add_argument("--verified", required=True, help="YYYY-MM-DD, harness-learn verification date")
    ap.add_argument("--out-dir", default="assets")
    args = ap.parse_args()
    generate(args.out_dir, starred=args.starred, date=args.date, verified=args.verified)
