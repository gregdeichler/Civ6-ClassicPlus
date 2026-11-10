# Classic+ contributor instructions

Keep the Gathering Storm roster and unique content while removing the six systems in the roadmap. Preserve loyalty, ordinary eras and diplomacy, disasters, and non-diplomatic victories. Existing DLC ownership and asset loading stay with the game; never bundle Firaxis files or edit the game installation.

Keep frontend configuration, gameplay SQL, UI wrappers, and localization separate. Prefer targeted row updates and existing engine effects. Add Lua only where data cannot control the behavior. Use the Gathering Storm action criterion for ruleset-specific code, stable mod and action IDs, and explicit load order. Keep stock records that the engine or another retained system may reference. Use the [architecture notes](docs/architecture.md) for sources and [known limitations](docs/known-limitations.md) for engine assumptions.

Run `python3 Tools/build.py` to check the manifest and create the install ZIP; install using the [README](README.md). Run `python3 Tools/validate.py CONFIG_DB GAMEPLAY_DB` against clean Gathering Storm debug databases. Rebuild the roster audit with `python3 Tools/audit.py CONFIG_DB GAMEPLAY_DB` when supported DLC changes. Keep debug databases, logs, and packages out of Git.

Use focused branches and draft milestone PRs; do not push to main. Each PR states player-facing behavior, test evidence, unverified areas, limitations, and install or upgrade steps. A system is done when the database changes, affected abilities and UI, and AI/player behavior have been verified in game. Record engine-limited approximations explicitly and keep manual test results distinct from SQLite checks.
