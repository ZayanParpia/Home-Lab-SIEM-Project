2026-07-05



Created username and password list to brute force using hydra

Tested Hydra on Endpoint IV

Successful SSH brute force attack

Saw logs on SIEM system



2026-07-06

Simulated Attack again and this time captured on Wazuh



2026-07-09

Today I edited the videos of the DEMO(s)



2026-07-10

Today I ran into a problem where I cant find the keys for when I logged into ssh, I then learned that I used password login instead of key login, I can add a new part of this attack simulation by enabling key login and generating a new key to copy, so now I learned about that attack vector aswell, where a bad actor can enable key login and use a key to login instead of a password or vise versa.



I ran cat /etc/ssh/sshd\_config to see if key authentication is enabled

I learned that it is already enabled, so I just have to generate a new key and save it



I ran ssh-keygen -t ed25519 to generate a new key



Its not working so im going to watch a tutorial on how to use SSH key login

I watched a tutorial and learned that, to generate ssh keys I type ssh-keygen -t Encryption Algorithm, then to add it to the server I do ssh-copy-id USERNAME@USERNAME



2026-07-12



Today I documented what happens when I add a ssh key to the authorized key file for ssh and I saw I could login even though the password was changed. I also saw that it wasn't being detected on the SIEM so I edited the ossec.conf so that it monitors that file for changes



2026-07-14

Today I reset my vms to be fresh when I initiate the real attack vector.



2026-07-15

Today I downloaded suricata so that my wazuh can see the nmap scans. I changed the ossec.conf file so that it attaches to it properly.



2026-07-16

Today I configured suricata by adding a custom rule where if any scanner touches port 22, it triggers and alert.

alert tcp any any -> any 22 (msg:"SIEM PROJECT: Nmap Scan to SSH Port 22"; flags:S; sid:1000002; rev:1;)

I also made the rule for this entire attack simulation, I learned to read the docs and do it all myself



