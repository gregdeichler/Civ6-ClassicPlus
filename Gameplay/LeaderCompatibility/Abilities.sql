-- Georgia retains its wall production, Tamar's religion/envoy bonuses and
-- the Tsikhe's defense. Make half its age bonus permanent.
DELETE FROM TraitModifiers
WHERE TraitType = 'TRAIT_CIVILIZATION_GOLDEN_AGE_QUESTS'
  AND ModifierId = 'TRAIT_ALLOW_QUESTS_IN_GOLDEN_AGE';

UPDATE Modifiers SET SubjectRequirementSetId = NULL
WHERE ModifierId = 'TSIKHE_FAITH_GOLDEN_AGE';

UPDATE ModifierArguments SET Value = '2'
WHERE ModifierId = 'TSIKHE_FAITH_GOLDEN_AGE' AND Name = 'Amount';

DELETE FROM RequirementSetRequirements
WHERE RequirementSetId = 'DISTRICT_IS_CITY_CENTER_TSIKHE_GOLDEN_AGE'
  AND RequirementId = 'REQUIRES_PLAYER_HAS_GOLDEN_AGE';

UPDATE ModifierArguments SET Value = '1'
WHERE ModifierId = 'CONSERVATION_TSIKHE_TOURISM_GOLDEN_AGE' AND Name = 'Amount';

-- Lautaro's original Free City bonus and loyalty pressure remain.
DELETE FROM RequirementSetRequirements
WHERE RequirementSetId = 'OPPONENT_IS_IN_GOLDEN_AGE_FREE_CITY_REQUIREMENTS'
  AND RequirementId = 'OPPONENT_IS_IN_GOLDEN_AGE_REQUIREMENT';

-- Mansa Musa gains one route at Political Philosophy, using the existing
-- Persian unlock condition. His desert trade yields stay in place.
UPDATE Modifiers
SET ModifierType = 'MODIFIER_PLAYER_ADJUST_TRADE_ROUTE_CAPACITY',
    SubjectRequirementSetId = 'PLAYER_HAS_POLITICAL_PHILOSOPHY'
WHERE ModifierId = 'GOLDEN_AGE_TRADE_ROUTE';

-- Magnificent Suleiman gets smaller steady bonuses in place of the age cycle.
UPDATE Modifiers SET SubjectRequirementSetId = NULL
WHERE ModifierId IN ('TRAIT_SULEIMAN_ALT_SCIENCE_CULTURE_GOLDEN_AGE',
                     'SULEIMAN_ALT_COMBAT_ABILITY', 'SULEIMAN_COMBAT_BUFF');

UPDATE ModifierArguments SET Value = '5, 5'
WHERE ModifierId = 'TRAIT_SULEIMAN_ALT_SCIENCE_CULTURE_GOLDEN_AGE' AND Name = 'Amount';

UPDATE ModifierArguments SET Value = '2'
WHERE ModifierId = 'SULEIMAN_COMBAT_BUFF' AND Name = 'Amount';

-- Sweden retains the Factory and University Great Person bonuses and Kristina's
-- theming. Canada replaces favor with a trade bonus for peaceful engagement.
DELETE FROM TraitModifiers
WHERE (TraitType = 'TRAIT_CIVILIZATION_NOBEL_PRIZE' AND ModifierId = 'TRAIT_GREATPERSON_FAVOR_MODIFIER')
   OR (TraitType = 'TRAIT_CIVILIZATION_FACES_OF_PEACE' AND ModifierId = 'TRAIT_EMERGENCY_FAVOR_MODIFIER');

UPDATE Modifiers SET ModifierType = 'MODIFIER_PLAYER_ADJUST_TRADE_ROUTES_CITY_STATE_YIELD'
WHERE ModifierId = 'TRAIT_TOURISM_INTO_FAVOR';

DELETE FROM ModifierArguments WHERE ModifierId = 'TRAIT_TOURISM_INTO_FAVOR';
INSERT INTO ModifierArguments (ModifierId, Name, Value)
SELECT ModifierId, 'Amount', '2' FROM Modifiers WHERE ModifierId = 'TRAIT_TOURISM_INTO_FAVOR'
UNION ALL
SELECT ModifierId, 'YieldType', 'YIELD_CULTURE' FROM Modifiers WHERE ModifierId = 'TRAIT_TOURISM_INTO_FAVOR';

-- America's wildcard conversion survives. Replace wildcard favor with a
-- small passive boost to earning envoys.
UPDATE Modifiers SET ModifierType = 'MODIFIER_PLAYER_ADJUST_INFLUENCE_POINTS_PER_TURN'
WHERE ModifierId = 'TRAIT_WILD_CARD_FAVOR';

DELETE FROM ModifierArguments WHERE ModifierId = 'TRAIT_WILD_CARD_FAVOR';
INSERT INTO ModifierArguments (ModifierId, Name, Value)
SELECT ModifierId, 'Amount', '1' FROM Modifiers WHERE ModifierId = 'TRAIT_WILD_CARD_FAVOR';

-- Preserve ordinary loyalty loss from kills; discard the age-only extra loss.
UPDATE ModifierArguments SET Value = '0'
WHERE ModifierId = 'TRAIT_DIMINISH_LOYALTY_IN_ENEMY_CITY' AND Name = 'AdditionalGoldenAge';
