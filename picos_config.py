#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Yachal Chen
# module_name: Config PicOS switch
########################################
from ansible.module_utils.basic import *
import commands
import os

module = AnsibleModule(
        argument_spec = dict(
            mode=dict(default='shell', choices=['shell', 'cli_show', 'cli_config', 'config_load']),
            cmd=dict(required=True),
        ),
)

#get the parameter name, basically, should be type in "shell", "show" or "config"
cmd = module.params['cmd']
mode = module.params['mode']

def getCmds():
    cmd = "/pica/bin/pica_sh -c 'configure;show | display set'"
    status,output = commands.getstatusoutput(cmd)
    if status==0:
        cmds_arry=re.findall("(set .*)",output)
        return cmds_arry
    else:
        result = dict(msg='can not get config',rc=status)


def checkCmds(cmds):
    cmd_arry=cmds.split(";")
    full_config_list = getCmds()
    full_config_str = ''.join(full_config_list)
    new_cmd = []
    for cmd in cmd_arry:
        if full_config_str.find(cmd.replace('\n','').replace('\r','').replace('\\','')) == -1:
            new_cmd.append(cmd)
    return new_cmd

def readConfigFile(file):
    orig_cmds_list = []
    if os.path.exists(file):
        with open(file) as cf:
            orig_cmds_list = cf.readlines()
    else:
       result = dict(msg='can not get config file',rc=False)
    orig_cmds = ";".join(orig_cmds_list)
    return orig_cmds

def generateTmpConfig(cmds):
    with open("/home/admin/ansible_config_tmp_new.conf", 'w') as config_file:
        for config_line in cmds:
            config_file.write(config_line)
    config_file.close()
    return 0

def removeTmpConfig():
    remove_cmd = "rm -f /home/admin/ansible_config_tmp_new.conf"
    removeStatus,removeOutput = commands.getstatusoutput(remove_cmd)

if mode=="shell":
    status,output = commands.getstatusoutput(cmd)
    changed_flag = False
elif mode=="cli_show":
    run_cmd = "/pica/bin/pica_sh -c \'" + cmd + "\'"
    status,output = commands.getstatusoutput(run_cmd)
    changed_flag = False
elif mode=="cli_config":
    new_cmds = checkCmds(cmd)
    if len(new_cmds)>0:
        new_cmds_str = ";".join(new_cmds)
        run_cmd = "/pica/bin/pica_sh -c \'" + "configure;" + new_cmds_str + ";commit\'"
        status,output = commands.getstatusoutput(run_cmd)
        changed_flag = True
    else:
        status = 0
        output = "Need not configure switch"
        changed_flag = False
elif mode=="config_load":
    config_path=cmd
    orig_cmds=readConfigFile(config_path)
    new_cmds = checkCmds(orig_cmds)
    if len(new_cmds)>0:
        #generate the new config file in switch after checking
        configCreate = generateTmpConfig(new_cmds)
        if configCreate == 0:
            cmd_str = "configure;execute /home/admin/ansible_config_tmp_new.conf;"
            run_cmd = "/pica/bin/pica_sh -c \'" + cmd_str + "commit\'"
            status,output = commands.getstatusoutput(run_cmd)
            if "failed" in output:
                status = 1
                changed_flag = False
            else:
                status = 0
                changed_flag = True
        else:
            output = "Failed to create temperlate config in switch."
            changed_flag = False
        # remove the temp config file after load the configuration file
        removeTmpConfig()
    else:
        status = 0
        output = "Need not configure switch"
        changed_flag = False


if status == 0:
    result = dict(module='picos_config',stdout=output,changed=changed_flag,rc=0)
    module.exit_json(**result)
else:
    result = dict(msg='execute failed',stdout=output,changed=False,rc=status)
    module.fail_json(**result)
