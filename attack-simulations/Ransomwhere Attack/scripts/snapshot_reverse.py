#!/usr/bin/env python3
"""
List all snapshots for a VMware VM and revert to the most recent (last) one.

Requires:
    pip install pyvmomi --break-system-packages

Usage:
    python3 vm_snapshot_revert.py --host vcenter.example.com --user administrator@vsphere.local --vm-name "MyVM"

You will be prompted for the password (or use --password / VMWARE_PASSWORD env var).
"""

import argparse
import atexit
import getpass
import os
import ssl
import sys
from datetime import datetime

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim


def get_args():
    parser = argparse.ArgumentParser(description="List and revert VMware VM snapshots")
    parser.add_argument("--host", required=True, help="vCenter/ESXi host or IP")
    parser.add_argument("--port", type=int, default=443, help="Port (default 443)")
    parser.add_argument("--user", required=True, help="Username")
    parser.add_argument("--password", default=None, help="Password (omit to be prompted, or set VMWARE_PASSWORD)")
    parser.add_argument("--vm-name", required=True, help="Name of the VM to operate on")
    parser.add_argument("--insecure", action="store_true", default=True,
                         help="Skip SSL certificate verification (default: True for self-signed certs)")
    parser.add_argument("--list-only", action="store_true",
                         help="Only list snapshots, do not revert")
    parser.add_argument("--yes", action="store_true",
                         help="Skip confirmation prompt before reverting")
    return parser.parse_args()


def connect(args, password):
    context = None
    if args.insecure:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(
        host=args.host,
        user=args.user,
        pwd=password,
        port=args.port,
        sslContext=context,
    )
    atexit.register(Disconnect, si)
    return si


def find_vm_by_name(content, name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    try:
        for vm in container.view:
            if vm.name == name:
                return vm
    finally:
        container.Destroy()
    return None


def flatten_snapshot_tree(snap_tree, depth=0, out=None):
    """Recursively flatten the snapshot tree, preserving creation order info."""
    if out is None:
        out = []
    for snap in snap_tree:
        out.append((depth, snap))
        if snap.childSnapshotList:
            flatten_snapshot_tree(snap.childSnapshotList, depth + 1, out)
    return out


def list_snapshots(vm):
    if vm.snapshot is None:
        print(f"VM '{vm.name}' has no snapshots.")
        return []

    flat = flatten_snapshot_tree(vm.snapshot.rootSnapshotList)

    print(f"\nSnapshots for VM '{vm.name}':")
    print("-" * 70)
    for depth, snap in flat:
        indent = "  " * depth
        created = snap.createTime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{indent}- {snap.name}  (id={snap.id}, created={created})")
        if snap.description:
            print(f"{indent}    desc: {snap.description}")
    print("-" * 70)

    return flat


def get_latest_snapshot(flat_snapshots):
    """Return the snapshot object with the most recent createTime."""
    if not flat_snapshots:
        return None
    latest = max(flat_snapshots, key=lambda item: item[1].createTime)
    return latest[1]


def wait_for_task(task, action_name="task"):
    while task.info.state in (vim.TaskInfo.State.running, vim.TaskInfo.State.queued):
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print(f"{action_name} completed successfully.")
    else:
        print(f"{action_name} failed: {task.info.error}")
        sys.exit(1)


def revert_to_snapshot(snap):
    print(f"\nReverting to snapshot '{snap.name}' (created {snap.createTime})...")
    task = snap.snapshot.RevertToSnapshot_Task()
    wait_for_task(task, "Revert")


def main():
    args = get_args()

    password = args.password or os.environ.get("VMWARE_PASSWORD")
    if not password:
        password = getpass.getpass(f"Password for {args.user}@{args.host}: ")

    si = connect(args, password)
    content = si.RetrieveContent()

    vm = find_vm_by_name(content, args.vm_name)
    if vm is None:
        print(f"VM '{args.vm_name}' not found.")
        sys.exit(1)

    flat_snapshots = list_snapshots(vm)

    if args.list_only:
        return

    if not flat_snapshots:
        print("No snapshots to revert to.")
        return

    latest = get_latest_snapshot(flat_snapshots)
    print(f"\nMost recent snapshot: '{latest.name}' (created {latest.createTime})")

    if not args.yes:
        confirm = input(f"Revert VM '{vm.name}' to this snapshot? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return

    revert_to_snapshot(latest)


if __name__ == "__main__":
    main()