#!/bin/bash
#########################################################
#														#
#			SELinux Ansible policy module			#
#														#
#	Restore fcontext script:							#
#		This script restores SELinux fcontexts.			#
#														#
#    https://github.com/lhqg/selinux_ansible		#
#														#
#########################################################

typset -i RC
RC=0

if selinuxenabled
then
  restorecon -RFi /{opt,srv}/ansible
  restorecon -RFi /var/{lib,log,run,tmp}/ansible
  restorecon -RFi ~ansible
  restorecon -RFi /etc/selinux/targeted/contexts/users/ansible_u
else
	echo "SElinux is not enabled, unable to restore fcontext."
	RC=1
fi

exit $RC
