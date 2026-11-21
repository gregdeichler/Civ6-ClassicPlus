# Testing Classic+ M1

## Evidence

The ZIP was checked against the modinfo, and its XML parsed. All six SQL files were applied in manifest order to in-memory copies of the [pinned debug databases](https://github.com/nuanyuqingfeng/civ6-modding-skills/tree/e618aad0dea24af91ecd38d8b2300f8c1daff695/skills/civ6-modding/database) with foreign keys enabled. The checks cover affected capabilities and diplomatic victory, unchanged selectable content and unrelated victories, and preserved eras, diplomacy, governors and strategic-resource rows. This is database evidence only. **The new 0.2 build has not yet been verified in the engine. AI, UI, and save tests remain pending.**

### 2026-11-20 load failure and local fix

The Windows/Proton game logs identified an invalid reference from `Modifiers.SubjectRequirementSetId` to `PLAYER_HAS_POLITICAL_PHILOSOPHY`, followed by gameplay validation failure and rollback. That stock requirement set is defined by the optional Macedonia/Persia DLC. Mansa Musa's replacement trade route now uses Classic+'s own civic requirement and requirement set. The logs also reported an unhandled manifest criterion; the manifest now uses `GameCoreInUse=Expansion2`, matching the installed Gathering Storm manifest, with criteria attributes on the actions.

`Tools/validate.py` now also removes the optional Persia requirement set from a disposable database copy, clearing its stock references, then applies all gameplay SQL. The original leader SQL reproduced the foreign-key failure in that fixture. The patched SQL passes both the full snapshot and the missing-rule fixture, including the requirement's link to Political Philosophy and all existing preservation checks. This fixture checks the missing rule, not a complete reconstruction of every possible DLC combination. `Tools/build.py` also rejects the unsupported criterion and checks the action guards. No live game databases or game installation files are modified by these checks.

To repeat with your own game files, start a new Gathering Storm game without Classic+ or other community mods, exit, and use the databases in the user data folder's `Cache`:

```sh
python3 Tools/build.py
python3 Tools/validate.py "/path/to/Cache/DebugConfiguration.sqlite" "/path/to/Cache/DebugGameplay.sqlite"
```

## 0.2 grievance and flooding evidence (2026-11-21)

The full manifest passes against the pinned clean databases, including the existing missing-Persia-rule regression. The two new SQL modules also pass on a disposable in-memory copy of the user's current Windows/Proton gameplay cache, with no added foreign-key errors. The validator checks war/capture/raze and promise grievance costs, source globals, the major/minor generation guard, AI grievance valuation, relationship-penalty coefficients, every standard disaster intensity, and coastal-lowland generation. It verifies that diplomatic prerequisites and state transitions, leaders, civilizations, eras, floodplain terrain, dams/power data, non-flood event frequencies/damage/yields, and non-diplomatic victories remain unchanged. Package contents match the manifest. These are SQL/data checks, not successful gameplay evidence.

## In-game smoke test (pending)

For the new engine checks, create a fresh generated Gathering Storm map, disable optional modes and other rules mods, and choose disaster intensity 4. Check that coastal tiles are not marked vulnerable. Declare a surprise war, capture/raze a city, conquer a city-state, denounce a leader, refuse a promise, and break a promise; verify the grievance ledger and grievance-based relationship penalties remain zero for both human and AI actors. Verify trade, peace, friendships, alliances, and other leader agenda reactions still work. Advance enough turns to check that river floods and coastal flooding do not occur while other disasters can still occur. Test save/reload separately. Imported maps, optional modes, and old saves remain outside this baseline.

1. Install the ZIP using the [README](../README.md). Enable Classic+ and owned official DLC only. Create a fresh Gathering Storm game with no optional modes. In Advanced Setup, confirm the Diplomatic Victory checkbox is absent and the other victories remain. Confirm you can select a base leader and leaders from the expansion, New Frontier and Leader Pass packs you own.
2. Start in Ancient on Online speed, take several AI turns, save, exit to the main menu, reload, and take another turn. Confirm the chronological era indicator remains, the age-score control is absent, and city loyalty and governor controls work.
3. Advance through the first world-era change. Verify the era advances, no dedication prompt or historic moment prevents ending the turn, and cities use normal loyalty pressure. Check policy selection, tech and civic progression, production and the historic timeline shortcut.
4. Continue through the Medieval era and past the first regular Congress window. In a second game use a Medieval start for a shorter independent check. Verify no Congress vote, special session, or emergency blocks turns. Inspect diplomacy, peace, alliances, trades and promise requests after meeting other civs. Verify the ranking UI does not allow a diplomatic victory and normal victory paths remain.
5. Use a small map or hotseat test to verify representative changed abilities: Mansa Musa's route at Political Philosophy; Magnificent Suleiman's yields and combat preview; Georgia's Tsikhe yields after Conservation; Lautaro's Free City strength and loyalty loss; America's influence points; Canada’s city-state trade yield; Sweden's Great Person generation and Kristina's theming. Check at least one unaffected expansion leader and one Leader Pass persona.
6. In `Logs` beside the user data folders, inspect `Modding.log` for ClassicPlus action dispatch and `Database.log` for errors. Inspect `Lua.log` if available for ActionPanel/PartialScreenHooks errors. Preserve the game version, platform, DLC and mod list, seed, failing turn, save, and exact log lines for a reproducible issue.
