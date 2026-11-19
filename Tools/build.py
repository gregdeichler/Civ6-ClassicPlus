"""Validate the manifest and package exactly the files it declares."""
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'ClassicPlus.modinfo'


def manifest():
    mod = ET.parse(ROOT / MANIFEST).getroot()
    paths = [f.text for f in mod.findall('./Files/File')]
    assert mod.tag == 'Mod' and paths and len(paths) == len(set(paths))
    assert len({p.casefold() for p in paths}) == len(paths)
    references = {f.text for section in ('FrontEndActions', 'InGameActions')
                  for f in mod.findall(f'./{section}//File')}
    references.update(f.text for f in mod.findall('./InGameActions//LuaReplace'))
    assert set(paths) == references, 'Manifest file declarations and action references differ'
    criteria = {node.get('id') for node in mod.findall('./ActionCriteria/Criteria')}
    actions = list(mod.find('FrontEndActions')) + list(mod.find('InGameActions'))
    assert len({a.get('id') for a in actions}) == len(actions)
    for action in actions:
        criterion = action.get('criteria') or action.findtext('Criteria')
        assert criterion is None or criterion in criteria, criterion
    for path in paths:
        parts = PurePosixPath(path).parts
        assert not PurePosixPath(path).is_absolute() and '..' not in parts
        assert (ROOT / path).is_file(), path
        if path.endswith('.xml'):
            ET.parse(ROOT / path)
    return mod, paths


def package():
    _, paths = manifest()
    out = ROOT / 'dist' / 'ClassicPlus-0.1.0-preview.zip'
    out.parent.mkdir(exist_ok=True)
    with ZipFile(out, 'w', compression=ZIP_DEFLATED) as archive:
        for path in sorted([MANIFEST, *paths]):
            info = ZipInfo(f'ClassicPlus/{path}')
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / path).read_bytes(), compress_type=ZIP_DEFLATED)
    with ZipFile(out) as archive:
        assert archive.testzip() is None
    print(out)


if __name__ == '__main__':
    package()
