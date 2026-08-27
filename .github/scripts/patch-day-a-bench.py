from pathlib import Path

path = Path("strength-circuit-2-day.html")
text = path.read_text(encoding="utf-8")

old_lift = '        {name:"Circuit 2 - Machine/Cable Chest Press", sets:3, reps:"10-12", rest:"30-45s", cue:"Pair with Bulgarian split squat; keep constant tension.", options:["Machine","Cable"]},'
new_lift = '        {name:"Circuit 2 - Bench/Cable Chest Press", sets:3, reps:"10-12", rest:"30-45s", cue:"Pair with Bulgarian split squat; press smoothly through a controlled range.", options:["Bench Press","Cable"], cues:{"Bench Press":"Pair with Bulgarian split squat; keep shoulder blades set, feet planted, and press smoothly.", "Cable":"Pair with Bulgarian split squat; keep constant tension through the full range."}},'

count = text.count(old_lift)
if count != 2:
    raise SystemExit(f"Expected 2 Machine/Cable Chest Press definitions, found {count}")

# Change Day 1 (A) only. Day 3 will be rebuilt separately as Day C.
text = text.replace(old_lift, new_lift, 1)

helper = '''  function migrateDayABenchPressHistory(stateObj){
    if(!stateObj || !stateObj.sessions) return false;
    let changed = false;
    Object.values(stateObj.sessions).forEach(weekSessions => {
      const session = weekSessions && weekSessions.d1;
      if(!session) return;
      const oldName = "Circuit 2 - Machine/Cable Chest Press";
      const newName = "Circuit 2 - Bench/Cable Chest Press";
      const oldCable = `${oldName}::Cable`;
      const newCable = `${newName}::Cable`;
      ["liftSets", "extraSets", "restOverrides"].forEach(bucket => {
        const obj = session[bucket];
        if(!obj || !Object.prototype.hasOwnProperty.call(obj, oldCable)) return;
        if(!Object.prototype.hasOwnProperty.call(obj, newCable)) obj[newCable] = obj[oldCable];
        delete obj[oldCable];
        changed = true;
      });
      if(session.liftOptions){
        const oldOptKey = `d1::${oldName}`;
        const newOptKey = `d1::${newName}`;
        if(Object.prototype.hasOwnProperty.call(session.liftOptions, oldOptKey)){
          const oldOpt = session.liftOptions[oldOptKey];
          if(oldOpt === "Cable" && !Object.prototype.hasOwnProperty.call(session.liftOptions, newOptKey)){
            session.liftOptions[newOptKey] = "Cable";
          }
          delete session.liftOptions[oldOptKey];
          changed = true;
        }
      }
    });
    return changed;
  }

'''

fn_anchor = '  function migrateLegacyLiftNames(stateObj){\n'
if 'function migrateDayABenchPressHistory' not in text:
    if fn_anchor not in text:
        raise SystemExit("Could not find migration function anchor")
    text = text.replace(fn_anchor, helper + fn_anchor, 1)

local_anchor = '  if(migrateLegacyLiftNames(state)){\n    save(state);\n  }\n'
local_call = '  if(migrateDayABenchPressHistory(state)){\n    save(state);\n  }\n'
if local_call not in text:
    if local_anchor not in text:
        raise SystemExit("Could not find local migration call anchor")
    text = text.replace(local_anchor, local_anchor + local_call, 1)

remote_anchor = '        if(migrateLegacyLiftNames(state) || migrateMetricsVersion(state)){\n          save(state);\n        }\n'
remote_repl = '        if(migrateLegacyLiftNames(state) || migrateDayABenchPressHistory(state) || migrateMetricsVersion(state)){\n          save(state);\n        }\n'
if remote_anchor in text:
    text = text.replace(remote_anchor, remote_repl, 1)
elif remote_repl not in text:
    raise SystemExit("Could not find remote migration call anchor")

path.write_text(text, encoding="utf-8")
