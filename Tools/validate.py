"""Apply mod SQL to disposable copies of clean Civ VI debug databases."""
import argparse
from pathlib import Path
import sqlite3

from build import ROOT, manifest


def check_databases(frontend, gameplay):
    mod, _ = manifest()
    for section, path in [('FrontEndActions', frontend), ('InGameActions', gameplay)]:
        uri = Path(path).resolve().as_uri() + '?mode=ro'
        with sqlite3.connect(uri, uri=True) as source, sqlite3.connect(':memory:') as db:
            source.backup(db)
            db.execute('PRAGMA foreign_keys = ON')
            fk_before = set(db.execute('PRAGMA foreign_key_check'))
            frontend_section = section == 'FrontEndActions'
            preserved = (
                ['SELECT * FROM Players', 'SELECT * FROM PlayerItems',
                 "SELECT * FROM Victories WHERE VictoryType <> 'VICTORY_DIPLOMATIC'"]
                if frontend_section else
                ['SELECT * FROM Eras', 'SELECT * FROM Eras_XP1', 'SELECT * FROM Eras_XP2',
                 'SELECT * FROM Leaders', 'SELECT * FROM Civilizations',
                 'SELECT * FROM Units_XP2', 'SELECT * FROM Governors',
                 'SELECT * FROM DiplomaticActions',
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
    print('Manifest, database postconditions, preserved data, and foreign keys passed. Engine/UI untested.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('configuration', help='Clean DebugConfiguration.sqlite')
    parser.add_argument('gameplay', help='Clean Gathering Storm DebugGameplay.sqlite')
    args = parser.parse_args()
    check_databases(args.configuration, args.gameplay)
