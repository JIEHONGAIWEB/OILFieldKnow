---
name: wpo-project-setup
description: 'Scaffold a new WPO (Well Performance Optimization) working copy under C:\Users\h22231\code\EEE-WPO. Creates a timestamped folder named wpo-new-YYYYMMDD-HHMMSS, clones the wpo-app repo on the dev branch, and runs a forced npm install. Use this whenever the user asks to set up/clone/新建 a new WPO project folder, start a fresh wpo-app checkout, or wants a clean dev-branch working copy with dependencies installed. Trigger on phrases like "新建 wpo 项目", "clone wpo-app", "set up a new WPO folder", "拉一份新的 wpo-app dev 分支".'
---
 
# WPO Project Setup
 
## What This Skill Produces
 
A brand-new, timestamped project folder containing a fresh `dev`-branch clone of
`wpo-app`, with `npm install --force` already run, ready to open in an editor.
 
## When To Use
 
- User asks to create/clone/set up a new WPO (well-performance-optimization) working copy.
- User wants a fresh `dev` branch checkout without touching an existing folder.
- User explicitly names the `wpo-new-<timestamp>` naming convention or the
  `EEE-WPO` base directory.
## Required Inputs (all optional — sane defaults below)
 
- **Base directory** (default: `C:\Users\h22231\code\EEE-WPO`)
- **Repo URL** (default: the org's `wpo-app` SSH remote, see script)
- **Branch** (default: `dev`)
- **npm install flag** (default: `--force`, matches team convention)
## Procedure
 
1. Run [setup script](./scripts/setup-wpo-project.ps1) in PowerShell:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\setup-wpo-project.ps1
   ```
   Optional overrides:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\setup-wpo-project.ps1 `
     -BaseDir "C:\Users\h224847\code\EEE-WPO" `
     -RepoUrl "git@gitlab.com:ds365ai/DFSDEV/apps/01-well-performance-optimization/source/wpo-app.git" `
     -Branch "dev" `
     -NpmFlag "--force"
   ```
2. The script will, in order:
   - Verify the base directory exists (create it if missing).
   - Generate a new folder name: `wpo-new-<yyyyMMdd-HHmmss>`.
   - `cd` into the base directory and create the new folder.
   - Run `git clone <RepoUrl> -b <Branch>` inside it.
   - `cd` into the cloned repo directory.
   - Run `npm i <NpmFlag>`.
3. Report back to the user:
   - Full path of the new folder.
   - Clone result (success/failure, HEAD commit if available).
   - npm install result (success/failure, and a tail of any errors).
4. If any step fails, **stop** and surface the exact error — do not continue to
   the next step (e.g. don't run `npm i` if the clone failed).
## Notes on the Repo URL
 
The URL given by the user (`git@gitlab.com:ds365ai/DFSDEV/apps/01-well-performance-optimization/source/wpo-app.git`)
is missing the `:` that SSH-style git remotes require between host and path
(standard form is `git@host:path/to/repo.git`). The script defaults to the
corrected form:
```
git@gitlab.com:ds365ai/DFSDEV/apps/01-well-performance-optimization/source/wpo-app.git
```
If this guess is wrong, ask the user for the exact remote URL (from `git remote -v`
on an existing checkout, or from their git hosting UI) before running the script,
and pass it via `-RepoUrl`.
 
## Validation
 
- Report must state the exact new folder path created.
- Report must confirm both `git clone` and `npm i` exit codes.
- Final response clearly states `Setup complete: Yes/No`, and if `No`, which
  step failed and the fix needed.
## Example Prompts
 
- 在 EEE-WPO 下新建一个 wpo-new 时间戳文件夹，clone dev 分支并 npm i --force。
- Set up a new WPO working copy with today's timestamp and install dependencies.
- Clone a fresh wpo-app dev branch into a new timestamped folder.