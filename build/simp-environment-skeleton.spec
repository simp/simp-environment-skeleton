Summary: The SIMP Environment Skeleton
Name: simp-environment-skeleton
Version: 7.2.1
Release: 1
# The entire source code is Apache License 2.0 except the following, which are
# OpenSSL:
#  * environments/secondary/FakeCA/CA
#  * environments/secondary/FakeCA/CA_batch
License: Apache License 2.0 and OpenSSL
Group: Applications/System
Source: %{name}-%{version}-%{release}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes: simp-environment < %{version}
Requires: simp-selinux-policy

Buildarch: noarch

Prefix: /usr/share/simp/environment-skeleton

%description

Contains template files and directories for initially setting up a SIMP server
using a default 'simp' Puppet Environment.

%prep
%setup -q

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# Make your directories here.
mkdir -p %{buildroot}/%{prefix}/puppet/data/hostgroups
mkdir -p %{buildroot}/%{prefix}/writable/simp_autofiles
mkdir -p %{buildroot}/%{prefix}/secondary/site_files/krb5_files/files/keytabs
mkdir -p %{buildroot}/%{prefix}/secondary/site_files/pki_files/files/keydist/cacerts

# Now install the files.

cp -r environments/* %{buildroot}/%{prefix}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0644,root,root,755)
%{prefix}
%{prefix}/writable/simp_autofiles

%{prefix}/secondary/site_files
%{prefix}/secondary/site_files/krb5_files
%{prefix}/secondary/site_files/krb5_files/files
%{prefix}/secondary/site_files/krb5_files/files/keytabs
%{prefix}/secondary/site_files/pki_files
%{prefix}/secondary/site_files/pki_files/files
%{prefix}/secondary/site_files/pki_files/files/keydist
%{prefix}/secondary/site_files/pki_files/files/keydist/cacerts

%{prefix}/puppet
%{prefix}/puppet/environment.conf.TEMPLATE
%{prefix}/puppet/hiera.yaml
%{prefix}/puppet/data/hosts/puppet.your.domain.yaml
%{prefix}/puppet/data/hosts/pe-puppet.your.domain.yaml
%{prefix}/puppet/data/hostgroups/default.yaml
%{prefix}/puppet/data/scenarios/simp.yaml
%{prefix}/puppet/data/scenarios/simp_lite.yaml
%{prefix}/puppet/data/scenarios/poss.yaml
%{prefix}/puppet/data/default.yaml
%{prefix}/puppet/manifests/site.pp

%{prefix}/secondary/FakeCA
%{prefix}/secondary/FakeCA/togen
%{prefix}/secondary/FakeCA/usergen
%{prefix}/secondary/FakeCA/ca.cnf
%{prefix}/secondary/FakeCA/user.cnf
%attr(0755,-,-) %{prefix}/secondary/FakeCA/CA
%attr(0755,-,-) %{prefix}/secondary/FakeCA/clean.sh
%attr(0755,-,-) %{prefix}/secondary/FakeCA/gencerts_common.sh
%attr(0755,-,-) %{prefix}/secondary/FakeCA/gencerts_nopass.sh
%attr(0755,-,-) %{prefix}/secondary/FakeCA/usergen_nopass.sh

%changelog
* Tue Feb 02 2021 Liz Nemsick <lnemsick.simp@gmail.com> - 7.2.1-1
- Removed the obsolete `simp_options::clamav` setting from all hieradata
  files.
- Updated the FakeCA README.

* Wed Nov 04 2020 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.2.0-1
- Ensure that firewalld is used by default in the applicable SIMP scenarios.
- Bump the Release to '1' in the RPM spec file since this is stable.

* Tue Sep 01 2020 Liz Nemsick <lnemsick.simp@gmail.com> - 7.1.4-0
- Fixed a bug in which the FakeCA CA script was not executable.

* Wed Aug 26 2020 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.1.4-0
- Ensure that the server hieradata defaults have 'simp::server' in the
  'simp::classes' array. Otherwise, it will never get picked up.

* Wed Jun 22 2020 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.1.3-0
- Replace `classes` with `simp::classes` and `simp::server::classes` as
  appropriate in example Hiera YAML files.

* Mon Mar 23 2020 Jeanne Greulich <jeanne.greulich@onyxpoint.com> - 7.1.2-0
- FakeCA Updates
  - When running in batch mode do not request input from the user.

* Sat Oct 26 2019 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.1.2-0
- FakeCA Updates
  - Allow users to specify an alternate output directory via a KEYDIST
    environment variable
  - Consolidate the certificate request and revocation code
  - Certificate revocation now runs in linear time

* Fri Sep 27 2019 Michael Morrone <michael.morrone@onyxpoint.com> - 7.1.1-0
- Changed permissions for files and directories to be world readable
- Removed executable permissions from non-script files

* Mon Sep 02 2019 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.1.1-0
- Add a PE-suitable puppet YAML data template.

* Wed Jun 26 2019 Trevor Vaughan <tvaughan@onyxpoint.com> - 7.1.0-0
- Rename the package to 'simp-environment-skeleton' to more accurately portray
  its purpose.
- Remove all SELinux components and add a dependency on 'simp-selinux-policy'
- Rename `simp` environment directory to `puppet`
- Rename template `environment.conf` `environment.conf.template` and
  within that file, rename the `simp` environment string to
  %%SKELETON_ENVIRONMENT%%.

* Tue Apr 09 2019 Jeanne Greulich <jeanne.greulich@onyxpoint.com> - 7.0.0-0
- Reworked packaging so this RPM no longer modifies files used by a user's
  'simp' Puppet environment
  - Changed installation directory from %{_var} file to %{prefix} for the
    subset of file previously installed there.  All files are
    now installed in /usr/share/simp as an example, only.
  - Removed OBE %config(noreplace) directives on files previously installed
    in /var/simp/environments/simp.
  - Removed erroneous %config(noreplace) directives on files installed
    in /usr/share/simp/environments/simp.
  - Removed actions that will be implemented by a simp cli command
    - selinux fixfiles on the /var/simp directory during installation.
    - cacertkey creation from post install.
    - Calls to the RPM helper script in the %post and %postun sections.
      This means the default environment is no longer copied into
      /etc/puppetlabs/code/environments/simp upon initial install, and no longer
      removed from that directory upon erase.

* Tue Apr 09 2019 Liz Nemsick <lnemsick.simp@gmail.com> - 6.3.1-0
- `simp_options::ldap` now defaults to `false` in the simp and simp_lite
  scenarios, because use of LDAP is not required.  This change
  is important for sites that do not use LDAP at all or use a different
  implementation of LDAP that does not match the schemas provided by
  SIMP.

* Fri Feb 15 2019 Michael Riddle <michael.riddle@onyxpoint.com> - 6.3.1-0
- If the gencerts scripts are called via sudo, puppet won't be in the path.
  Added the fully qualified path to the puppet binary to remedy this issue.

* Thu Jul 26 2018 Nick Miller <nick.miller@onyxpoint.com> - 6.3.0-0
- Added a default Hiera 5 hiera.yaml.
- Renamed environments/simp/hieradata/ to environments/simp/data/ to support
  staged rollout of environment-specific hiera.yaml use.
- Removed the OBE environments/simp/hieradata/compliance_profiles directory
  and references to it.
- Removed unnecessary package dependencies to make installation more portable.
- Only use simp_rpm_helper to copy files installed in /usr/share/simp/environments
  into /etc/puppetlabs/code/environments/simp, as appropriate, if this is an
  initial install.
- Only use simp_rpm_helper to remove file copies that reside in
  /etc/puppetlabs/code/environments/simp, as appropriate, if this is an erase.

* Mon Jul 16 2018 Jeanne Greulich <jeanne.greulich@onyxpoint.com> - 6.2.10-0
- Added force option to the selinux fixfiles command in the post install
  section.  If this is not set, only the type context is restored, even
  though the user context is also set in the selinux policy.
- Removed logic to link production environment to simp environment.  This
  is done in 'simp config', if it is needed.
- Updated rsync version required to 6.2.  Selinux code was moved from
  simp-rsync to simp-environment at that time and using older versions can
  cause unexpected results in the selinux policy.

* Wed Apr 25 2018 Jeanne Greulich <jeanne.greulich@onyxpoint.com> - 6.2.9-0
- Remove the simp_options::selinux variable from the scenario hieradata.

* Thu Mar 08 2018 Liz Nemsick <lnemsick.simp@gmail.com> - 6.2.8-0
- Pre-populate the /var/simp/environments/simp/site_files/pki_files/
  directory tree and set its ownership and permissions appropriately.
  This is part of the fix to the failure of SIMP to bootstrap on
  a system on which root's umask has already been restricted to 077.

* Fri Dec 15 2017 Chris Tessmer <chris.tessmer@onyxpoint.com> - 6.2.8-0
- Add the 'dist' to the package release to account for the SELinux version
  restrictions

* Fri Nov 17 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.2.7-0
- Enable the UDP localhost rsyslog server on the puppetserver to capture
  messages from the puppet services for processing and forwarding

* Fri Nov 03 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.2.6-0
- Ensure that FakeCA works properly with Puppet Enterprise
- Ensure that the RPM installation permissions work properly with Puppet
  Enterprise

* Thu Oct 26 2017 Jeanne Greulich <jeanne.greulich@onyxpoint.com> - 6.2.5-0
- selinux policy in module simp-environment was changing settings on rsync files not in the
  simp environment and removing their selinux context.  This caused DNS, DHCP to fail
  if they were running in an enviroment by a name other then simp.
- moved selinux policy to simp-environment module and had simp rsync require this module
  so the selinux policy for /var/simp directory would be in one spot.
  file contexts are not overwritten by it.
- updated the policy so it would explicitly set the context for files in simp environment and
  not overwrite settings that were not explicitly set.

* Fri Sep 22 2017 Liz Nemsick <lnemsick.simp@gmail.com> - 6.2.4-0
- Fix changelog/version mismatch which resulted in the release of
  a 6.2.1 tag for which the RPM version was erroneously 6.2.3.

* Fri Sep 22 2017 Liz Nemsick <lnemsick.simp@gmail.com> - 6.2.3-0
- Version erroneously tagged as 6.2.1.

* Fri Sep 22 2017 Liz Nemsick <lnemsick.simp@gmail.com> - 6.2.2-0
- Untagged version.

* Thu Aug 31 2017 Nick Miller <nick.miller@onyxpoint.com> - 6.2.1
- Fleshed out the hostgroup documentation with a practical example

* Wed May 10 2017 Nick Markowski <nmarkowski@keywcorp.com> - 6.2.1
- Added a 'remote_access' scenario

* Thu Apr 20 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.2.1
- Updated the compliance maps based on recent code changes.

* Mon Apr 03 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.2.0
- Move FakeCA down into /var/simp/environment/simp where it can be
  appropriately applied without getting wiped out by r10k or Code Manager
- Make FakeCA use relative paths for writing keys
- Ensure that a copy of the FakeCA core exists in /usr/share/simp so that users
  have a clean copy to work from

* Mon Apr 03 2017 Liz Nemsick <lnemsick.simp@gmail.com> - 6.1.0
- Remove YUM-related parameters in puppet.your.domain.yaml,
  as these parameters are managed by 'simp config'.


* Fri Mar 31 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.1.0
- Remove the unnecessary class includes from the EL6-specific hieradata
- The appropriate class includes have been moved into the 'simp' and
  'simp-lite' scenarios in the simp module

* Wed Mar 29 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.3
- Reintroduce the 'classes' and 'class_exclusions' Global Hiera Arrays

* Thu Mar 16 2017 Liz Nemsick <lnemsick.simp@gmail.com> - 6.0.2
- Only warn about missing /var/www/yum/SIMP directory when this RPM is
  installed via the SIMP ISO.

* Wed Mar 01 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.1
- Moved the class lists from 'scenarios' Hiera data to pupmod-simp-simp
- Updated site.pp to use include the base classes in the correct order

* Thu Feb 16 2017 Liz Nemsick <lnemsick.simp@gmail.com> - 6.0.0
- Fix path to facter in post install

* Tue Jan 10 2017 Nick Miller <nick.miller@onyxpoint.com> - 6.0.0
- Moved the default location of keydist from the normal puppet environment and
  modulepath to /var/simp/environments/simp/site_files/pki_files/files/keydist,
  which won't be overwritten or deleted when using r10k and a control repo
- Added the SIMP scenarios feature, so a user can specify a class list and
  simp_options defaults they would like to use in their implementation
- Stengthen default Puppet server hiera file to include most of the simp
  scenario and default simp_options values

* Fri Jan 06 2017 Trevor Vaughan <tvaughan@onyxpoint.com> - 6.0.0-Alpha
- Eliminated the 'localusers' capability
- Changed the name to simp-environment
- Ripped out all of the legacy materials
- Updated to use the simp-adapter RPM helper

* Tue Dec 06 2016 Nick Markowski <nmarkowski@keywcorp.com> - 6.0.0-Alpha
- Updated nist compliance map to reference new gnome::enable_screensaver
  parameter.
- Updated compliance maps to API 1.0.0 format
- Updated hieradata to reflect changes in puppetdb (SIMP-1450)

* Thu Sep 01 2016 Ralph Wright <ralph.wright@onyxpoint.com> - 5.3.2-0
- Modified compliance files to handle updated audit rules.

* Mon Aug 15 2016 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.3.1-0
- Relocated the 'site_files' directory and created a custom selinux policy for
  the included files.

* Fri Aug 12 2016 Nick Miller <nick.miller@onyxpoint.com> - 5.3.1-0
- Added keytab storage to site_files
- Corrected site_files implementation to work with our krb5 implementation

* Wed Aug 10 2016 Lisa Umberger <lisa.umberger@onyxpoint.com> - 5.3.1-0
- Added a compliance profile for DISA STIG.

* Thu Jul 07 2016 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.3.0-0
- Moved to semantic versioning
- Added support for a 'site_files' module path in the primary 'simp'
  environment for modules like krb5 and pki that have files in them that should
  not be managed by r10k or code manager.

* Mon Apr 25 2016 Chris Tessmer <chris.tessmer@onyxpoint.com> - 5.2.1-5
- Required 'sudo' to resolve ordering race that overwrote '/etc/sudoers'.

* Fri Jan 29 2016 Ralph Wright <ralph.wright@onyxpoint.com> - 5.2.1-4
- Added suppport for compliance module

* Fri Dec 04 2015 Chris Tessmer <chris.tessmer@onyxpoint.com> - 5.2.1-3
- Migrated from 'common::' to 'simplib::'

* Mon Nov 09 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.2.1-2
- Fixed a regression that reverted the 'post' section of the RPM to using
  /srv/www instead of /var/www.

* Tue Jun 09 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.2.1-1
- Made some minor fixes to prepare for public release.
- Added a global Exec default for the command path.
- Refactored the FakeCA to not include any code from the OpenSSL package.

* Thu Apr 09 2015 Chris Tessmer <chris.tessmer@onyxpoint.com> - 5.2.1-0
- Ensured SIMP-ready Puppet environment paths on install as well as upgrade.

* Thu Apr 02 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.2.0-0
- Added PuppetDB support and ensured that the default Puppet server is running
  PuppetDB.

* Fri Feb 27 2015 Nick Markowski <nmarkowski@keywcorp.com> - 5.1.0-0
- Modified the default simp Mcollective hieradata file to include SSL config.

* Fri Feb 06 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.1.0-0
- Create a consistent environment framework for SIMP called 'simp'
- Symlink this new environment to 'production' by default.
- Remove the Passenger SELinux custom policy since we no longer use Passenger
  by default.
- Remove all Passenger and Apache requirements
- Now include the FakeCA in the new 'simp' environment as an example
- Obsolete simp-config
- Add initial build password complexity settings if the system is kickstarting
  and not yet managed by Puppet
- Update the SIMP environment FakeCA to drop keys into the PKI module's
  'keydist' directory.
- Set up a symlink to the PKI module's 'keydist' directory for ease of use.
- Update the default hiera.yaml file to use the hieradata in the environments.

* Mon Dec 15 2014 Kendall Moore <kmoore@keywcorp.com> - 5.0.0-7
- Updated the Passenger SELinux policy to allow httpd to write puppet log files.

* Mon Dec 15 2014 Nick Markowski <nmarkowski@keywcorp.com> - 5.0.0-7
- Updated simp user and group id to 1777 from 777.

* Thu Dec 04 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-6
- Updated to convert log_server (string) to log_servers (array)
  throughout Hiera. This will *not* convert any sub log_server entries
  since there is no way to determine if this is ours or not.

* Fri Oct 31 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-5
- Added support for Hiera SSL keys in the keydist directory.
- Added a default setup for Hiera based on the host SSL keys.

* Thu Oct 30 2014 Chris Tessmer <ctessmer@onyxpoint.com> - 5.0.0-5
- Updated the simp-passenger.te SELinux policy to allow Passenger/Puppet to
  create and rmdir under /var/lib/puppet.

* Mon Aug 25 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-4
- Added a setting to remove the allow virtual package warnings.

* Sat Aug 02 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-3
- Removed common::runlevel class inclusion
- Changed common::runlevel::default to just common::runlevel

* Thu Jul 24 2014 Kendall Moore <kmoore@keywcorp.com> - 5.0.0-2
- Moved references of /srv/www/yum to /var/www/yum.
- Enabled/disabled SIMP yum repos depending on the existence of /var/www/yum/SIMP.

* Mon Jul 21 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-2
- Updated the SELinux policy for passenger to allow httpd_t to do ALL
  THE THINGS.
- Changed web references from /srv to /var
- Upated to use the new /var/simp/rsync path and support splitting the
  rsync paths by fact.

* Mon Jul 14 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-1
- Added stringify_facts = false as the default in puppet.conf to
  support complex facts in Facter 2.

* Fri May 16 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 5.0.0-0
- Updated the sameple puppet.conf.rpmnew file to support directory
  environments since Puppet 3.6 deprecated the 'manifest' option.
- Linked the usual suspects into the 'production' directory
  environment if the targets did not already exist.
- Removed management of /etc/puppet/modules since puppet now supplies
  this.
- Added policycoreutils-devel as a dependency for RHEL 7.

* Tue May 06 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-2
- Added hiera defaults for logstash.
- Moved the old Local repo over to being a SIMP repo.
- Generated a full default Hiera configuration.
- Removed the call to pki::pre in base_config since it no longer exists.
- Removed openldap::slapo::lastbind from ldap_common since it
  constantly generates LDAP updates and subsequently generates audit
  records. Users can add it back in manually if they need it.

* Tue Feb 04 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-1
- Modified the ldap* base classes to use the new openldap module.
- Moved the hiera data from /etc/puppet/hiera to /etc/puppet/hieradata
  to match the documentation on the Internet.
- Ensure that hieradata/simp/%{module_name}/default works.
- The default 'web_server' class has been removed since Hiera can now
  handle all settings properly.
- All references to pupmod::server were replaced by pupmod::master due
  to pupmod-pupmod being rewritten.
- The call to timezone::set_timezone was changed to timezone::set.

* Thu Dec 12 2013 Morgan Haskel <morgan.haskel@onyxpoint.com> - 4.1.0-0
- Added default LDAP referral chaining for slave nodes.
- Fixed the LDAP slave RID to be adjustable.

* Tue Nov 12 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-0
- Migrated default data into Hiera for default_classes.
- Removed all calls to the common::sysctl::* defines and updated the
  includes to point to the new common::sysctl class. Hiera should be
  used for manipulating the individual entities.

* Mon Nov 04 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-0
- Added a default hiera data file for 'sec'
- Modified all calls to 'auditd' to use the new hiera-friendly
  includes.
- Removed the auditd rsync service from the puppet server since we
  haven't served that out for quite a while.

* Sun Oct 06 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 3.0.0-1
- Moved /etc/puppet/manifests/hiera to /etc/puppet/hieradata to match the rest
  of the world.
- Modified the 'fqdn' lookup in hiera.yaml to be 'clientcert'.

* Fri Sep 27 2013 Nick Markowski <nmarkowski@keywcorp.com> 3.0.0-0
- Replaced Extdata with Hiera

* Tue Sep 24 2013 Kendall Moore <kmoore@keywcorp.com> 2.0.3-7
- Upgraded dependencies to puppet 3.X and puppet-server 3.X because of an
  upgrade to use hiera instead of extdata.
- Ensure that the hiera.yaml file is put in /etc/puppet and then linked to
  /etc as well.

* Sat Sep 07 2013 Trevor Vaughan <tvaughan@onyxpoint.com> 2.0.3-6
- Fixed a bug in the 'security_relevant_logs' setting of extdata where the
  escapes were interfering with proper log collection.
- Added all 'sudo' logs to the 'security_relevant_logs' variable.

* Tue Sep 03 2013 Nick Markowski <nmarkowski@keywcorp.com> 2.0.3-6
- Incorporated a lastbind manifest to the default ldap server

* Fri Jun 28 2013 Kendall Moore <kmoore@keywcorp.com> 2.0.3-5
- Updated the simp-passenger.te SELinux policy to allow for the context passenger_t
  access to the context ssh_keygen_exec_t for these file permissions: execute, execute_no_trans, open, read.
- The following avc errors are known to appear in the audit log but have not
  been found to cause any issues.
    - avc:  denied  { relabelto } for  pid=7908 comm="ruby" name="ca_crt.pem"
      dev=dm-6 ino=163921 scontext=unconfined_u:system_r:passenger_t:s0
      tcontext=system_u:object_r:puppet_var_lib_t:s0 tclass=file
    - avc:  denied  { relabelfrom } for pid=7908 comm="ruby" name="ca_crt.pem"
      dev=dm-6 ino=163921 scontext=unconfined_u:system_r:passenger_t:s0
      tcontext=unconfined_u:object_r:puppet_var_lib_t:s0 tclass=file
    - avc:  denied  { relabelfrom } for  pid=7908 comm="ruby" name="master.pid"
      dev=dm-6 ino=114729 scontext=unconfined_u:system_r:passenger_t:s0
      tcontext=unconfined_u:object_r:puppet_var_run_t:s0 tclass=file
    - avc:  denied  { relabelto } for  pid=7908 comm="ruby" name="master.pid"
      dev=dm-6 ino=114729 scontext=unconfined_u:system_r:passenger_t:s0
      tcontext=system_u:object_r:puppet_var_run_t:s0 tclass=file
    - avc:  denied  { getattr } for  pid=8108 comm="ruby"
      path="/var/run/puppet/master.pid" dev=dm-6 ino=114729
      scontext=unconfined_u:system_r:passenger_t:s0
      tcontext=system_u:object_r:puppet_var_run_t:s0 tclass=file

* Fri May 17 2013 Adam Yohrling <adam.yohrling@onyxpoint.com> 2.0.3-4
- Added support for changing the LDAP sync user to connect to legacy
  systems.

* Mon May 13 2013 Trevor Vaughan tvaughan@onyxpoint.com 2.0.3-3
- Added SELinux support for the way Passenger needs to work with the
  system.
- This is *not* a generic Passenger module but one that is designed to
  explicitly work with Puppet as we have designed it into the system.

* Tue May 07 2013 Nick Markowski <nmarkowski@keywcorp.com>
2.0.3-2
- Removed pull_keys.  Openssh now directly authenticates via ldap.

* Thu Dec 06 2012 Maintenance
2.0.3-1
- Updated to fix lack of inclusion of 'pupmod::client' in
  base_config.pp.

* Wed Nov 28 2012 Maintenance
2.0.3-0
- Added a dependency on pupmod-pupmod-2.1.0-0
- Modified calls to pupmod::* functions to use the new parameterized
  classes instead of the previous defines.

* Wed Jul 25 2012 Maintenance - 2.0.2-3
- Edited the post section so the baseurls of the repofiles would
  add the architecture to the path when it did not already exist.
- Now prune the /etc/ssh/ssh_known_hosts file if you have Puppet
  collecting all of your keys.

* Thu Jun 28 2012 Maintenance
2.0.2-2
- Ensure that the simp_def.csv is not overwritten on update.
- Edited the post section so the baseurls of the repofiles would not
  be changed on an upgrade.

* Wed May 30 2012 Maintenance
2.0.2-0
- Added a section to 'site.pp' to create an /etc/simp directory.
- Added a file, /etc/simp/simp.version that's generated from the
  'simp_version()' server function and contains the version of SIMP as
  the server knows it.
- Modified pull_keys in base_config.pp to be a parameterized class
  call.

* Tue Mar 06 2012 Maintenance
2.0.1-0
- Updated puppet_server.pp to include the rsync server statement
  for jenkins
- Updated the name to simp-bootstrap for consistency.

* Wed Feb 15 2012 Maintenance
2.0.0-8
- Commented out the 'mount' statement in base_config. It's just too
  difficult to do any sort of assumption about mount statments in a
  stock build.
- Removed all references to the $newserver fact and the creation of
  the newserver dynamic fact from the puppet server manifest.
- Added $puppet_server and $puppet_server_ip to vars.pp and removed
  $puppet_servers.
- Added a $puppet_server_alt_names variable to allow users to add any
  required name to /etc/hosts for the puppet server.

* Tue Dec 20 2011 Maintenance
2.0.0-7
- Added a variable 'primary_ipaddress' to advanced_vars.pp that uses extlookup
  to pull its value or falls back to $::ipaddress as a default.
- Added extlookup settings to site.pp that will allow you to override variables
  in the following order (from more specific to less specific):
  - /etc/puppet/manifests/extdata/hosts/FQDN.csv
  - /etc/puppet/manifests/extdata/hosts/HOSTNAME.csv
  - /etc/puppet/manifests/extdata/domains/DOMAIN.csv
  - /etc/puppet/manifests/extdata/default.csv
- Added 'simp' to the 'wheel' group so that it can 'su' to root directly with
  the new 'su' PAM settings.

* Fri Nov 18 2011 Maintenance
2.0.0-6
- Ensure that we whack the old puppetd cron job using ralsh.
- Disable sssd by default and enable nscd.

* Sun Nov 06 2011 Maintenance
2.0.0-5
- Removed the 'attrs' line from the ldap_slave class so that it will properly
  copy the password policy entries from the master server. This is extremely
  important since, otherwise, the noExpire password policy will not function
  and you may end up locking out the hostAuth user.

* Sat Oct 08 2011 Maintenance
2.0.0-4
- Add a stanza to ldap_server.pp that adds an unlimited query capability for
  $ldap_bind_dn so that akeys can pull down all user keys.
- Update to wrap the ldap.conf segment in base_config.pp with a section that
  ignores it if using SSSD.

* Fri Aug 12 2011 Maintenance
2.0.0-3
- Added the variable $runpuppet_print_stats = 'true' to kickstart_server.pp to
  enable stats in the runpuppet kickstart file. Simply remove or set to 'false'
  to revert to the old way of doing things.
- Updated default version to RHEL5.7
- Removed the incrond 'watch_local_keys' from default_classes and moved it into
  the openldap module since that was more appropriate.

* Fri Jun 24 2011 Maintenance
2.0.0-2
- Stunnel now listens on all interfaces by default.
- Removed common::resolv::add_entry which has been replaced by
  common::resolv::conf.
- Updated secure_config to ensure that pam::wheel is called with
  the 'administrators' group.

* Wed Apr 27 2011 Maintenance - 2.0.0-1
- Added a class svckill_ignore to default_classes and now include it in
  secure_config by default. This provides a list of services that should
  usually be disabled but which have bad 'status' return codes.
- Added the $use_sssd variable to vars.pp and set it to 'true' by default.
- Set $use_nscd to false by default in vars.pp
- Added logic to base_config.pp to properly set up SSSD vice NSCD.
- Added a global exec to disable SELinux if it is currently enabled. This
  seemed appropriate since we really need it to be off to operate properly.
- Updated the puppet_servers.pp to include randomly generated rsync passwords
  to correspond with the changes for securing rsync. This is important to do
  for any sensitive rsync area. The affected areas are:
    - openldap
    - $domain
    - apache
    - tftpboot
    - dhcpd
- Updated the localusers file with additional details about the new ability to
  prevent user password expiration completely.
- Updated sudoers rule to allow admins to run puppetca
- Added %post code to check and see if Local is correct on the system.
- Updated site to look for Local repos in Local/noarch and
  Local/${architecture} instead of in Local.
- Updated 'Updates' repo to look in 'lsbmajdistrelease' instead of
  'lsbdistrelease' so that RedHat updates do not break the repo path.

* Tue Jan 11 2011 Maintenance - 2.0.0-0
- Refactored for SIMP-2.0.0-alpha release
- Split 'vars.pp' into 'vars.pp' and 'advanced_vars.pp'

* Wed Dec 8 2010 Maintenance 1.0-4
- Moved ntpd::client out of base_config and into the default and puppet nodes
  so that users can now create a separate NTP server. This also means that
  users need to call ntpd::add_servers on a node specific basis.
- Added an incron rule to watch /etc/ssh/local_keys and copy keys to
  /etc/ssh/auth_keys in real time.
- Ensure that SSL access is enabled by default for 'web_server'.
- Get rid of /5 -> 5.2 symlink

* Tue Nov 09 2010 Maintenance 1.0-3
- Modified the post install to be more careful about chowning all of /etc/puppet.

* Thu Sep 09 2010 Maintenance
1.0-2
- Added deprecation notice to tcpwrappers::tcpwrappers_allow

* Wed Jul 14 2010 Maintenance
1.0-1
- Updated the default puppet server to include an rsync space for freeradius with a password.
- Updated default values for 'ldapuri' and 'dns_servers' in vars.pp.

* Thu Jul 01 2010 Maintenance
1.0-0
- Added support for including all hosts public ssh keys in each other's /etc/ssh/ssh_known_hosts files by default.
- puppet/bootstrap/manifests/nodes/default_classes/puppet_servers.pp
  now creates /etc/puppet/facts/newserver.rb based on variables in
  vars.pp so that clustering can work.
- Modified vars.pp to meet the needs of clustering. Variable
  'puppet_server_ip' is now deprecated.  Variables 'puppet_servers',
'search_servers', and 'quiet_server_search' were added.
- Updated default.pp and puppet_servers.pp to call common::sysctl::net::conf
  with default settings
- Updated default_classes/ldap_server.pp to call
  common::sysctl::net::advanced::conf with default settings
- Added elinks to base_config
- Added dependency on rubygem-passenger
- Updated default.pp and puppet_servers.pp to include
  'rsyslog::stock::log_local' to accomodate the new format.
- Added variable "disable_repos"
- Removed 'import "puppet-sysctl"' from class base_config
- Changed 'include "sec::advanced"' to 'include "sec::stock"' in
  /etc/puppet/manifests/nodes/default_classes/secure_config.pp
- Added variable "puppet_servers"

* Mon May 03 2010 Maintenance
0.4-5
- Modified to use new rubygem packages.

* Thu Feb 18 2010 Maintenance
0.4-4
- Added the variable $ldap_use_certs to vars.pp and modified base_config.pp to
  use it. If set to 'false' (the new default) /etc/ldap.conf will *not* be
  populated with cert file locations. If set to 'true', the default if it's not
  there, the certs will be included in the /etc/ldap.conf configuration for
  backward compatibility with existing configurations.

* Thu Feb 04 2010 Maintenance
0.4-3
- Added a short post script to set things up for the new yum layout by default.

* Mon Jan 11 2010 Maintenance
0.4-2
- Files no longer back up to the filebucket by default.  If you wish to back up
  a particular file, you will need to set 'backup => <valid value>'.

* Wed Jan 06 2010 Maintenance
0.4-1
- Included common::sysctl::net in default.pp and puppet_servers.pp
- If users want this functionality, they will need to update their site
  manifests accordingly!
- Also, included common::sysctl::net::advanced in ldap_server.pp since this has
  been shown to dramatically increase performance and the ability to handle a
  large load.

* Tue Dec 15 2009 Maintenance
0.4-0
- Changed the default updates URL for the repo in site.pp to use the
  lsbdistrelease instead of operatingsystemrelease.
  NOTE: This does require a modification to your YUM repo!
  Instead of /srv/www/yum/RedHat/5, it will now be /srv/www/yum/RedHat/5.2 or
  /srv/www/yum/RedHat/5.4, etc...
- Removed default use of PKI certs by LDAP client configuration to support
  GNOME.
- Added the variable ldap_master_uri to vars.pp to support the explicit
  declaration of a LDAP master for referrals. This defaults to the last entry in
  the ldap_uri variable string.

* Fri Dec 4 2009 Maintenance
0.3-9
- Removed the postfix rsync space from the puppet server defaults.
- Updated vars.pp example to show use of $dns_domain

* Tue Nov 24 2009 Maintenance
0.3-8
- Fixed the default IPTables rule in rsyslog.

* Tue Oct 20 2009 Maintenance
0.3-7
- Abstracted the shared LDAP items in default_nodes.  Users should see no
  difference.
- Added a rsync share for the 'snmp' space for the new module.

* Thu Oct 08 2009 Maintenance
0.3-6
- Now include 'vmware::client' by default.  The class was written to only apply
  to vmware systems by default, so this will not affect any other types of host
  but is one less thing to remember to include.
- Changed the verify variable for syslog to 2.
