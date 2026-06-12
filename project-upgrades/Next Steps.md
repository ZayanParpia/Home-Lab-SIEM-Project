\## Endpoint Expansion \& Monitoring Configuration



\### Virtualized Endpoints (VMware)



\#### Security Monitoring Lab

\- Add \*\*2 Ubuntu CLI endpoints\*\* using VMware.

\- Add \*\*1 Ubuntu CLI endpoint\*\* and \*\*1 Windows endpoint\*\* using VMware on the gaming laptop.



\### Endpoint Logging \& Telemetry



\#### Windows Endpoints

\- Install \*\*Sysmon\*\* on all Windows endpoints.



\#### Linux Endpoints

\- Install \*\*Sysmon for Linux\*\* on all Ubuntu endpoints.

\- Install \*\*auditd\*\* on all Linux endpoints for system auditing and event loggin

\- configure new endpoints to have auditd and Sysmon connected to Wazuh Server Logs



\### Wazuh Integration



\#### Centralized Monitoring

\- Connect all endpoints to the \*\*Wazuh Server\*\*.

\- Verify successful agent registration and communication.

\- Confirm log ingestion from:

&#x20; - Sysmon (Windows)

&#x20; - Sysmon for Linux

&#x20; - auditd

\- Validate all endpoints are functional and visible within the Wazuh dashboard.



\### STEPS FOR 2026-06-10

\- Installed and configured \*\*Sysmon for Linux\*\* on Endpoint IV. ✅

\- Installed and configured \*\*auditd\*\* on Endpoint IV. ✅



\### STEPS FOR 2026-06-11



\- Connected Ubuntu Endpoint IV to the \*\*Wazuh Server\*\*. ✅

\- Verified that endpoint IV is actively reporting to Wazuh. ✅

\- Confirmed log collection and endpoint visibility within the Wazuh dashboard. ✅



\### STEPS FOR 2026-06-12

* Set up Sysmon for Windows on Windows Endpoint ✅



\### STEPS FOR 2026-06-13

* Ensure that Sysmon is sending logs to Wazuh Server

