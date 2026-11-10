# Known limitations

**M1 is an unverified in-game preview.** Database postconditions passed against a Gathering Storm snapshot. First launch, era transitions, the Medieval Congress boundary, DLC combinations, AI play, and save/reload need engine verification. Stock game modes and multiplayer are outside the initial test baseline. Dramatic Ages is suppressed in setup because it deliberately reintroduces ages; leave it off in any imported configuration.

The game may still have hard-coded or ungated entry points: the historian keyboard shortcut, stale age or Favor descriptions, Favor deal widgets, and the diplomacy ranking tab are smoke-test targets. Congress capabilities and its regular start era are changed in gameplay, rather than just hiding its button. The Favor database type, engine trade code, and dormant catalog entries remain. Some alternate reward text (e.g. Monarchy, future civics, Carbon Recapture, and former diplomatic-victory wonders) still needs a pass. Congress-dependent competitions and emergencies are intentionally excluded from this preview. The effects of the free promise requests on AI valuation are unverified. Dark Age cards remain defined and should be inaccessible; check the policy and Civilopedia screens after an era transition.

Classic+ still uses governors, strategic stockpiles, electricity, and grievances. In particular:

- A governor capability exists. The data audit found Seondeok, original Suleiman and Mapuche dependencies; title rewards, loyalty pressure, governors granted by modes, and AI allocation need a separate pass.
- `Units.StrategicResource` and `Units_XP2.ResourceCost` / maintenance columns coexist. Their presence does not prove the original resource-access rule runs under Gathering Storm. A change to production, purchase, or upgrade costs needs in-game tests with both zero access and an improved source, including AI behavior. No resource costs were changed.
- `Buildings_XP2` exposes power demand, fuel and powered amenities; `Building_YieldChangesBonusWithPower` holds conditional yields. Power also touches regional yields, fuel improvements, disasters and emissions, so converting those two tables alone is insufficient.
- `DiplomaticActions_XP2` exposes several grievance sources, but the original warmonger behavior is not known to be restorable in this core. Do not hide grievance UI until generation and AI relationship effects have been tested.

English descriptions are updated selectively. Other locales retain stock descriptions. UI mods replacing ActionPanel or PartialScreenHooks, or rules mods writing the same capabilities, traits, or victory setup, can conflict. Existing saves and other rulesets are unsupported.
