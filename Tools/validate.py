"""Apply mod SQL to disposable copies of clean Civ VI debug databases."""
import argparse
from pathlib import Path
import sqlite3

from build import ROOT, manifest


def diplomacy_and_flooding_checks(db):
    assert not db.execute('''SELECT 1 FROM DiplomaticActions
        WHERE WarmongerPercent<>0 OR CaptureWarmongerPercent<>0 OR RazeWarmongerPercent<>0''').fetchone()
    assert not db.execute('''SELECT 1 FROM DiplomaticActions_XP2
        WHERE GrievanceCost<>0 OR GrievancesForRefusal<>0 OR GrievancesPerIncursion<>0''').fetchone()
    assert db.execute('''SELECT TraitType FROM TraitModifiers
        WHERE ModifierId='CLASSICPLUS_NO_GRIEVANCE_GENERATION' ORDER BY TraitType''').fetchall() == [
            ('MINOR_CIV_DEFAULT_TRAIT',), ('TRAIT_LEADER_MAJOR_CIV',)]
    assert db.execute('''SELECT m.ModifierType, a.Value FROM Modifiers m
        JOIN ModifierArguments a USING (ModifierId)
        WHERE m.ModifierId='CLASSICPLUS_NO_GRIEVANCE_GENERATION' AND a.Name='Amount'
        ''').fetchone() == ('MODIFIER_PLAYER_ADJUST_GRIEVANCE_MULTIPLIER', '-100')
    grievance_sources = db.execute('''SELECT Name, Value FROM GlobalParameters
        WHERE Name IN ('GRIEVANCE_MULTIPLIER_FOR_BROKEN_PROMISE',
            'GRIEVANCES_ALL_PLAYERS_CITY_STATE_CONQUEST', 'GRIEVANCES_FOR_DENOUNCEMENT',
            'GRIEVANCES_HAVE_ENVOYS_CITY_STATE_DOW', 'GRIEVANCES_POSSESS_CAPITAL_PER_TURN',
            'GRIEVANCES_POSSESS_NON_CAPITAL_PER_TURN', 'GRIEVANCES_SUZERAIN_CITY_STATE_DOW',
            'SHARE_WAR_GRIEVANCES_ALLY', 'SHARE_WAR_GRIEVANCES_DECLARED_FRIENDS',
            'SHARE_WAR_GRIEVANCES_DEFENSIVE_PERCENT')''').fetchall()
    assert len(grievance_sources) == 10 and all(int(value) == 0 for _, value in grievance_sources)
    assert db.execute('''SELECT Value FROM ModifierArguments
        WHERE (ModifierId='STANDARD_DIPLOMATIC_WARMONGER'
            AND Name IN ('PercentOfGrievances', 'LowerLimit'))
        OR (ModifierId='STANDARD_DIPLOMATIC_THIRD_PARTY_WARMONGER'
            AND Name IN ('PercentOfGrievancesDelta', 'LowerLimit'))''').fetchall() == [('0',)] * 4
    assert db.execute('''SELECT DefaultValue FROM PseudoYields
        WHERE PseudoYieldType='PSEUDOYIELD_DIPLOMATIC_GRIEVANCE' ''').fetchone() == (0,)
    # Do not touch divisor or duration parameters while neutralizing source amounts.
    assert int(db.execute("SELECT Value FROM GlobalParameters WHERE Name='FAVOR_GRIEVANCES_DIVISOR'").fetchone()[0]) > 0
    flood_events = {row[0] for row in db.execute('''SELECT RandomEventType FROM RandomEvents
        WHERE EffectOperatorType IN ('FLOODPLAIN', 'SEA_LEVEL')''')}
    assert {'RANDOM_EVENT_FLOOD_MODERATE', 'RANDOM_EVENT_FLOOD_MAJOR',
            'RANDOM_EVENT_FLOOD_1000_YEAR', 'RANDOM_EVENT_SEA_LEVEL_RISE7'} <= flood_events
    for event in flood_events:
        frequencies = db.execute('''SELECT OccurrencesPerGame FROM RandomEvent_Frequencies
            WHERE RandomEventType=?''', (event,)).fetchall()
        assert len(frequencies) == db.execute('SELECT COUNT(*) FROM RealismSettings').fetchone()[0]
        assert all(row == (0,) for row in frequencies), event
        assert db.execute('SELECT ChanceIncreasePerDegree FROM RandomEvents WHERE RandomEventType=?',
                          (event,)).fetchone() == (0,)
    assert not db.execute('''SELECT 1 FROM RandomEvent_Damages d JOIN RandomEvents e USING (RandomEventType)
        WHERE e.EffectOperatorType='FLOODPLAIN'
          AND (d.Percentage<>0 OR d.MinHP<>0 OR d.MaxHP<>0 OR d.CoastalLowlandPercentage<>0)''').fetchone()
    assert not db.execute('''SELECT 1 FROM RandomEvent_Yields y JOIN RandomEvents e USING (RandomEventType)
        WHERE e.EffectOperatorType='FLOODPLAIN' AND (y.Percentage<>0 OR y.Amount<>0)''').fetchone()
    assert db.execute('''SELECT Value FROM GlobalParameters
        WHERE Name='CLIMATE_CHANGE_PERCENT_COASTAL_LOWLANDS' ''').fetchone() == ('0',)
    assert {'CAPABILITY_DIPLOMACY', 'CAPABILITY_DIPLOMACY_DEALS', 'CAPABILITY_TRADE',
            'CAPABILITY_RANDOM_EVENTS'} <= {r[0] for r in db.execute('SELECT GameCapability FROM GameCapabilities')}


def check_databases(frontend, gameplay):
    mod, _ = manifest()
    cases = [('FrontEndActions', frontend, False),
             ('InGameActions', gameplay, False),
             ('InGameActions', gameplay, True)]
    for section, path, without_persia_requirement in cases:
        uri = Path(path).resolve().as_uri() + '?mode=ro'
        with sqlite3.connect(uri, uri=True) as source, sqlite3.connect(':memory:') as db:
            source.backup(db)
            db.execute('PRAGMA foreign_keys = ON')
            if without_persia_requirement:
                # Reproduce the missing optional-DLC rule reported by the engine.
                # Clear stock users of that rule in this disposable fixture only.
                for column in ('OwnerRequirementSetId', 'SubjectRequirementSetId'):
                    db.execute(f'UPDATE Modifiers SET {column}=NULL WHERE {column}=?',
                               ('PLAYER_HAS_POLITICAL_PHILOSOPHY',))
                db.execute('DELETE FROM RequirementSetRequirements WHERE RequirementSetId=?',
                           ('PLAYER_HAS_POLITICAL_PHILOSOPHY',))
                db.execute('DELETE FROM RequirementSets WHERE RequirementSetId=?',
                           ('PLAYER_HAS_POLITICAL_PHILOSOPHY',))
                db.commit()
                print('Regression: optional Persia requirement set absent')
            fk_before = set(db.execute('PRAGMA foreign_key_check'))
            frontend_section = section == 'FrontEndActions'
            action_columns = ', '.join(f'"{r[1]}"' for r in db.execute('PRAGMA table_info(DiplomaticActions)')
                                       if r[1] not in ('WarmongerPercent', 'CaptureWarmongerPercent', 'RazeWarmongerPercent')) \
                if not frontend_section else ''
            preserved = (
                ['SELECT * FROM Players', 'SELECT * FROM PlayerItems',
                 "SELECT * FROM Victories WHERE VictoryType <> 'VICTORY_DIPLOMATIC'"]
                if frontend_section else
                ['SELECT * FROM Eras', 'SELECT * FROM Eras_XP1', 'SELECT * FROM Eras_XP2',
                 'SELECT * FROM Leaders', 'SELECT * FROM Civilizations',
                 'SELECT * FROM Units_XP2', 'SELECT * FROM Governors',
                 f'SELECT {action_columns} FROM DiplomaticActions',
                 'SELECT * FROM DiplomaticStateActions', 'SELECT * FROM DiplomaticStateTransitions',
                 'SELECT * FROM DiplomaticTriggeredTransitions',
                 'SELECT DiplomaticActionType, PromiseType, RequiredPromise FROM DiplomaticActions_XP2',
                 'SELECT * FROM Feature_Floodplains', 'SELECT * FROM Features',
                 'SELECT * FROM CoastalLowlands', 'SELECT * FROM Districts_XP2',
                 'SELECT * FROM Buildings_XP2', 'SELECT * FROM Building_YieldChangesBonusWithPower',
                 'SELECT RandomEventType FROM RandomEvents',
                 "SELECT * FROM RandomEvents WHERE EffectOperatorType NOT IN ('FLOODPLAIN', 'SEA_LEVEL')",
                 "SELECT f.* FROM RandomEvent_Frequencies f JOIN RandomEvents e USING (RandomEventType) WHERE e.EffectOperatorType NOT IN ('FLOODPLAIN', 'SEA_LEVEL')",
                 "SELECT d.* FROM RandomEvent_Damages d JOIN RandomEvents e USING (RandomEventType) WHERE e.EffectOperatorType NOT IN ('FLOODPLAIN', 'SEA_LEVEL')",
                 "SELECT y.* FROM RandomEvent_Yields y JOIN RandomEvents e USING (RandomEventType) WHERE e.EffectOperatorType NOT IN ('FLOODPLAIN', 'SEA_LEVEL')",
                 "SELECT * FROM Victories WHERE VictoryType <> 'VICTORY_DIPLOMATIC'"]
            )
            before = [list(db.execute(query)) for query in preserved]
            assert db.execute("SELECT 1 FROM Victories WHERE VictoryType='VICTORY_DIPLOMATIC' "
                              "AND EnabledByDefault=1").fetchone(), 'Use a clean Gathering Storm DB'
            actions = sorted(mod.findall(f'./{section}/UpdateDatabase'),
                             key=lambda a: int(a.findtext('./Properties/LoadOrder', '0')))
            for action in actions:
                for file in action.findall('File'):
                    db.executescript((ROOT / file.text).read_text())
                    print(f'Applied {file.text}')
            assert set(db.execute('PRAGMA foreign_key_check')) <= fk_before
            assert [list(db.execute(query)) for query in preserved] == before
            assert not db.execute("SELECT 1 FROM Victories WHERE VictoryType='VICTORY_DIPLOMATIC' "
                                  "AND EnabledByDefault=1").fetchone()
            if frontend_section:
                assert db.execute("SELECT Visible, ReadOnly FROM Victories "
                                  "WHERE Domain='Expansion2_Victories' AND VictoryType='VICTORY_DIPLOMATIC'").fetchone() == (0, 1)
                continue
            caps = {row[0] for row in db.execute('SELECT GameCapability FROM GameCapabilities')}
            assert not caps & {'CAPABILITY_WORLD_CONGRESS', 'CAPABILITY_EMERGENCIES',
                               'CAPABILITY_GOLDEN_AND_DARK_AGES', 'CAPABILITY_HISTORIC_MOMENTS'}
            assert {'CAPABILITY_ERAS', 'CAPABILITY_LENS_LOYALTY', 'CAPABILITY_GOVERNORS',
                    'CAPABILITY_DIPLOMACY_DEALS', 'CAPABILITY_WORLD_CLIMATE'} <= caps
            assert db.execute('SELECT MAX(EraScore) FROM Moments').fetchone() == (0,)
            era = db.execute("SELECT Value FROM GlobalParameters WHERE Name='WORLD_CONGRESS_INITIAL_ERA'").fetchone()
            assert int(era[0]) > db.execute('SELECT COUNT(*) FROM Eras').fetchone()[0]
            assert db.execute("SELECT Value FROM ModifierArguments WHERE ModifierId="
                              "'TRAIT_TOURISM_INTO_FAVOR' AND Name='YieldType'").fetchone() == ('YIELD_CULTURE',)
            assert db.execute("SELECT ModifierType FROM Modifiers WHERE ModifierId="
                              "'GOLDEN_AGE_TRADE_ROUTE'").fetchone() == ('MODIFIER_PLAYER_ADJUST_TRADE_ROUTE_CAPACITY',)
            assert db.execute("SELECT SubjectRequirementSetId FROM Modifiers WHERE ModifierId="
                              "'GOLDEN_AGE_TRADE_ROUTE'").fetchone() == ('CLASSICPLUS_PLAYER_HAS_POLITICAL_PHILOSOPHY',)
            assert db.execute('''SELECT s.RequirementSetType, r.RequirementType, a.Value
                FROM RequirementSets s
                JOIN RequirementSetRequirements links USING (RequirementSetId)
                JOIN Requirements r USING (RequirementId)
                JOIN RequirementArguments a USING (RequirementId)
                WHERE s.RequirementSetId='CLASSICPLUS_PLAYER_HAS_POLITICAL_PHILOSOPHY'
                  AND a.Name='CivicType' ''').fetchall() == [
                    ('REQUIREMENTSET_TEST_ALL', 'REQUIREMENT_PLAYER_HAS_CIVIC', 'CIVIC_POLITICAL_PHILOSOPHY')]
            diplomacy_and_flooding_checks(db)
    print('Manifest, database postconditions, preserved data, and foreign keys passed. Engine/UI untested.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('configuration', help='Clean DebugConfiguration.sqlite')
    parser.add_argument('gameplay', help='Clean Gathering Storm DebugGameplay.sqlite')
    args = parser.parse_args()
    check_databases(args.configuration, args.gameplay)
