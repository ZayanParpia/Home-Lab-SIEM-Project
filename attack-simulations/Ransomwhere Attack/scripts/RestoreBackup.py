import os
import shutil
from pathlib import Path

import gdown


# ============================================================
# CONFIGURATION
# ============================================================

DRIVE_FOLDER_URL = (
    "https://drive.google.com/drive/folders/"
    "1W0Ti8DK2-kFQid1BPrjDky_9ho7GVl5f?usp=sharing"
)

LOCAL_FOLDER = Path(
    r"C:\Users\ikepa\OneDrive\Pictures\SIEM system"
    r"\\attack-simulations\\Ransomwhere Attack\\scripts"
)


# ============================================================
# REMOVE OLD FILE/FOLDER
# ============================================================

def remove_existing(path):
    """
    Remove an existing file or folder.
    """

    if not path.exists():
        return

    if path.is_file() or path.is_symlink():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


# ============================================================
# DOWNLOAD GOOGLE DRIVE FOLDER
# ============================================================

def download_drive_folder():

    print("=" * 60)
    print("Google Drive Restore")
    print("=" * 60)

    print(f"\nGoogle Drive folder:")
    print(DRIVE_FOLDER_URL)

    print(f"\nLocal destination:")
    print(LOCAL_FOLDER)

    LOCAL_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # Temporary download location.
    temp_folder = LOCAL_FOLDER / "_google_drive_restore"

    # Start with a clean temporary folder.
    if temp_folder.exists():
        print("\nRemoving previous temporary download...")
        remove_existing(temp_folder)

    temp_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\nDownloading assets...")
    print("-" * 60)

    try:

        downloaded = gdown.download_folder(
            url=DRIVE_FOLDER_URL,
            output=str(temp_folder),
            quiet=False,
            use_cookies=False
        )

    except Exception as error:

        print("\nDOWNLOAD FAILED")
        print("-" * 60)
        print(error)

        if temp_folder.exists():
            remove_existing(temp_folder)

        return False

    print("\nDownload finished.")
    print("-" * 60)

    # ========================================================
    # FIND THE DOWNLOADED FOLDER
    # ========================================================

    downloaded_items = list(temp_folder.iterdir())

    if not downloaded_items:

        print("No files were downloaded.")

        remove_existing(temp_folder)

        return False

    # gdown normally creates the Drive folder inside output.
    # If there is exactly one directory, use it.
    if len(downloaded_items) == 1 and downloaded_items[0].is_dir():

        source_folder = downloaded_items[0]

    else:

        source_folder = temp_folder

    # ========================================================
    # REPLACE EXISTING FILES/FOLDERS
    # ========================================================

    print("\nRestoring files...")
    print("-" * 60)

    for source in source_folder.iterdir():

        destination = LOCAL_FOLDER / source.name

        print(f"\nRestoring: {source.name}")

        # Remove existing item with the same name.
        if destination.exists():

            print("  Replacing existing item...")

            remove_existing(destination)

        # Copy folder.
        if source.is_dir():

            shutil.copytree(
                source,
                destination
            )

        # Copy file.
        else:

            shutil.copy2(
                source,
                destination
            )

        print("  Restored successfully.")

    # ========================================================
    # CLEAN UP
    # ========================================================

    print("\nCleaning temporary files...")

    remove_existing(temp_folder)

    print("\n" + "=" * 60)
    print("RESTORE COMPLETE")
    print("=" * 60)

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    success = download_drive_folder()

    if success:

        print("\nAll Google Drive assets have been restored.")

    else:

        print("\nRestore failed.")


if __name__ == "__main__":
    main()

