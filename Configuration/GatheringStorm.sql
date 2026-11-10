-- Frontend database: only the Gathering Storm victory domain is affected.
UPDATE Victories
SET EnabledByDefault = 0, Visible = 0, ReadOnly = 1
WHERE Domain = 'Expansion2_Victories' AND VictoryType = 'VICTORY_DIPLOMATIC';

-- This optional mode explicitly reintroduces the systems Classic+ removes.
UPDATE Parameters SET DefaultValue = 0, Visible = 0, ReadOnly = 1
WHERE Key1 = 'Ruleset' AND Key2 = 'RULESET_EXPANSION_2'
  AND ConfigurationId = 'GAMEMODE_DRAMATICAGES';
