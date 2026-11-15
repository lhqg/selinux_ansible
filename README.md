![GitHub Release (latest SemVer)](https://img.shields.io/github/v/release/lhqg/XXXXXXXX)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![GitHub Issues](https://img.shields.io/github/issues/lhqg/XXXXXXXX)](https://github.com/lhqg/XXXXXXXX/issues)
[![GitHub PR](https://img.shields.io/github/issues-pr/lhqg/XXXXXXXX)](https://github.com/lhqg/XXXXXXXX/pulls)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/lhqg/XXXXXXXX)](https://github.com/lhqg/XXXXXXXX/commits/main)
[![GitHub Last commit](https://img.shields.io/github/last-commit/lhqg/XXXXXXXX)](https://github.com/lhqg/XXXXXXXX/commits/main)
![GitHub Downloads](https://img.shields.io/github/downloads/lhqg/XXXXXXXX/total)

# SELinux policy policy modules for LHQG

Maintained and provided as a community contribution by [LHQG](https://www.lhqg.fr/).

## Table of Contents

1. [Introduction](#introduction)
2. Basic Ansible SELinux policy module
3. (Dangerous) Unconfined Ansible policy modules
4. [Disclaimer](#disclaimer)

## Introduction

Security-Enhanced Linux (SELinux) secures Ansible actions via flexible
mandatory access control (MAC).

For Linux system administrators, Ansible is a very powerful tool to manage and
automate the deployment and configuration of their managed hosts.

Yet, "with great power comes great responsibility"... So, system administrators
must be careful when using Ansible to manage their machines and make sure that
Ansible is not misused by malicious users to compromise their managed hosts nor
to exfiltrate sensitive information from them.

To help them secure their managed hosts, implement the information security
policies of their organization, apply the principle of least privilege and
reduce the surface of attack of their managed hosts, the [LHQG](https://www.lhqg.fr/)
company has developed an open source SELinux policy module to confine
the Ansible processes on the managed hosts.

The basic idea is to confine the Ansible processes in a dedicated SELinux domain
and to define a set of SELinux rules to restrict the access of these processes
to the managed host resources (files, directories, network ports, other
processes...).

## Basic Ansible SELinux policy module

### Confining the Ansible processes

#### Entrypoints

Since Ansible is a framework and not a single binary, there is no binary entry
point to the ansible_t SELinux type/domain.

#### Linux user (SELinux login) mapping to SELinux user

The selinux_ansible policy module defines the `ansible_u` SELinux user and
the `ansible_r` SELinux role.

For Ansible processes to be effectively confined in the
`ansible_u:ansible_r:ansible_t`
SELinux context when the Ansible runner connects to the managed host, system
administrators must map the Linux account used by the Ansible runner
host/platform uses.

For instance, if the Ansible runner connects to the managed host with the
`ansible` account, this account must be mapped to the `ansible_u`
SELinux user.

##### SELinux login "global" mapping

The Linux account used by Ansible can be mapped regardless of the method (PAM
service) it connects to the managed host.

Such SELinux login mapping are managed using the `semanage login` command.

For example:
```semanage login --add -s ansible_u -r s0 ansible```

##### SELinux login method/service specific mapping

The Linux account used by Ansible can be mapped for a specific method (PAM
service) it connects to the managed host with.

Such SELinux login mapping are managed deploying a text file in the
`/etc/selinux/targeted/login` directory.

The file name must be the Linux account name used by Ansible to connect to the
managed host.

This file contains one line per specific method/service to map the Linux
account. Each line must comply with the following format:

`<SELinux login>:<SELinux user>:<SELinux level range>`

For example:
File `/etc/selinux/targeted/logins/ansible` to map the `ansible` Linux user when connected via SSHd:
```sshd:ansible_u:s0```

#### Process types

SELinux defines process types (domains) for each process running on the system.
Policy governs the access confined processes have to files/directories and all

## (Dangerous) Unconfined Ansible policy modules

When confronted with a situation where the SELinux confinement by the _normal_
LHQG ansible SELinux policy module deployed on the managed hosts is too
restrictive for the Ansible processes to perform all their legitimate tasks,
system administrators can decide to run Ansible in an unconfined mode on the
managed hosts.

### WARNING: Running Ansible in an unconfined mode is NOT RECOMMENDED

Running Ansible in an unconfined mode on the managed hosts means that the
Ansible processes are not confined by SELinux and can perform **any**
access on **any** resource on the managed hosts, and can perform **any**
action on the host itself.

The security of the managed hosts is then fully dependent on the DAC
(Discretionary Access Control) permissions setup on the managed hosts, and
restricted only by the privileges of the Linux user running the Ansible
processes.

The Ansible processes can then be misused by malicious users to compromise the
managed hosts and/or to exfiltrate sensitive information from them.

The Ansible processes can then be misused by malicious users to disrupt the
services running on the managed hosts.

### DISCLAIMER: Running Ansible in an unconfined mode is DANGEROUS

Only system administrators who are fully aware of the security implications of
running Ansible in an unconfined mode on the managed hosts should consider this
option.

Should you decide to run Ansible in an unconfined mode on the hosts you
manage, you do so at your own risk and the LHQG company cannot be held
responsible for any damage or loss of data that may occur.

### WARNING: Lack of traceability of Ansible actions on the managed hosts

When Ansible is run in an unconfined mode on the managed hosts, the Ansible
processes actions and accesses on the managed hosts are not logged by SELinux
and it will be almost impossible to differentiate between legitimate and
malicious actions on the managed hosts.

Making the `ansible_t` process type unconfined

Making the `ansible_sudo_t` process type unconfined

## Disclaimer

The code of the project module is provided AS-IS. People and organisation
willing to use it must be fully aware that they are doing so at their own risks and
expenses.

The Author(s) of this code SHALL NOT be held liable nor accountable, in
 any way, of any malfunction or limitation of said module, nor of the resulting damage, of
 any kind, resulting, directly or indirectly, of the usage of this code.

It is strongly advised to always use the last version of the code, to check for the
compatibility of the platform where it is about to be deployed, to compile the module on
the target specific Linux distribution and version where it is intended to be used.

Finally, users should check regularly for updates.
