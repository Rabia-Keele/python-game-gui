# Dodge the Blocks (Tkinter)

A tiny Python GUI game built with the standard library (`tkinter`). Your task is to **show good Git/GitHub practice** while evolving this repo.

## How to run
```bash
python game.py
```
Use Left/Right arrows to move. Avoid the falling blocks. Press Space to restart.

> Tkinter ships with Python on Windows/macOS/Linux. No extra packages required.

---

## Suggested Git plan (what markers want to see)

1. **Initial commit**  
   - `README.md`, `.gitignore`, and a skeleton `game.py` that prints "Hello game".

2. **Branch:** `feature/gui`  
   - Add the Tkinter window and a static player rectangle.  
   - Commit small steps: create window → draw player → handle keyboard.

3. **Branch:** `feature/blocks` (branch off `feature/gui`)  
   - Implement falling blocks + spawn timer.  
   - Open a PR into `feature/gui`, then merge.

4. **Branch:** `feature/scoring` (from `main`)  
   - Add score, best score, and HUD.  
   - Merge into `main` via PR.

5. **Branch:** `bugfix/collision-edge`  
   - Tweak collision box or wall clamping if needed.  
   - Reference the issue number in the commit message.

6. **Tag a release**  
   - `v1.0.0` after merging features. Attach a short release note.

> Keep commits **small and frequent**. Write clear messages like:  
> `feat(gui): add canvas and player rect`  
> `feat(blocks): spawn with random speeds`  
> `fix(collision): clamp player at walls`

---

## Example commit message format

```
<type>(<scope>): <short summary>

Body (why + what changed). Reference issues/PRs.
```

Common types: `feat`, `fix`, `docs`, `refactor`, `style`, `test`, `chore`.

---

## Branching & merging tips

- Protect `main`. Merge through Pull Requests.
- Use GitHub Issues for TODOs and link them in commits/PRs.
- Resolve a tiny conflict on purpose (e.g., edit the same line in `README.md` on two branches) to **demonstrate** merge skills.
- Add a screenshot to the README in a later commit (after the game runs).

---

## Commands cheat‑sheet (local → GitHub)

### Start locally
```bash
git init
git config user.name "Your Name"
git config user.email "your.keele.email@keele.ac.uk"   # IMPORTANT
git add .
git commit -m "chore: bootstrap project"
```

### Create GitHub repo and push
```bash
# Create empty public repo on GitHub first (no README)
git branch -M main
git remote add origin https://github.com/<your-username>/dodge-the-blocks.git
git push -u origin main
```

### Work on a feature branch
```bash
git checkout -b feature/gui
# edit code...
git add game.py
git commit -m "feat(gui): create window and draw player"
git push -u origin feature/gui
# Open PR on GitHub and merge
```

### Tag a release
```bash
git tag v1.0.0 -m "First playable release"
git push origin v1.0.0
```

---

## Marking checklist mapping

- ✅ Regular, meaningful commits
- ✅ Branching workflow with at least 2 feature branches and 1 bugfix branch
- ✅ Pull Requests & merges (with at least one conflict resolved)
- ✅ Tagged release
- ✅ Clear README

Good luck!
