import shutil
import tempfile
from pathlib import Path

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


# ============================================================
# CONFIGURATION
# ============================================================

# The ID of the shared folder (from the URL:
# https://drive.google.com/drive/folders/<THIS_PART>?usp=sharing)
DRIVE_FOLDER_ID = "1W0Ti8DK2-kFQid1BPrjDky_9ho7GVl5f"

LOCAL_FOLDER = Path(
    r"/home/endpoint4/Documents"
)

# Path to the OAuth client secrets file you download from
# Google Cloud Console (APIs & Services -> Credentials ->
# OAuth client ID -> Desktop app -> Download JSON).
# Resolved relative to this script's own folder, so it works
# no matter what directory you launch the script from.
SCRIPT_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = str(SCRIPT_DIR / "client_secret_92787663520-e5gm4tp5e298mdp8vfdr85rnjqpvehjd.apps.googleusercontent.com.json")

# Where PyDrive2 will cache your OAuth token after the first
# login, so you don't have to re-authenticate every run.
SAVED_CREDS_FILE = str(SCRIPT_DIR / "saved_credentials.json")


# ============================================================
# AUTH
# ============================================================

def authenticate():
    """
    Authenticate with the Google Drive API using OAuth.

    Because this uses YOUR account's credentials (not an
    anonymous/public request like gdown), it can access any
    file you own or have been shared, regardless of whether
    that file individually has "Anyone with the link" turned
    on. This is what fixes the permission errors gdown hit.
    """

    gauth = GoogleAuth()

    gauth.LoadClientConfigFile(CLIENT_SECRETS_FILE)
    gauth.LoadCredentialsFile(SAVED_CREDS_FILE)

    if gauth.credentials is None:
        # No local browser available on headless Ubuntu/CLI, so
        # print a URL to open elsewhere and paste back the code.
        gauth.CommandLineAuth()

    elif gauth.access_token_expired:
        gauth.Refresh()

    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(SAVED_CREDS_FILE)

    return GoogleDrive(gauth)


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
# RECURSIVELY DOWNLOAD A DRIVE FOLDER
# ============================================================

def download_folder_recursive(drive, folder_id, destination, stats, depth=0):
    """
    Recursively download every file and every subfolder (at any
    depth) under folder_id into destination, using authenticated
    API calls (no public-link permission required).

    stats is a dict used to accumulate counts of successes and
    failures across the whole recursive walk, so a bad file
    somewhere deep in the tree never stops the rest of the
    folder from downloading.
    """

    destination.mkdir(parents=True, exist_ok=True)

    indent = "  " * depth

    query = (
        f"'{folder_id}' in parents and trashed=false"
    )

    file_list = drive.ListFile({
        "q": query,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
        "corpora": "allDrives",
    }).GetList()

    if not file_list:
        print(f"{indent}(empty folder)")
        return

    # Process subfolders first, then files, purely for readable output.
    subfolders = [
        f for f in file_list
        if f["mimeType"] == "application/vnd.google-apps.folder"
    ]
    files = [f for f in file_list if f not in subfolders]

    for item in subfolders:
        item_name = item["title"]
        item_path = destination / item_name

        print(f"{indent}[dir] {item_name}/")
        download_folder_recursive(
            drive, item["id"], item_path, stats, depth + 1
        )

    for item in files:
        item_name = item["title"]
        item_path = destination / item_name

        print(f"{indent}Downloading: {item_name}")

        try:
            item.GetContentFile(str(item_path))
            print(f"{indent}  OK")
            stats["succeeded"].append(str(item_path))

        except Exception as error:
            print(f"{indent}  FAILED: {error}")
            stats["failed"].append((str(item_path), str(error)))


# ============================================================
# MAIN RESTORE FLOW
# ============================================================

def download_drive_folder():

    print("=" * 60)
    print("Google Drive Restore (authenticated)")
    print("=" * 60)

    print("\nGoogle Drive folder ID:")
    print(DRIVE_FOLDER_ID)

    print("\nLocal destination:")
    print(LOCAL_FOLDER)

    print("\nAuthenticating...")
    drive = authenticate()

    LOCAL_FOLDER.mkdir(parents=True, exist_ok=True)

    temp_folder = Path(
        tempfile.mkdtemp(prefix="google_drive_restore_")
    )

    print("\nTemporary download location:")
    print(temp_folder)

    print("\nDownloading assets (recursing into every subfolder)...")
    print("-" * 60)

    stats = {"succeeded": [], "failed": []}

    try:
        download_folder_recursive(drive, DRIVE_FOLDER_ID, temp_folder, stats)

    except Exception as error:
        print("\nDOWNLOAD FAILED")
        print("-" * 60)
        print(error)

        remove_existing(temp_folder)
        return False

    print("\n" + "-" * 60)
    print(f"Downloaded: {len(stats['succeeded'])}   Failed: {len(stats['failed'])}")

    if stats["failed"]:
        print("\nThe following items failed and were skipped:")
        for path, error in stats["failed"]:
            print(f"  - {path}: {error}")

    downloaded_items = list(temp_folder.iterdir())

    if not downloaded_items:
        print("\nDOWNLOAD FAILED")
        print("The temporary folder is empty.")

        remove_existing(temp_folder)
        return False

    print("\nDownload finished.")
    print("-" * 60)

    # ========================================================
    # RESTORE FILES
    # ========================================================

    print("\nRestoring files...")
    print("-" * 60)

    for source in temp_folder.iterdir():

        destination = LOCAL_FOLDER / source.name

        print(f"\nRestoring: {source.name}")

        if destination.exists():
            print("  Replacing existing item...")
            remove_existing(destination)

        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

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