# SPEC-002 — Sitcom scene floors with cuts
1. Load 4 optional PNGs from himym_data/ (gitignored): floor_apt_day.png,
   floor_apt_night.png, floor_pub_day.png, floor_pub_night.png.
2. Floor = f(state.location, time_of_day). On location change: 350ms black
   "cut" + 🎬 clap (if sfx on) — sitcom scene change.
3. Per-scene anchors (tune to art): 
   Apartment: LivingRoom [[640,520],[830,470],[470,470]], Kitchen [[950,640],[1050,560]],
   Bedroom [[260,600],[360,640]]
   MacLarens: Bar [[640,640],[840,600],[460,620]], Booth [[250,430],[330,520]]
   Re-route all agents through routeTo() on scene change.
4. ambience() gated per scene: TV/dust = apartment only; neon/steam = pub only.
5. Fallback: if scene PNGs missing, use existing combined floor_day/night.
Commit: spec-002 scene floors
