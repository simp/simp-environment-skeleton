# policycoreutils_version and selinux_policy_version are specifically set
# to the *earliest* version of these packages present in these major releases.
#
# This is required since SELinux policies are forward compatible during a major
# release but not necessarily backwards compatible and we want to ensure
# maximum package compatibility.
#
# Use environment variable SIMP_ENV_NO_SELINUX_DEPS to ignore this
# and use the latest.  (This is good when building test ISOs that
# from a local environment, instead of a docker build, where a later
# version of selinux is installed.)
%define ignore_selinux_reqs %{getenv:SIMP_ENV_NO_SELINUX_DEPS}

# Only run the following if the environment variable is *not* defined
%if "%{ignore_selinux_reqs}" == ""
  %if 0%{?rhel} == 6 || 0%{?rhel} == 7
    %if 0%{?rhel} == 6
      %global policycoreutils_version 2.0.83
      %global selinux_policy_version 3.7.19
    %endif

    %if 0%{?rhel} == 7
      %global policycoreutils_version 2.2.5
      %global selinux_policy_version 3.12.1
    %endif
  %endif
%endif

%global selinux_variants targeted

%define selinux_policy_short simp-environment
%define selinux_policy %{selinux_policy_short}.pp

Summary: The SIMP Environment Skeleton
Name: simp-environment-skeleton
Version: 7.0.0
Release: 0%{?dist}
License: Apache License 2.0
Group: Applications/System
Source: %{name}-%{version}-%{release}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes: simp-environment < %{version}

Buildarch: noarch

Prefix: /usr/share/simp/environment-skeleton

%package -n simp-environment-selinux-policy
Summary: SELinux Policy for deployed SIMP environment resources
Version: 1.0.0
Release: 0%{?dist}
License: Apache License 2.0
Requires: libselinux-utils
Requires: policycoreutils
Requires(post): glibc-common
Requires(post): libsemanage
%if 0%{?selinux_policy_version:1}
Requires(post): selinux-policy >= %{selinux_policy_version}
Requires(post): selinux-policy-targeted >= %{selinux_policy_version}
%else
Requires(post): selinux-policy
Requires(post): selinux-policy-targeted
%endif
Requires(post,postun): policycoreutils
BuildRequires: selinux-policy-targeted
%if 0%{?selinux_policy_version:1}
BuildRequires: policycoreutils == %{policycoreutils_version}
BuildRequires: policycoreutils-python == %{policycoreutils_version}
BuildRequires: selinux-policy == %{selinux_policy_version}
BuildRequires: selinux-policy-devel == %{selinux_policy_version}
  %if 0%{?rhel} == 7
BuildRequires: policycoreutils-devel == %{policycoreutils_version}
  %endif
%else
BuildRequires: policycoreutils
BuildRequires: policycoreutils-python
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
  %if 0%{?rhel} == 7
BuildRequires: policycoreutils-devel
BuildRequires: selinux-policy-targeted
  %endif
%endif

%description

Contains template files and directories for initially setting up a SIMP server
using a default 'simp' Puppet Environment.

%description -n simp-environment-selinux-policy

Provides SELinux policies suitable for configuring permissions on SIMP provided
environment data.

%prep
%setup -q

%build
cd build/selinux
  make -f %{_datadir}/selinux/devel/Makefile
cd -

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# Make your directories here.
mkdir -p %{buildroot}/%{prefix}/simp/data/hostgroups
mkdir -p %{buildroot}/%{prefix}/writable/simp_autofiles
mkdir -p %{buildroot}/%{prefix}/secondary/site_files/krb5_files/files/keytabs
mkdir -p %{buildroot}/%{prefix}/secondary/site_files/pki_files/files/keydist/cacerts

# Now install the files.

cp -r environments/* %{buildroot}/%{prefix}

# Handle the SELinux materials
cd build/selinux
  install -p -m 644 -D %{selinux_policy} %{buildroot}/%{_datadir}/selinux/packages/%{selinux_policy}
cd -

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0640,root,root,0750)
%{prefix}
%attr(0750,-,-) %{prefix}/writable/simp_autofiles

%attr(0750,-,-) %{prefix}/secondary/site_files
%attr(0750,-,-) %{prefix}/secondary/site_files/krb5_files
%attr(0750,-,-) %{prefix}/secondary/site_files/krb5_files/files
%attr(0750,-,-) %{prefix}/secondary/site_files/krb5_files/files/keytabs
%attr(0750,-,-) %{prefix}/secondary/site_files/pki_files
%attr(0750,-,-) %{prefix}/secondary/site_files/pki_files/files
%attr(0750,-,-) %{prefix}/secondary/site_files/pki_files/files/keydist
%attr(0750,-,-) %{prefix}/secondary/site_files/pki_files/files/keydist/cacerts

%{prefix}/simp
%attr(0750,-,-) %{prefix}/simp
%{prefix}/simp/environment.conf
%{prefix}/simp/hiera.yaml
%{prefix}/simp/data/hosts/puppet.your.domain.yaml
%{prefix}/simp/data/hostgroups/default.yaml
%{prefix}/simp/data/scenarios/simp.yaml
%{prefix}/simp/data/scenarios/simp_lite.yaml
%{prefix}/simp/data/scenarios/poss.yaml
%{prefix}/simp/data/default.yaml
%{prefix}/simp/manifests/site.pp

%{prefix}/secondary/FakeCA
%{prefix}/secondary/FakeCA/togen
%{prefix}/secondary/FakeCA/usergen
%{prefix}/secondary/FakeCA/ca.cnf
%{prefix}/secondary/FakeCA/user.cnf
%{prefix}/secondary/FakeCA/clean.sh
%{prefix}/secondary/FakeCA/gencerts_common.sh
%{prefix}/secondary/FakeCA/gencerts_nopass.sh
%{prefix}/secondary/FakeCA/usergen_nopass.sh
%attr(0750,-,-) %{prefix}/secondary/FakeCA/clean.sh
%attr(0750,-,-) %{prefix}/secondary/FakeCA/gencerts_common.sh
%attr(0750,-,-) %{prefix}/secondary/FakeCA/gencerts_nopass.sh
%attr(0750,-,-) %{prefix}/secondary/FakeCA/usergen_nopass.sh

%files -n simp-environment-selinux-policy
%defattr(0640,root,root,0750)
%{_datadir}/selinux/*/%{selinux_policy}

%post -n simp-environment-selinux-policy
# Build an load policy to set selinux context to enable puppet
# to read from /var/simp directories.
/usr/sbin/semodule -n -i %{_datadir}/selinux/packages/%{selinux_policy}
if /usr/sbin/selinuxenabled; then
  /usr/sbin/load_policy
  /sbin/fixfiles -F -R %{name} restore || :
fi

%postun -n simp-environment-selinux-policy
# Post uninstall stuff
if [ $1 -eq 0 ]; then
  /usr/sbin/semodule -n -r %{selinux_policy_short}
  if /usr/sbin/selinuxenabled; then
    /usr/sbin/load_policy
    /sbin/fixfiles -R %{name} restore || :
  fi
fi

%changelog -n simp-environment-selinux-policy
* Tue Apr 30 2019 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.0.0-0
- Creation of a new simp-environment-skeleton package (7.0.0)
- Creation of a new simp-environment-selinux-policy subpackage (1.0.0)
