from pathlib import Path

path = Path("workout.html")
text = path.read_text(encoding="utf-8")

old = '''      mobility:[
        {name:"90/90 hip switches", dose:"2x6/side", cue:"Stay tall; move slowly into range."},
        {name:"World's Greatest Stretch", dose:"1-2x/side", cue:"Long exhale; rotate through upper back."},
        {name:"Ankle dorsiflexion rocks", dose:"2x10/side", cue:"Heel stays down; knee tracks over toes."},
      ],
      lifts:[
        {name:"Walking Lunges", sets:3, reps:"12/leg", rest:"90s", cue:"Long stride; stable knee."},
        {name:"Squat", sets:4, reps:"5-8", rest:"90-120s", cue:"Brace hard; consistent depth; clean reps.", options:["Back","Front"]},
        {name:"Romanian Deadlift", sets:3, reps:"8", rest:"90-120s", cue:"Hinge; neutral spine; feel hamstrings."},
'''

new = '''      mobility:[
        {name:"Bodyweight Walking Lunges", dose:"3 sets", cue:"Long stride; stay tall and move smoothly."},
        {name:"Bodyweight Walking Single-Leg RDL", dose:"3 sets", cue:"Reach long through the back leg; keep hips square and move under control."},
        {name:"90/90 hip switches", dose:"2x6/side", cue:"Stay tall; move slowly into range."},
        {name:"Ankle dorsiflexion rocks", dose:"2x10/side", cue:"Heel stays down; knee tracks over toes."},
      ],
      lifts:[
        {name:"Squat", sets:4, reps:"5-8", rest:"90-120s", cue:"Brace hard; consistent depth; clean reps.", options:["Back","Front"]},
        {name:"Romanian Deadlift", sets:3, reps:"8", rest:"90-120s", cue:"Hinge; neutral spine; feel hamstrings."},
        {name:"Walking Lunges", sets:3, reps:"12/leg", rest:"90s", cue:"Long stride; stable knee."},
'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected exactly 1 Day 2 block, found {count}")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
