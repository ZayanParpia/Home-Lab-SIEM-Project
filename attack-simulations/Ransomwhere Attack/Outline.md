\# Ransomware Detection \& Automated Response — Project Outline



\*\*Goal:\*\* Simulate a ransomware attack in a controlled lab, detect it in Wazuh via

File Integrity Monitoring (FIM) + auditd process tracking, and trigger a SOAR

response that kills the offending process, deletes the executable, and restores

affected files from a snapshot backup.



\*\*MITRE ATT\&CK mapping:\*\* T1486 — Data Encrypted for Impact (Impact tactic)

Supporting techniques to reference in the writeup:

\- T1059 — Command and Scripting Interpreter (executing the encryptor)

\- T1489 — Service Stop (optional, if you kill security/backup services first)

\- T1490 — Inhibit System Recovery (optional, if you simulate shadow-copy/backup deletion before your defense stops it)



\*\*Atomic Red Team tests to reference/run (validates detections against a known framework, not just your own script):\*\*

\- T1486 — atomics include a PowerShell/Windows-focused ransomware simulation; for Linux you can note it was referenced for technique alignment even though you built a custom Linux-native simulator

\- T1490 — includes tests for deleting Volume Shadow Copies / backups, useful if you want to demonstrate detecting backup-tampering attempts too



\---



\## Phase 1: Build the Attack (Days 1–3)



\### 1. Build the safe ransomware simulator

Fernet-based Python script (`cryptography` library) that recursively encrypts

a test folder and drops a `ransom\_note.txt`. Keep it self-contained with a

matching decrypt function for demo/reset purposes.

\- Run locally on the victim, or

\- Push and execute it via a reverse shell from Kali (see Kali tools below) to

&#x20; simulate a real initial-access → execution chain



\### 2. Set up snapshot backups

Cron job (every 15–30 min) that rsyncs the target folder to a timestamped

backup directory: `/backup/snapshots/<timestamp>/`. This is the "previous

version" the SOAR response restores from.



\---



\## Phase 2: Detection (Days 4–7)



\### 3. Enable Wazuh FIM + auditd process tracking

\- `syscheck` real-time monitoring on the target directory (catches mass file

&#x20; changes)

\- auditd watch rule on the same directory: `-w /path -p wa -k ransomware\_watch`

&#x20; so the `exe=` field (actual binary responsible) and PID are captured

\- Confirm Wazuh is ingesting auditd logs via the audit log collector



\### 4. Write the correlation rule

In `local\_rules.xml`: fire a high-severity alert when many FIM

modify/rename events hit the same directory within a short timeframe (e.g.

20+ changes in 10 seconds). Correlate with the auditd event so the alert

payload includes the offending process's `exe` path and PID — this is what

your active response script will act on.



\### 5. Validate detection end-to-end

Trigger the simulator and confirm:

\- The correlation rule fires (not just individual FIM events)

\- The alert includes the exe path and PID, not just "files changed"

\- Time from first encrypted file to alert firing is captured (useful metric

&#x20; for the writeup)



\---



\## Phase 3: Response (Days 8–11)



\### 6. Build the kill + delete + restore response

Wazuh Active Response script triggered by the rule:

1\. Kill the PID

2\. Delete or quarantine the executable at the `exe` path pulled from the alert

3\. rsync the most recent clean snapshot back over the target folder



Keep a copy of your simulator script outside the target directory (e.g. in

git) since step 2 will delete it as part of the correct behavior.



\### 7. Wire up SOAR notification

Wazuh webhook → Shuffle (or n8n) → Slack/email alert including:

\- What was killed (PID, exe path)

\- What was deleted

\- Which snapshot was restored and its timestamp

\- Optional: auto-create a case/ticket for the "incident"



\---



\## Phase 4: Documentation (Days 12–14)



\### 8. Document for the portfolio

\- MITRE ATT\&CK mapping (T1486, plus any supporting techniques used)

\- Note on Atomic Red Team tests referenced for technique validation

\- Architecture diagram (attacker → victim → Wazuh → SOAR → notification)

\- Before/after screenshots: encrypted files → process killed → files restored

\- Short demo video/GIF showing the full detect → respond → restore loop

\- README with setup steps, so it's reproducible



\---



\## Kali Linux Tools (if simulating delivery/execution from Kali)



\- \*\*Netcat / Metasploit (msfvenom)\*\* — establish a reverse shell to the victim

&#x20; to execute the ransomware simulator remotely, simulating a real

&#x20; execution-after-compromise chain

\- \*\*Atomic Red Team\*\* — optional, to run standardized technique tests

&#x20; alongside your custom simulator for detection validation

