Name:		ansible-selinux
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	SELinux policy module for Ansible on managed hosts
Vendor:   LHQG, https://www.lhqg.fr/
License:	GPLv3
URL:		https://github.com/lhqg/selinux_ansible
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	selinux-policy-devel
BuildRequires:	make

Requires:	selinux-policy-targeted %{?_sepol_minver_cond}
Requires:	selinux-policy-targeted %{?_sepol_maxver_cond}

Requires:	policycoreutils
Requires:	policycoreutils-python-utils
Requires:	libselinux-utils

%description
SELinux policy module to confine Ansible on managed hosts.
The Ansible processes will run in the ansible_t domain.

###################################

%clean
%{__rm} -rf %{buildroot}

###################################

%prep

if [ ! -d %{_builddir}/se_module -a -d %{_builddir}/../se_module ]
then
  ln -s %{_builddir}/../se_module   %{_builddir}/
  ln -s %{_builddir}/../scripts     %{_builddir}/
  ln -s %{_builddir}/../README.md   %{_builddir}/
  ln -s %{_builddir}/../LICENSE     %{_builddir}/
  ln -s %{_builddir}/../manpages    %{_builddir}/
fi

###################################

%build

make -f /usr/share/selinux/devel/Makefile -C %{_builddir}/se_module/ clean
make -f /usr/share/selinux/devel/Makefile -C %{_builddir}/se_module/ ansible.pp

###################################

%install

ls -lR %{_builddir}/
mkdir -p -m 0755 %{buildroot}/usr/share/selinux/packages/targeted
mkdir -p -m 0755 %{buildroot}/usr/share/man/man8
mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}
mkdir -p -m 0755 %{buildroot}/%{_datarootdir}/%{name}

install -m 0555 %{_builddir}/scripts/* %{buildroot}/%{_datarootdir}/%{name}/
install -m 0444 %{_builddir}/se_module/ansible.pp %{buildroot}/usr/share/selinux/packages/targeted/
install -m 0444 %{_builddir}/se_module/ansible_u %{buildroot}/etc/selinux/targeted/contexts/users/
install -m 0444 %{_builddir}/{LICENSE,README.md} %{buildroot}/%{_docdir}/%{name}/
install -m 0444 %{_builddir}/manpages/man8/*.8 %{buildroot}/usr/share/man/man8/

make -f /usr/share/selinux/devel/Makefile -C %{_builddir}/se_module/ clean

###################################

%post

semodule -i /usr/share/selinux/packages/targeted/ansible.pp

if selinuxenabled
then
  restorecon -RFi /{opt,srv}/ansible 
  restorecon -RFi /{lib,etc}/systemd/system/ansible*
  restorecon -RFi /var/{lib,log,run,tmp}/ansible
  restorecon -RFi /usr/share/man
fi

###################################

%postun

if [ $1 -eq 0 ]
then
  semodule -l | grep -qvw ansible || semodule -r ansible
fi

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/packages/targeted/ansible.pp
/etc/selinux/targeted/contexts/users/ansible_u

%dir	%{_datarootdir}/%{name}
%{_datarootdir}/%{name}/*

%dir		%{_docdir}/%{name}
%license 	%{_docdir}/%{name}/LICENSE
%doc		%{_docdir}/%{name}/README.md
%doc		/usr/share/man/man*/*
