import os
import zipfile
from pathlib import Path
from pyunpack import Archive
from tempfile import TemporaryDirectory


def zipit(path, archname):
    """
    recursive zip

    :param path:
    :param archname:
    :return:
    """
    archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        _zippy(path, path, archive)
    else:
        _, name = os.path.split(path)
        archive.write(path, name)
    archive.close()


def _zippy(base_path, path, archive):
    paths = os.listdir(path)
    for p in paths:
        p = os.path.join(path, p)
        if os.path.isdir(p):
            _zippy(base_path, p, archive)
        else:
            archive.write(p, os.path.relpath(p, base_path))


for skin_file in Path("skins").glob("*.zip"):
    with TemporaryDirectory() as temp_dir:
        Archive(str(skin_file)).extractall(temp_dir)
        monster_dir = Path(temp_dir) / "monsters"
        heroes_dir = Path(temp_dir) / "heroes"
        print(skin_file.name)
        assert any([monster_dir.exists(), heroes_dir.exists()])

        if monster_dir.exists():
            the_dir = monster_dir
        else:
            the_dir = heroes_dir

        # do stuff here

        # (the_dir / ".skin_identifier").unlink()
        # (next(the_dir.glob("*")) / ".skin_identifier").write_text(skin_file.stem)
        zipit(str(temp_dir), "skins/" + skin_file.name)
