-- Keep CAPABILITY_ERAS and the Eras tables: world eras drive unrelated systems.
DELETE FROM GameCapabilityDependencies
WHERE GameCapability IN ('CAPABILITY_GOLDEN_AND_DARK_AGES', 'CAPABILITY_HISTORIC_MOMENTS')
   OR DependsOnCapability IN ('CAPABILITY_GOLDEN_AND_DARK_AGES', 'CAPABILITY_HISTORIC_MOMENTS');

DELETE FROM GameCapabilities
WHERE GameCapability IN ('CAPABILITY_GOLDEN_AND_DARK_AGES', 'CAPABILITY_HISTORIC_MOMENTS');

UPDATE Moments SET EraScore = 0 WHERE EraScore <> 0;

DELETE FROM Notifications
WHERE NotificationType IN ('NOTIFICATION_QUEST_RECORDED', 'NOTIFICATION_COMMEMORATION_AVAILABLE');

-- The Taj Mahal's only special effect was era score.
DELETE FROM BuildingModifiers
WHERE BuildingType = 'BUILDING_TAJ_MAHAL' AND ModifierId = 'TAJ_MAHAL_EXTRA_ERA_SCORE';

INSERT OR IGNORE INTO Building_YieldChanges (BuildingType, YieldType, YieldChange)
SELECT BuildingType, 'YIELD_CULTURE', 4 FROM Buildings WHERE BuildingType = 'BUILDING_TAJ_MAHAL';
