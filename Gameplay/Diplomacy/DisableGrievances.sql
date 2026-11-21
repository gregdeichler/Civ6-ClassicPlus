-- Neutralize Gathering Storm's grievance accounting, keeping war, peace,
-- friendships, alliances, promises and trading available.
-- Use the stock percentage effect as a guard for engine-generated grievances.
INSERT INTO Modifiers (ModifierId, ModifierType)
VALUES ('CLASSICPLUS_NO_GRIEVANCE_GENERATION', 'MODIFIER_PLAYER_ADJUST_GRIEVANCE_MULTIPLIER');

INSERT INTO ModifierArguments (ModifierId, Name, Value)
VALUES ('CLASSICPLUS_NO_GRIEVANCE_GENERATION', 'Amount', '-100');

INSERT INTO TraitModifiers (TraitType, ModifierId)
SELECT TraitType, 'CLASSICPLUS_NO_GRIEVANCE_GENERATION'
FROM Traits WHERE TraitType IN ('TRAIT_LEADER_MAJOR_CIV', 'MINOR_CIV_DEFAULT_TRAIT');

-- These are source amounts and percentages, not divisors or turn intervals.
UPDATE GlobalParameters SET Value = 0
WHERE Name IN (
    'GRIEVANCE_MULTIPLIER_FOR_BROKEN_PROMISE',
    'GRIEVANCES_ALL_PLAYERS_CITY_STATE_CONQUEST',
    'GRIEVANCES_FOR_DENOUNCEMENT',
    'GRIEVANCES_HAVE_ENVOYS_CITY_STATE_DOW',
    'GRIEVANCES_POSSESS_CAPITAL_PER_TURN',
    'GRIEVANCES_POSSESS_NON_CAPITAL_PER_TURN',
    'GRIEVANCES_SUZERAIN_CITY_STATE_DOW',
    'SHARE_WAR_GRIEVANCES_ALLY',
    'SHARE_WAR_GRIEVANCES_DECLARED_FRIENDS',
    'SHARE_WAR_GRIEVANCES_DEFENSIVE_PERCENT'
);

-- Gathering Storm reuses these war/capture/raze multipliers for grievances.
-- Keep the action records, prerequisites and legal diplomatic transitions.
UPDATE DiplomaticActions
SET WarmongerPercent = 0, CaptureWarmongerPercent = 0, RazeWarmongerPercent = 0;

UPDATE DiplomaticActions_XP2
SET GrievanceCost = 0, GrievancesForRefusal = 0, GrievancesPerIncursion = 0;

-- Stop grievance totals, including third-party totals, affecting relationships.
-- Keep the stock modifiers and all their references valid.
UPDATE ModifierArguments SET Value = '0'
WHERE (ModifierId = 'STANDARD_DIPLOMATIC_WARMONGER'
       AND Name IN ('PercentOfGrievances', 'LowerLimit'))
   OR (ModifierId = 'STANDARD_DIPLOMATIC_THIRD_PARTY_WARMONGER'
       AND Name IN ('PercentOfGrievancesDelta', 'LowerLimit'));

UPDATE PseudoYields SET DefaultValue = 0
WHERE PseudoYieldType = 'PSEUDOYIELD_DIPLOMATIC_GRIEVANCE';

UPDATE AiFavoredItems SET Value = 0
WHERE Item = 'PSEUDOYIELD_DIPLOMATIC_GRIEVANCE';
