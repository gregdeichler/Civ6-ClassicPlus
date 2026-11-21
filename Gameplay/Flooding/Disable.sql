-- Disable river floods and coastal inundation at every disaster intensity.
-- Keep the event catalog: lowland, notification and other engine records refer
-- to it. Other disaster types retain their stock scheduling and damage.
UPDATE RandomEvent_Frequencies SET OccurrencesPerGame = 0
WHERE RandomEventType IN (
    SELECT RandomEventType FROM RandomEvents
    WHERE EffectOperatorType IN ('FLOODPLAIN', 'SEA_LEVEL')
);

-- Warming must not add river floods back to a zero-frequency schedule.
UPDATE RandomEvents SET ChanceIncreasePerDegree = 0
WHERE EffectOperatorType IN ('FLOODPLAIN', 'SEA_LEVEL');

-- A second guard for any forced river event: no damage or flood fertilization.
UPDATE RandomEvent_Damages
SET Percentage = 0, MinHP = 0, MaxHP = 0, CoastalLowlandPercentage = 0
WHERE RandomEventType IN (
    SELECT RandomEventType FROM RandomEvents WHERE EffectOperatorType = 'FLOODPLAIN'
);

UPDATE RandomEvent_Yields SET Percentage = 0, Amount = 0
WHERE RandomEventType IN (
    SELECT RandomEventType FROM RandomEvents WHERE EffectOperatorType = 'FLOODPLAIN'
);

-- The stock CoastalLowlands map utility uses this percentage before marking
-- vulnerable tiles. Zero produces no coastal lowlands on newly generated maps.
-- Floodplain features, rivers, dams, power and ordinary tile yields remain.
UPDATE GlobalParameters SET Value = 0
WHERE Name = 'CLIMATE_CHANGE_PERCENT_COASTAL_LOWLANDS';
