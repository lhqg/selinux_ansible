Name:		ansible-selinux-devel
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	SELinux policy module for Ansible on managed hosts - devel
Vendor:   LHQG, https://www.lhqg.fr/
License:	GPLv3
URL:		https://github.com/lhqg/selinux_ansible
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

Requires:	selinux-policy-devel
Requires:	ansible-selinux = %{version}-%{release}

%description
SELinux policy development interface for Ansible on managed hosts policy module.

###################################

%clean
%{__rm} -rf %{buildroot}

###################################

%prep

if [ ! -d %{_builddir}/se_module -a -d %{_builddir}/../se_module ]
then
  ln -s %{_builddir}/../se_module %{_builddir}/
fi

###################################

%install

ls -lR %{_builddir}/
mkdir -p -m 0755 %{buildroot}/usr/share/selinux/devel/include/apps
install -m 0444 %{_builddir}/se_module/ansible.if %{buildroot}/usr/share/selinux/devel/include/apps/

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/devel/include/apps/ansible.if