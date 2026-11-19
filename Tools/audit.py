"""Print a Gathering Storm roster and candidate dependencies from clean game databases."""
import argparse
from collections import defaultdict
from pathlib import Path
import re
import sqlite3

PATTERNS = {
    'Ages': r'GOLDEN_AGE|DARK_AGE|ERA_AGE|ERA_SCORE|COMMEMORATION|HISTORIC_MOMENT',
    'Governors': r'GOVERNOR',
    'Congress': r'CONGRESS|FAVOR|DIPLOMATIC_VICTORY|EMERGENCY|NOBEL_PRIZE',
    'Resources': r'STOCKPILE|ACCUMULATION|RESOURCE_MAINTENANCE|STRATEGIC_RESOURCE|RESOURCE_COST|RESOURCE_EXTRACTION',
    'Power': r'REQUIRED_POWER|POWERED|POWER_CONSUMPTION|POWER_PRODUCTION|POWER_PLANT|POWER_REQUIREMENT|ELECTRICITY',
    'Grievances': r'GRIEVANCE|WARMONGER',
}


def read_only(path):
    return sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)


def audit(configuration, gameplay):
    with read_only(configuration) as config, read_only(gameplay) as db:
        roster = config.execute("""
            SELECT LeaderType, CivilizationType FROM Players
            WHERE Domain = 'Players:Expansion2_Players' AND HumanPlayable = 1
            ORDER BY LeaderType, CivilizationType
        """).fetchall()
        traits = defaultdict(set)
        roots = defaultdict(set)
        modifier_data = defaultdict(set)
        children = defaultdict(set)
        for table, key in [('LeaderTraits', 'LeaderType'), ('CivilizationTraits', 'CivilizationType')]:
            for owner, trait in db.execute(f'SELECT {key}, TraitType FROM {table}'):
                traits[owner].add(trait)
        for trait, modifier in db.execute('SELECT TraitType, ModifierId FROM TraitModifiers'):
            roots[trait].add(modifier)
        for content, key in [('Buildings', 'BuildingType'),
                             ('Districts', 'DistrictType'), ('Improvements', 'ImprovementType')]:
            for trait, modifier in db.execute(f'''
                SELECT c.TraitType, m.ModifierId FROM {content} c
                JOIN {content[:-1]}Modifiers m USING ({key}) WHERE c.TraitType IS NOT NULL
            '''):
                roots[trait].add(modifier)
        for trait, modifier in db.execute('''
            SELECT DISTINCT u.TraitType, m.ModifierId FROM Units u
            JOIN TypeTags ut ON ut.Type = u.UnitType
            JOIN TypeTags ab ON ab.Tag = ut.Tag
            JOIN UnitAbilityModifiers m ON m.UnitAbilityType = ab.Type
            JOIN UnitAbilities a ON a.UnitAbilityType = ab.Type
            WHERE u.TraitType IS NOT NULL AND a.Inactive = 0
        '''):
            roots[trait].add(modifier)
        for mid, modifier_type, owner, subject in db.execute('''
            SELECT ModifierId, ModifierType, OwnerRequirementSetId, SubjectRequirementSetId
            FROM Modifiers
        '''):
            modifier_data[mid].update(x for x in (mid, modifier_type, owner, subject) if x)
            for req in (owner, subject):
                if req:
                    modifier_data[mid].update(x for row in db.execute('''
                        SELECT r.RequirementId, r.RequirementType FROM RequirementSetRequirements sr
                        JOIN Requirements r USING (RequirementId) WHERE sr.RequirementSetId = ?
                    ''', (req,)) for x in row)
        for mid, name, value in db.execute('SELECT ModifierId, Name, Value FROM ModifierArguments'):
            if value in modifier_data:
                children[mid].add(value)
            elif name != 'Amount':
                modifier_data[mid].add(value)
        for leader, civ in roster:
            owned = traits[leader] | traits[civ]
            pending = [mid for trait in owned for mid in roots[trait]]
            visited = set()
            signals = set(owned)
            while pending:
                mid = pending.pop()
                if mid not in visited:
                    visited.add(mid)
                    signals.update(modifier_data[mid])
                    pending.extend(children[mid])
            # Some unique content uses XP2 columns with no attached modifier.
            for table, id_col, xp2_fields, category in (
                ('Units', 'UnitType', 'x.ResourceCost > 0 OR x.ResourceMaintenanceAmount > 0', 'STRATEGIC_RESOURCE'),
                ('Buildings', 'BuildingType', 'x.RequiredPower > 0 OR x.ResourceTypeConvertedToPower IS NOT NULL', 'REQUIRED_POWER'),
            ):
                for trait in owned:
                    if db.execute(f'''
                        SELECT 1 FROM {table} t JOIN {table}_XP2 x USING ({id_col})
                        WHERE t.TraitType = ? AND ({xp2_fields}) LIMIT 1
                    ''', (trait,)).fetchone():
                        signals.add(category)
            flags = [label for label, pattern in PATTERNS.items()
                     if any(re.search(pattern, signal.upper()) for signal in signals)]
            print(f'| `{leader}` | `{civ}` | {", ".join(flags) or "None flagged"} |')
    print(f'\n{len(roster)} playable entries.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('configuration')
    parser.add_argument('gameplay')
    args = parser.parse_args()
    audit(args.configuration, args.gameplay)
