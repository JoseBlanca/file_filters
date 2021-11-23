
from pathlib import Path


def filter_out_changed_files(current_dir, fnames, orig_dir, dest_dir, fnames_to_ignore=None):

    if fnames_to_ignore is None:
        fnames_to_ignore = []

    current_dir = Path(current_dir).resolve()
    orig_dir = orig_dir.resolve()
    dest_dir = dest_dir.resolve()

    relative_current_dir = current_dir.relative_to(orig_dir)

    changed_files_fnames = []
    for fname in fnames:
        file_path_in_orig_dir = orig_dir / relative_current_dir / fname
        file_path_in_dest_dir = dest_dir / relative_current_dir / fname

        if fname in fnames_to_ignore:
            continue
        if not file_path_in_dest_dir.exists():
            changed_files_fnames.append(fname)
            continue
        if file_path_in_dest_dir.is_dir():
            changed_files_fnames.append(fname)
            continue

        orig_size = file_path_in_orig_dir.stat().st_size
        dest_size = file_path_in_dest_dir.stat().st_size
        if orig_size != dest_size:
            changed_files_fnames.append(fname)
    
    fnames = [fname for fname in fnames if fname not in changed_files_fnames]
    return fnames
