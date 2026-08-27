from pathlib import Path

path = Path("strength-circuit-2-day.html")
text = path.read_text(encoding="utf-8")

# Update the page label now that this is a true A/B/C/D plan.
text = text.replace("<title>2-Day Strength Circuit</title>", "<title>4-Day Strength Circuit</title>", 1)
text = text.replace("<h1>2-Day Strength Circuit</h1>", "<h1>4-Day Strength Circuit</h1>", 1)
text = text.replace("// Circuit plan from 2-Day_Strength_Circuit_Workout.docx.\n", "// Four-day A/B/C/D strength circuit plan.\n", 1)

old_day_c = '''    {
      id:"d3", short:"Day 3 (A)", title:"Push + Quad Focus",
      muscleGroups:["Chest","Shoulders","Triceps","Quads","Hamstrings","Calves","Core","Carries"],
      mobility:[
        {name:"Treadmill warm-up", dose:"10 min", cue:"5 min brisk walk, then 5 min incline walk."},
      ],
      lifts:[
        {name:"Circuit 1 - Goblet Squat", sets:3, reps:"8-10", rest:"30-45s", cue:"Pair with neutral-grip dumbbell bench press; move steadily between stations."},
        {name:"Circuit 1 - Neutral-Grip Dumbbell Bench Press", sets:3, reps:"8-10", rest:"30-45s", cue:"Pair with goblet squat; keep shoulders packed and press smoothly."},
        {name:"Circuit 2 - Bulgarian Split Squat", sets:3, reps:"8-10/leg", rest:"30-45s", cue:"Pair with machine or cable chest press; controlled depth and stable knee."},
        {name:"Circuit 2 - Machine/Cable Chest Press", sets:3, reps:"10-12", rest:"30-45s", cue:"Pair with Bulgarian split squat; keep constant tension.", options:["Machine","Cable"]},
        {name:"Circuit 3 - Rope Triceps Pushdown", sets:3, reps:"12", rest:"30s", cue:"Pair with scaption raise and plank; elbows stay pinned."},
        {name:"Circuit 3 - Scaption Raise", sets:3, reps:"12-15", rest:"30s", cue:"Raise in the scapular plane; avoid shrugging."},
        {name:"Circuit 3 - Plank", sets:3, reps:"45-60s", rest:"30s", cue:"Ribs down, glutes tight, steady breathing."},
        {name:"Circuit 4 - Standing Calf Raises", sets:3, reps:"15-20", rest:"30s", cue:"2-3 rounds; pause at top and bottom."},
        {name:"Circuit 4 - Leg Curl", sets:3, reps:"12-15", rest:"30s", cue:"2-3 rounds; control the eccentric."},
        {name:"Circuit 4 - Farmer Carry", sets:3, reps:"40-60 yd", rest:"30s", cue:"2-3 rounds; tall posture, slow controlled steps.", options:["Yards","30-45 sec"]},
      ],
      conditioning:{label:"Session Target", rx:"60 minutes total including the 10-minute treadmill warm-up."}
    },'''

new_day_c = '''    {
      id:"d3", short:"Day 3 (C)", title:"Push + Quad Focus",
      muscleGroups:["Chest","Shoulders","Triceps","Quads","Glutes","Calves","Core","Carries"],
      mobility:[
        {name:"Treadmill warm-up", dose:"10 min", cue:"5 min brisk walk, then 5 min incline walk."},
      ],
      lifts:[
        {name:"Circuit 1 - Reverse Lunge", sets:3, reps:"10/leg", rest:"30-45s", cue:"Pair with incline dumbbell bench press; stay tall and control the step back."},
        {name:"Circuit 1 - Incline Dumbbell Bench Press", sets:3, reps:"10-12", rest:"30-45s", cue:"Pair with reverse lunges; keep shoulder blades set and press smoothly."},
        {name:"Circuit 2 - Step-Ups", sets:3, reps:"10/leg", rest:"30-45s", cue:"Pair with dumbbell fly; drive through the working leg and control the descent."},
        {name:"Circuit 2 - Dumbbell Fly", sets:3, reps:"12-15", rest:"30-45s", cue:"Pair with step-ups; use a controlled arc and stop before the shoulders roll forward."},
        {name:"Circuit 3 - Overhead Cable Triceps Extension", sets:3, reps:"12-15", rest:"30s", cue:"Ab room circuit; keep elbows pointed forward and ribs stacked."},
        {name:"Circuit 3 - Dumbbell Lateral Raise", sets:3, reps:"12-15", rest:"30s", cue:"Ab room circuit; raise with control and avoid shrugging."},
        {name:"Circuit 3 - Plank Shoulder Taps", sets:3, reps:"10-12/side", rest:"30s", cue:"Ab room circuit; keep hips square and minimize side-to-side movement."},
        {name:"Circuit 4 - Barbell Back Squat", sets:3, reps:"8-10", rest:"30-45s", cue:"Ab room circuit; brace before each rep and keep the bar path controlled."},
        {name:"Circuit 4 - Standing Calf Raises", sets:3, reps:"15-20", rest:"30s", cue:"Ab room circuit; pause at the top and bottom."},
        {name:"Circuit 4 - Suitcase Carry", sets:3, reps:"30-45 sec/side", rest:"30s", cue:"Ab room circuit; hold one dumbbell at your side, stay tall, and resist leaning."},
      ],
      conditioning:{label:"Session Target", rx:"60 minutes total including the 10-minute treadmill warm-up."}
    },'''

old_day_d = '''    {
      id:"d4", short:"Day 4 (B)", title:"Pull + Posterior Chain Focus",
      muscleGroups:["Back","Lats","Rear Delts","Biceps","Hamstrings","Glutes","Quads","Core"],
      mobility:[
        {name:"Treadmill warm-up", dose:"10 min", cue:"5 min brisk walk, then 5 min incline walk."},
      ],
      lifts:[
        {name:"Circuit 1 - Romanian Deadlift", sets:3, reps:"8-10", rest:"30-45s", cue:"Pair with lat pulldown; hinge with a neutral spine."},
        {name:"Circuit 1 - Lat Pulldown", sets:3, reps:"8-10", rest:"30-45s", cue:"Pair with Romanian deadlift; full stretch and strong pull."},
        {name:"Circuit 2 - Standing Cable Row", sets:3, reps:"10-12", rest:"30-45s", cue:"Pair with bodyweight hip thrust; pull to the ribs without leaning back."},
        {name:"Circuit 2 - Bodyweight Hip Thrust", sets:3, reps:"15-25", rest:"30-45s", cue:"Pair with standing cable row; pause at the top and finish each rep with the glutes, not the low back."},
        {name:"Circuit 3 - Face Pull", sets:3, reps:"15", rest:"30s", cue:"Pair with dumbbell shrugs and hanging knee raise; elbows high."},
        {name:"Circuit 3 - Dumbbell Shrugs", sets:3, reps:"12", rest:"30s", cue:"Lift straight up, pause briefly, avoid rolling the shoulders."},
        {name:"Circuit 3 - Hanging Knee Raise", sets:3, reps:"12", rest:"30s", cue:"Control the pelvis; avoid swinging."},
        {name:"Circuit 4 - Walking Lunges", sets:3, reps:"10/leg", rest:"30s", cue:"2-3 rounds; long stride and stable knee."},
        {name:"Circuit 4 - Dumbbell Reverse Fly", sets:3, reps:"12-15", rest:"30s", cue:"2-3 rounds; hinge slightly, lead with the elbows, and avoid shrugging."},
        {name:"Circuit 4 - Pallof Press", sets:3, reps:"12/side", rest:"30s", cue:"2-3 rounds; resist rotation and keep ribs stacked."},
      ],
      conditioning:{label:"Session Target", rx:"60 minutes total including the 10-minute treadmill warm-up."}
    }'''

new_day_d = '''    {
      id:"d4", short:"Day 4 (D)", title:"Pull + Posterior Chain Focus",
      muscleGroups:["Back","Lats","Rear Delts","Biceps","Hamstrings","Glutes","Core"],
      mobility:[
        {name:"Treadmill warm-up", dose:"10 min", cue:"5 min brisk walk, then 5 min incline walk."},
      ],
      lifts:[
        {name:"Circuit 1 - Single-Leg Dumbbell Romanian Deadlift", sets:3, reps:"10/leg", rest:"30-45s", cue:"Main gym; hinge over the working leg with the hips square and a neutral spine."},
        {name:"Circuit 1 - Neutral-Grip Lat Pulldown", sets:3, reps:"10-12", rest:"30-45s", cue:"Main gym; pull the elbows down toward the ribs and control the stretch."},
        {name:"Circuit 2 - Three-Point Dumbbell Row", sets:3, reps:"10-12/side", rest:"30-45s", cue:"Main gym; brace with one hand, keep the torso stable, and pull toward the hip."},
        {name:"Circuit 2 - Weighted Hip Thrust", sets:3, reps:"10-15", rest:"30-45s", cue:"Main gym; pause at the top and finish with the glutes without overextending the low back."},
        {name:"Circuit 2 - Dumbbell Reverse Fly", sets:3, reps:"12-15", rest:"30-45s", cue:"Main gym; hinge slightly, lead with the elbows, and avoid shrugging."},
        {name:"Circuit 3 - Dumbbell Hammer Curl", sets:3, reps:"10-12", rest:"30s", cue:"Ab room circuit; keep the upper arms quiet and use a neutral grip."},
        {name:"Circuit 3 - Face Pull", sets:3, reps:"12-15", rest:"30s", cue:"Ab room circuit; pull toward the face with elbows high and control the return."},
        {name:"Circuit 3 - Side Plank", sets:3, reps:"30-45 sec/side", rest:"30s", cue:"Ab room circuit; keep hips stacked and maintain a straight line from head to feet."},
        {name:"Circuit 4 - Exercise-Ball Leg Curl", sets:3, reps:"12-15", rest:"30s", cue:"Ab room circuit; keep hips lifted as you curl the ball toward you."},
        {name:"Circuit 4 - Cable Chop", sets:3, reps:"10-12/side", rest:"30s", cue:"Ab room circuit; use a controlled high-to-low diagonal pull and rotate smoothly."},
        {name:"Circuit 4 - Russian Twist", sets:3, reps:"16-24 total", rest:"30s", cue:"Ab room circuit; rotate under control rather than swinging the weight."},
      ],
      conditioning:{label:"Session Target", rx:"60 minutes total including the 10-minute treadmill warm-up."}
    }'''

if old_day_c in text:
    text = text.replace(old_day_c, new_day_c, 1)
elif new_day_c not in text:
    raise SystemExit("Could not find the expected Day 3 block")

if old_day_d in text:
    text = text.replace(old_day_d, new_day_d, 1)
elif new_day_d not in text:
    raise SystemExit("Could not find the expected Day 4 block")

# Day D keeps the same dumbbell reverse-fly movement, but it moves from
# Circuit 4 to Circuit 2. Migrate that history only for d4.
helper = '''  function migrateDayDReverseFlyHistory(stateObj){
    if(!stateObj || !stateObj.sessions) return false;
    let changed = false;
    Object.values(stateObj.sessions).forEach(weekSessions => {
      const session = weekSessions && weekSessions.d4;
      if(!session) return;
      const oldName = "Circuit 4 - Dumbbell Reverse Fly";
      const newName = "Circuit 2 - Dumbbell Reverse Fly";
      ["liftSets", "extraSets", "restOverrides"].forEach(bucket => {
        if(remapStorageKey(session[bucket], oldName, newName)) changed = true;
      });
    });
    return changed;
  }

'''

fn_anchor = '  function migrateLegacyLiftNames(stateObj){\n'
if 'function migrateDayDReverseFlyHistory' not in text:
    if fn_anchor not in text:
        raise SystemExit("Could not find the migration-function anchor")
    text = text.replace(fn_anchor, helper + fn_anchor, 1)

local_anchor = '  if(migrateDayABenchPressHistory(state)){\n    save(state);\n  }\n'
local_call = '  if(migrateDayDReverseFlyHistory(state)){\n    save(state);\n  }\n'
if local_call not in text:
    if local_anchor not in text:
        raise SystemExit("Could not find the local migration-call anchor")
    text = text.replace(local_anchor, local_anchor + local_call, 1)

remote_old = '        if(migrateLegacyLiftNames(state) || migrateDayABenchPressHistory(state) || migrateMetricsVersion(state)){\n'
remote_new = '        if(migrateLegacyLiftNames(state) || migrateDayABenchPressHistory(state) || migrateDayDReverseFlyHistory(state) || migrateMetricsVersion(state)){\n'
if remote_old in text:
    text = text.replace(remote_old, remote_new, 1)
elif remote_new not in text:
    raise SystemExit("Could not find the remote migration-call anchor")

path.write_text(text, encoding="utf-8")
