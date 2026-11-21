# Civilization VI: Classic+

Classic+ aims to keep the civilizations, leaders, and unique content you own while simplifying the Gathering Storm rules. This **0.2.0 preview** disables Ages, World Congress, grievance generation and its relationship penalties, river floods, and coastal flooding/submersion. Ordinary diplomacy, trading, wars, alliances, and non-flood disasters remain. Governors, strategic resource stockpiles, and power still use Gathering Storm rules. Database checks pass; **the new rules need in-game verification**.

## Install

1. Use the current Civilization VI build with **Gathering Storm** installed and enabled. Enable any other owned DLC you want to play.
2. Extract the install ZIP so that `Mods/ClassicPlus/ClassicPlus.modinfo` exists. If working from this checkout, run `python3 Tools/build.py` to create `dist/ClassicPlus-0.2.0-preview.zip`.
3. In Civilization VI, enable **Classic+** under **Additional Content → Mods**. Start a **new** single-player game and choose the **Gathering Storm** ruleset. For the first run, leave optional game modes and other community mods off.

| Platform | User Mods folder |
| --- | --- |
| Windows | `Documents\My Games\Sid Meier's Civilization VI\Mods` (use the actual Documents location, including OneDrive if redirected) |
| macOS, Steam | `~/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Mods` on current installs; older installs can use the outer folder. Use the folder beside your active `Saves` directory. [Aspyr's path guide](https://support.aspyr.com/hc/en-us/articles/19003861040653-Game-Files-Missing-after-update-Civilization-VI-Mac-Steam) |
| macOS, Mac App Store | `~/Library/Containers/com.aspyr.civ6.appstore/Data/Library/Application Support/Sid Meier's Civilization VI/Mods`; Finder may display the container as “Civilization VI.” [Aspyr's Mac FAQ](https://support.aspyr.com/hc/en-us/articles/213487546-Civilization-VI-Mac-FAQ) |
| Linux, native Steam | `${XDG_DATA_HOME:-~/.local/share}/aspyr-media/Sid Meier's Civilization VI/Mods`. Proton uses the Windows Documents layout inside Steam's prefix for app 289070. |

Create `Mods` if needed. For an upgrade, quit the game and replace the old ClassicPlus folder so only one copy is installed. For removal, disable Classic+ and start a new game without it. Keep previous saves and the mod version that created them.

Use a newly generated map for the flooding changes: coastal vulnerability is assigned during map creation. This update does not restore submerged land or erase existing grievance history in old saves. Grievance-related panels may remain visible; this neutralizes the expansion's accounting and penalties rather than restoring the base game's warmonger rules. Flood-dependent bonuses no longer trigger; dams retain their other benefits. Custom maps, forced-disaster scripts, and optional modes need separate testing.

See [the smoke test](docs/testing.md), [leader compatibility](docs/compatibility-matrix.md), [known limitations](docs/known-limitations.md), and [the roadmap](docs/roadmap.md).
