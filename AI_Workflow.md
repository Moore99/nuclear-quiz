# AI_WORKFLOW.md
Unified AI Development Workflow for the nuclear_quiz Repository

## Overview
This document defines how AI tools (Claude Code, Cline, Continue.dev) should be used when developing the nuclear_quiz project. It standardizes prompts, workflows, branching strategy, and the long-term feature roadmap across Web, Android, and iOS. The goal is to ensure safe, consistent, maintainable AI-assisted development in a multi-platform codebase that has been modified by multiple AIs over time.

## Project Structure
The repository includes:
- Web app deployed at quiz.nuclear-motd.com
- Flutter Android app (most heavily modified by AI)
- Flutter iOS app (must meet Apple App Store requirements)
- Shared backend database used by all platforms
- Historical context files such as Claude.md, memory.md, and other .md documents

The codebase contains drift, inconsistent patterns, and partial implementations due to multiple AI contributors. All AI tools must account for this.

## Prompts

### Claude Code Prompt (Architect & Reviewer)
Use this when you want repo-wide reasoning, architecture analysis, or multi-platform planning.

CLAUDE_CODE_PROMPT:
You are assisting with ongoing development of the multi-platform project nuclear_quiz, which includes:
- A web app deployed at quiz.nuclear-motd.com
- A Flutter Android app
- A Flutter iOS app
All share the same backend database.

The repository has been modified by multiple AIs. Expect drift, inconsistencies, and partial implementations. You have full repo access.

Before proposing changes, review:
- Claude.md
- memory.md
- Any other .md files containing historical context

Current priorities:
1. Implement user account deletion across Web, Android, and iOS.
2. Fix the Web admin navbar bug where admin users cannot see the admin endpoint.
3. Identify and correct cross-platform drift.
4. Establish testing workflows for Web (Docker), Android (Android Studio), and iOS (Xcode/Flutter).

Additional features to support:
- Admin password reset
- User password reset flow
- AdMob integration
- Analytics instrumentation
- Database backup functions

Your role:
- Inspect the repository directly.
- Identify inconsistencies before proposing changes.
- Prefer diff-style patches, but full rewrites are allowed when necessary.
- Maintain database schema consistency.
- Provide platform-specific testing instructions.

Workflow:
1. Scan the repository and read all context files.
2. Identify the current state of account deletion logic.
3. Diagnose the admin navbar issue.
4. Identify drift across platforms.
5. Propose a unified plan.
6. Provide diffs or detailed instructions.
7. Provide testing instructions.

First task:
Summarize the current state of account deletion, the admin navbar issue, and cross-platform drift. Then propose a prioritized plan.


### Cline Prompt (Executor & Agent)
Use this when you want step-by-step execution, file edits, or terminal commands.

CLINE_PROMPT:
You are assisting with the nuclear_quiz repository. Your job is to execute tasks safely using step-by-step reasoning, minimal diffs, and verification. Use concise reasoning to reduce token usage.

You must:
- Read and understand the repository before making changes.
- Follow a plan before editing files.
- Use minimal diffs unless a full rewrite is approved.
- Confirm assumptions before acting.
- Avoid destructive changes.
- Run commands only when necessary.

Project context:
- Web app (quiz.nuclear-motd.com)
- Flutter Android app
- Flutter iOS app
All share the same backend database.

Reference materials:
- Claude.md
- memory.md
- Other .md context files

Current priorities:
1. Implement user account deletion across all platforms.
2. Fix the Web admin navbar bug.
3. Identify and correct cross-platform drift.
4. Establish testing workflows.

Additional features:
- Admin password reset
- User password reset
- AdMob integration
- Analytics
- Database backups

Workflow:
1. Inspect the repository.
2. Read context files.
3. Summarize understanding.
4. Propose a step-by-step plan.
5. Wait for approval.
6. Execute using minimal diffs.
7. Verify each change.
8. Provide testing instructions.

First task:
Inspect the repository, summarize the current state of account deletion, the admin navbar issue, and drift. Propose a safe plan.


### Continue.dev Prompt (Inline Editor)
Use this for small, local edits and inline completions.

CONTINUE_PROMPT:
You are assisting with incremental improvements to the nuclear_quiz repository. Focus on small, localized edits and inline completions.

Context:
- Web app
- Flutter Android app
- Flutter iOS app
All share the same backend database.

Reference:
- Claude.md
- memory.md
- Other .md files

Do:
- Provide concise inline completions.
- Suggest small, safe edits.
- Maintain API and schema consistency.
- Produce minimal code snippets.

Do not:
- Perform multi-file refactors.
- Rewrite entire components unless asked.
- Run commands or behave agentically.

Primary use cases:
- Fixing small bugs
- Improving readability
- Adding imports
- Completing functions
- Minor UI adjustments

Wait for the user to highlight code before acting.

## Model Selection
| Task | Tool | Model |
|------|------|--------|
| Repo-wide reasoning | Claude Code | Claude 3.5 Sonnet |
| Multi-file refactors | Claude Code → Cline | Claude for plan, GLM5 Pro for execution |
| File edits | Cline | GLM5 Pro |
| Terminal commands | Cline | GLM5 Pro |
| Small code fixes | Continue.dev | GLM5 Lite |
| UI tweaks | Continue.dev | GLM5 Lite |
| Backend endpoint creation | Cline | GLM5 Pro |
| Reviewing diffs | Claude Code | Claude 3.5 Sonnet |
| Debugging builds | Cline | GLM5 Pro |

## Testing Workflow

### Web (Docker)
- docker build -t nuclear_quiz_web .
- docker run -p 8080:8080 nuclear_quiz_web
- Test login, admin navbar, account deletion, password reset, API compatibility.

### Android (Android Studio — Compose Multiplatform, NOT Flutter)
- Open `android/` folder in Android Studio
- Gradle sync (automatic)
- Run on emulator or physical device
- Test login, account deletion, password change, API calls.
- Note: there is no `flutter` command. This is Kotlin/CMP.

### iOS (Xcode — Compose Multiplatform, NOT Flutter)
- cd android && ./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64
- Open android/iosApp/iosApp.xcodeproj in Xcode
- Run on simulator or device
- Test account deletion (Apple App Store requirement), password change, API compatibility.

### Cross-platform API validation
Use a shared Postman collection to test all endpoints from all platforms.

## Git Branching Strategy

### Branch Types
- main — production
- develop — integration
- feature/<name> — one feature
- fix/<name> — one bug
- ai/claude/<task> — Claude Code planning
- ai/cline/<task> — Cline implementation

### Workflow
1. Claude Code produces a plan in ai/claude/...  
2. Cline implements in ai/cline/...  
3. Continue.dev handles small fixes  
4. Merge into develop after human review  
5. Merge into main after full testing  

## Long-Term Roadmap

### Account Deletion
- Backend DELETE /user/{id}
- Auth required
- Cascade delete or anonymize
- UI for Web, Android, iOS
- Apple-compliant UX

### Password Reset
- Admin reset
- User reset flow
- Email token system
- Token expiration
- Backend endpoints

### AdMob Integration
- Android: SDK + placements
- iOS: SDK + Info.plist
- Test ads during development

### Analytics
- Firebase recommended
- Track quiz events, account deletion, password reset
- Web + mobile integration

### Database Backups
- Nightly backups
- On-demand admin backup
- Secure storage
- Optional encryption
- Admin UI for triggering backups

### Additional Improvements
- Centralize API client code
- Standardize error handling
- Improve logging
- Add rate limiting
- Add monitoring
- Add automated tests
- Add CI/CD for Docker + Flutter