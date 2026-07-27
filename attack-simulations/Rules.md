\# 🚨 Rule: Sudo Password Guessing Detection



\*\*Rule ID:\*\* `100002`

\*\*Severity Level:\*\* `10`

\*\*Category:\*\* Privilege Escalation / Password Guessing

\*\*MITRE ATT\&CK:\*\* `T1110 - Brute Force`



\## Description



This rule detects potential \*\*sudo privilege escalation password guessing\*\* attempts.



The rule monitors for Wazuh rule \*\*5557\*\* (`Failed Password Attempt`). If this event occurs \*\*3 times within 2 minutes (120 seconds)\*\*, Wazuh triggers \*\*rule 100002\*\* with a severity level of \*\*10\*\*, indicating a possible brute-force attack against sudo authentication.



\## Detection Logic



\* \*\*Base Rule:\*\* `5557` (Failed Password Attempt)

\* \*\*Threshold:\*\* `3` failed attempts

\* \*\*Time Window:\*\* `120` seconds

\* \*\*Triggered Rule:\*\* `100002`

\* \*\*Severity:\*\* `10`



\## Wazuh Rule Configuration



```xml

<group name="Password-Guessing">

&#x20; <rule id="100002" level="10" frequency="3" timeframe="120">

&#x20;   <if\_matched\_sid>5557</if\_matched\_sid>

&#x20;   <description>Sudo Password Guessing: 3 failed password attempts detected.</description>

&#x20;   <group>authentication\_failed,pci\_dss\_10.2.4</group>

&#x20; </rule>

</group>

```



\## Alert Conditions



An alert is generated when:



1\. A user enters an incorrect sudo password.

2\. Wazuh generates rule `5557`.

3\. Rule `5557` occurs three times within 120 seconds.

4\. Rule `100002` is triggered.



\## Security Impact



Successful password guessing attacks could allow an attacker to:



\* Gain elevated privileges.

\* Perform unauthorized administrative actions.

\* Establish persistence on the system.

\* Move laterally within the environment.



\## Recommended Response



\* Identify the source user and host.

\* Review authentication logs for additional failed attempts.

\* Determine whether the activity was legitimate or malicious.

\* Lock or monitor the affected account if necessary.

\* Consider implementing account lockout policies or multi-factor authentication.



<!-- SSH Attack -->

<group name="Brute Force Detection,Possible Unauthorized Access,FIM trigger,">

  <!-- Rule 100010: SSH Brute Force -->
  <rule id="100010" level="10" frequency="3" timeframe="60">
    <if_matched_sid>5710</if_matched_sid>
    <same_srcip />
    <description>SSH brute force attack detected from a single source IP</description>
    <mitre>
      <id>T1098.004</id>
    </mitre>
    <group>unauth_access_trigger</group>
  </rule>

<!-- Scanning test -->

  <rule id="86601" level="3" overwrite="yes">
     <if_sid>86600</if_sid>
     <field name="event_type">^alert$</field>
     <description>Suricata: Alert - $(alert.signature)</description>
     <options>no_full_log</options>
     <group>unauth_access_trigger</group>
  </rule>

  <!-- Rule 100011: Unauthorized Access -->
  <rule id="100011" level="10" timeframe="900">
    <if_sid>5715</if_sid>
    <if_matched_group>unauth_access_trigger</if_matched_group>
    <same_srcip />
    <description>Possible Unauthorized User inside Machine</description>
    <mitre>
      <id>T1110.001</id>
      <id>T1021.004</id>
    </mitre>
    <group>unauth_access_trigger</group>

  </rule>

  <!-- Rule 100012: FIM Trigger -->
  <rule id="100012" level="10" timeframe="900">
    <if_sid>550</if_sid>
    <if_matched_group>unauth_access_trigger</if_matched_group>
    <description>Unauthorized Added key inside /.ssh/authorized_keys, initiating machine lockdown</description>
    <mitre>
      <id>T1098.004</id>
    </mitre>
  </rule>

</group>

