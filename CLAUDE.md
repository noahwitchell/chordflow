# ChordFlow (formerly FretFlow) — notes for Claude

- Owner: Noah. Goal: a true companion app for ear training / perfect pitch and for seeing
  how chords fit together to write music. Phone first (installed PWA), also works on desktop.
- No build step, no frameworks, no npm deps. ES modules served statically.
- Dev server: `.claude/launch.json` in ~/Claude has `chordflow` (python http.server 5181).
- Keep the chromatic colour map (C red … B rose) as the default: Noah trains associations on it.
- Tabs now: Clock, Grid, Ear (Wheel + Moves removed 2026-11-23, Noah only used three; they are in git history).
- Verify in the browser preview at phone size (375×812) and desktop before handing back.
- Commit after each meaningful change. Repo is PUBLIC (github.com/noahwitchell/chordflow) and served by
  GitHub Pages from main at https://noahwitchell.github.io/chordflow/ : pushing main = deploying. Bump
  CACHE in sw.js when shipping. Nothing secret goes in this repo.
- Icon: `python3 tools/make_icon.py && tools/render_icons.sh` (headless Chrome renders the PNGs).
- Ear data lives in localStorage `fretflow.ear.v1` (js/ear/log.js), app state in `fretflow.v2`.
- Renamed FretFlow → ChordFlow. Repo + Pages URL renamed to `chordflow` on 2026-11-23 (old
  /fretflow/ URL is dead). Local folder is ~/Claude/ChordFlow; localStorage keys still say `fretflow`; storage is
  per-origin (noahwitchell.github.io), so data carried over to the new path.
