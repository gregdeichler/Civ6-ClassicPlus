# Testing Classic+ M1

## Evidence

The ZIP was checked against the modinfo, and its XML parsed. All four SQL files were applied in manifest order to in-memory copies of the [pinned debug databases](https://github.com/nuanyuqingfeng/civ6-modding-skills/tree/e618aad0dea24af91ecd38d8b2300f8c1daff695/skills/civ6-modding/database) with foreign keys enabled. The checks cover affected capabilities and diplomatic victory, unchanged selectable content and unrelated victories, and preserved eras, diplomacy, governors and strategic-resource rows. This is database evidence only. **No game, AI, UI, or save test has been run.**

To repeat with your own game files, start a new Gathering Storm game without Classic+ or other community mods, exit, and use the databases in the user data folder's `Cache`:

```sh
python3 Tools/build.py
python3 Tools/validate.py "/path/to/Cache/DebugConfiguration.sqlite" "/path/to/Cache/DebugGameplay.sqlite"
```

## In-game smoke test (pending)

1. Install the ZIP using the [README](../README.md). Enable Classic+ and owned official DLC only. Create a fresh Gathering Storm game with no optional modes. In Advanced Setup, confirm the Diplomatic Victory checkbox is absent and the other victories remain. Confirm you can select a base leader and leaders from the expansion, New Frontier and Leader Pass packs you own.
2. Start in Ancient on Online speed, take several AI turns, save, exit to the main menu, reload, and take another turn. Confirm the chronological era indicator remains, the age-score control is absent, and city loyalty and governor controls work.
3. Advance through the first world-era change. Verify the era advances, no dedication prompt or historic moment prevents ending the turn, and cities use normal loyalty pressure. Check policy selection, tech and civic progression, production and the historic timeline shortcut.
4. Continue through the Medieval era and past the first regular Congress window. In a second game use a Medieval start for a shorter independent check. Verify no Congress vote, special session, or emergency blocks turns. Inspect diplomacy, peace, alliances, trades and promise requests after meeting other civs. Verify the ranking UI does not allow a diplomatic victory and normal victory paths remain.
5. Use a small map or hotseat test to verify representative changed abilities: Mansa Musa's route at Political Philosophy; Magnificent Suleiman's yields and combat preview; Georgia's Tsikhe yields after Conservation; Lautaro's Free City strength and loyalty loss; America's influence points; Canada’s city-state trade yield; Sweden's Great Person generation and Kristina's theming. Check at least one unaffected expansion leader and one Leader Pass persona.
6. In `Logs` beside the user data folders, inspect `Modding.log` for ClassicPlus action dispatch and `Database.log` for errors. Inspect `Lua.log` if available for ActionPanel/PartialScreenHooks errors. Preserve the game version, platform, DLC and mod list, seed, failing turn, save, and exact log lines for a reproducible issue.
