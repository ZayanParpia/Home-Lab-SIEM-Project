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

\- Install \*\*auditd\*\* on all Linux endpoints for system auditing and event logging.



\### Wazuh Integration



\#### Centralized Monitoring

\- Connect all endpoints to the \*\*Wazuh Server\*\*.

\- Verify successful agent registration and communication.

\- Confirm log ingestion from:

&#x20; - Sysmon (Windows)

&#x20; - Sysmon for Linux

&#x20; - auditd

\- Validate all endpoints are functional and visible within the Wazuh dashboard.





