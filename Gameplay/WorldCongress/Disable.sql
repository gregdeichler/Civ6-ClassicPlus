DELETE FROM GameCapabilityDependencies
WHERE GameCapability IN ('CAPABILITY_WORLD_CONGRESS', 'CAPABILITY_EMERGENCIES')
   OR DependsOnCapability IN ('CAPABILITY_WORLD_CONGRESS', 'CAPABILITY_EMERGENCIES');

DELETE FROM GameCapabilities
WHERE GameCapability IN ('CAPABILITY_WORLD_CONGRESS', 'CAPABILITY_EMERGENCIES');

-- The second guard delays normal sessions past the last stock era even if
-- a UI or engine path ignores the capability. It does not change world eras.
UPDATE GlobalParameters SET Value = 200 WHERE Name = 'WORLD_CONGRESS_INITIAL_ERA';

UPDATE Victories SET EnabledByDefault = 0 WHERE VictoryType = 'VICTORY_DIPLOMATIC';

-- Keep the engine's favor records, but remove stock sources and penalties
-- with verified parameters. Do not zero divisor or cost parameters.
UPDATE GlobalParameters SET Value = 0
WHERE Name IN (
    'WORLD_CONGRESS_ALLIANCE_FAVOR_PER_TURN',
    'WORLD_CONGRESS_BASELINE_FAVOR_PER_TURN',
    'WORLD_CONGRESS_SUZERAIN_FAVOR_PER_TURN',
    'WORLD_CONGRESS_TRADE_PARTNER_FAVOR_PER_TURN',
    'FAVOR_FOR_LIBERATE_CITY_STATE',
    'FAVOR_FOR_LIBERATE_PLAYER_CITY',
    'FAVOR_FOR_REVIVE_PLAYER',
    'FAVOR_PER_OWNED_ORIGINAL_CAPITAL',
    'FAVOR_CO2_MINIMUM',
    'FAVOR_GRIEVANCES_MINIMUM'
);

DELETE FROM GoodyHutSubTypes WHERE SubTypeGoodyHut = 'GOODYHUT_FAVOR';

-- Neutralize the stock additive rewards without deleting the modifier records
-- their buildings, projects and future civics reference. Leave science victory alone.
UPDATE ModifierArguments SET Value = '0'
WHERE Name = 'Amount' AND ModifierId IN (
    SELECT ModifierId FROM Modifiers
    WHERE ModifierType IN (
        'MODIFIER_PLAYER_ADD_FAVOR',
        'MODIFIER_PLAYER_ADJUST_EXTRA_FAVOR_PER_TURN',
        'MODIFIER_PLAYER_CITIES_ADJUST_EXTRA_FAVOR_PER_TURN',
        'MODIFIER_PLAYER_ADJUST_FAVOR_FROM_DELEGATIONS',
        'MODIFIER_PLAYER_ADJUST_FAVOR_FROM_EMBASSIES',
        'MODIFIER_PLAYER_ADJUST_DIPLOMATIC_VICTORY_POINTS'
    )
    AND ModifierId NOT IN ('GOVCITYSTATES_ADJUST_FAVOR', 'PAGODA_ADJUST_FAVOR')
);

-- These existing buildings can use the same passive influence effect as
-- the Consulate. Hungary's wonder keeps a diplomatic benefit for its owner.
UPDATE Modifiers SET ModifierType = 'MODIFIER_PLAYER_ADJUST_INFLUENCE_POINTS_PER_TURN'
WHERE ModifierId IN ('GOVCITYSTATES_ADJUST_FAVOR', 'PAGODA_ADJUST_FAVOR', 'ORSZAGHAZ_DOUBLE_FAVOR_SUZERAIN');

UPDATE ModifierArguments SET Value = CASE ModifierId
    WHEN 'GOVCITYSTATES_ADJUST_FAVOR' THEN '2'
    WHEN 'PAGODA_ADJUST_FAVOR' THEN '1'
    WHEN 'ORSZAGHAZ_DOUBLE_FAVOR_SUZERAIN' THEN '3'
END
WHERE Name = 'Amount'
  AND ModifierId IN ('GOVCITYSTATES_ADJUST_FAVOR', 'PAGODA_ADJUST_FAVOR', 'ORSZAGHAZ_DOUBLE_FAVOR_SUZERAIN');

-- The promise requests otherwise require 30 favor and become unaffordable.
-- Keep the promise types and their grievance consequences.
UPDATE DiplomaticActions_XP2 SET FavorCost = 0
WHERE PromiseType IS NOT NULL AND FavorCost > 0;
