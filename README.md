Ansible module for PicOS

In order to help customer to easy integrate PicOS switch into Ansible, we should provide a Ansible module to customer which can display configuration, status, configure switch, and execute the Linux command in PicOS switch

Installing:
copy picos_config.py to a path and add this path into ansible.cfg e.g. 
library=/usr/share/ansible_lib/


License related:
Function: License querying, installing updating
Return:  changed-flag, status (indicate license status), Output Result( feature, model, expired date)

Linux shell related:
Function: executed the linux command in shell, some API to configure PicOS globally (PicOS_boot configuration, Port break-out configuration)
Return:  status (indicate command executed status), Output Result

PicOS show command related:
Function: executed the PicOS show xxx command
Return:  changed-flag (Usually, it will be false, except time changing …), Output Result (in default, just give the output result line by line of PicOS output, remove the useless info), but for some important display command, we should format the output, e.g. show interface, show version, show counter, show MLAG, show vlans

PicOS configuration command related:
Function: configuring the switch by configuration string,  by configuration file
Return:  changed-flag, status (indicate configuration executed status), output(actually executed configuration, some existing configuration in switch will not be executed actually.)

Some screen capture of demo PicOS ansible module (Implemented by me locally, have not upload to github)
When configure mtu with new configuration
 
Then configure the switch with same configuration, it will not be configured, and the “change” flag will be false
 
Change another configuration
 

Execute the shell command and picOS show command
 
 
![image](https://user-images.githubusercontent.com/39779637/110180508-c4909500-7dbe-11eb-8749-8c144c4d4bb2.png)
