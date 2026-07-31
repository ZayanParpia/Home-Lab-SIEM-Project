import sys
import json
import subprocess
import os

LOG_FILE = "/var/ossec/logs/active-responses.log"

def log_action(message):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"SOAR-100012: {message}\n")
    except Exception:
        pass

def main():
    log_action("Script triggered by Wazuh.")

    try:
        raw_input = sys.stdin.read()
        alert = json.loads(raw_input)
    except Exception as e:
        log_action(f"Failed to parse input JSON: {e}")
        sys.exit(1)

    command = alert.get("command")
    parameters = alert.get("parameters", {})
    alert_info = parameters.get("alert", {})
    data_field = alert_info.get("data", {})

    # Extract source IP specifically pointing to data.srcip from Rule 100010 / 100012 payload context
    src_ip = (
        data_field.get("srcip") or
        alert_info.get("data", {}).get("srcip") or
        parameters.get("srcip") or
        alert_info.get("srcip")
    )

    user = "SSHATTACK"
    log_action(f"Target User: {user}, Extracted Attacker IP: {src_ip}")

    if command != "add":
        sys.exit(0)

    # Action 1: Remove/Ensure Authorized Keys file exists and clear it
    try:
        home_dir = f"/home/{user}"
        ssh_dir = os.path.join(home_dir, ".ssh")
        auth_keys_path = os.path.join(ssh_dir, "authorized_keys")

        os.makedirs(ssh_dir, exist_ok=True)
        with open(auth_keys_path, "w") as f:
            f.write("")
        os.chmod(ssh_dir, 0o700)
        os.chmod(auth_keys_path, 0o600)
        subprocess.run(["chown", "-R", f"{user}:{user}", ssh_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        log_action(f"SUCCESS: Reset and cleared {auth_keys_path}")
    except Exception as e:
        log_action(f"ERROR managing authorized keys: {e}")

    # Action 2: Reset User Password
    try:
        new_password = "NEWPASSWORD2468"
        passwd_process = subprocess.run(
            ["/usr/sbin/chpasswd"],
            input=f"{user}:{new_password}".encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if passwd_process.returncode == 0:
            log_action(f"SUCCESS: Reset password for user: {user}")
            subprocess.run(["/usr/bin/passwd", "-e", user], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            log_action(f"ERROR resetting password: {passwd_process.stderr.decode()}")
    except Exception as e:
        log_action(f"ERROR setting emergency password: {e}")

    # Action 3: Block Network Traffic via iptables
    if src_ip and src_ip != "-" and src_ip != "None":
        try:
            check_rule = subprocess.run(["/usr/sbin/iptables", "-C", "INPUT", "-s", src_ip, "-j", "DROP"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if check_rule.returncode != 0:
                subprocess.run(["/usr/sbin/iptables", "-A", "INPUT", "-s", src_ip, "-j", "DROP"], check=True)
                log_action(f"SUCCESS: Blocked source IP via iptables: {src_ip}")
            else:
                log_action(f"NOTICE: IP {src_ip} is already blocked.")
        except Exception as e:
            log_action(f"ERROR applying network block for {src_ip}: {e}")
    else:
        log_action(f"NOTICE: Skipping IP block, invalid src_ip: {src_ip}")

    # Action 4: Terminate Active Sessions
    try:
        subprocess.run(["/usr/bin/pkill", "-u", user], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_action(f"SUCCESS: Terminated active sessions for user: {user}")
    except Exception as e:
        log_action(f"ERROR terminating sessions: {e}")

    log_action("SOAR Response execution cycle finished for Rule 100012.")
    sys.exit(0)

if __name__ == "__main__":
    main()