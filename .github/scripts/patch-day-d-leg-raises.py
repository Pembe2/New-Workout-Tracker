from pathlib import Path

path = Path("strength-circuit-2-day.html")
text = path.read_text(encoding="utf-8")

old = '        {name:"Circuit 2 - Weighted Hip Thrust", sets:3, reps:"10-15", rest:"30-45s", cue:"Main gym; pause at the top and finish with the glutes without overextending the low back."},'
new = '        {name:"Circuit 2 - Leg Raises", sets:3, reps:"12-15", rest:"30-45s", cue:"Main gym; control the pelvis and lower slowly without arching the low back."},'

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exactly 1 Day D weighted hip thrust definition, found {count}")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
