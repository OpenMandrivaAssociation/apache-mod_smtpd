#Module-Specific definitions
%define mod_name mod_smtpd
%define mod_conf A38_%{mod_name}.conf
%define mod_so %{mod_name}.so

%define snap r235759

Summary:	A SMTP protocol enabled module for apache 2.x based on qpsmtpd
Name:		apache-%{mod_name}
Version:	0.9
Release:	1.%{snap}.13
Group:		System/Servers
License:	Apache License
URL:		https://www.mail-archive.com/dev@httpd.apache.org/msg27099.html
# http://svn.apache.org/repos/asf/httpd/mod_smtpd/trunk/
Source0: 	%{mod_name}-%{version}-%{snap}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.55
Requires(pre):	apache >= 2.0.55
Requires:	apache-conf >= 2.0.55
Requires:	apache >= 2.0.55
BuildRequires:	apache-devel >= 2.0.55
BuildRequires:	file
Epoch:		1

%description
A SMTP protocol enabled module for apache 2.x based on qpsmtpd.

%package	devel
Summary:	Development files for %{mod_name}
Group:		Development/C

%description	devel
Development files for %{mod_name}.

%prep

%setup -q -n %{mod_name}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

cp smtp_core.c mod_smtpd.c

%{_bindir}/apxs -c mod_smtpd.c smtp_protocol.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_includedir}

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

install -m0644 mod_smtpd.h %{buildroot}%{_includedir}/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc CREDITS NOTICE STATUS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*

%files devel
%{_includedir}/*.h




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.13mdv2012.0
+ Revision: 772763
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.12
+ Revision: 678417
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.11mdv2011.0
+ Revision: 588063
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.10mdv2010.1
+ Revision: 516179
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.9mdv2010.0
+ Revision: 406650
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.8mdv2009.1
+ Revision: 326256
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.7mdv2009.0
+ Revision: 235102
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.6mdv2009.0
+ Revision: 215637
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.5mdv2008.1
+ Revision: 181900
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 1:0.9-1.r235759.4mdv2008.1
+ Revision: 119823
- rebuild (missing devel package on ia32)

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.3mdv2008.0
+ Revision: 82674
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9-1.r235759.2mdv2007.1
+ Revision: 140755
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.1mdv2007.1
+ Revision: 79511
- Import apache-mod_smtpd

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-1.r235759.1mdv2007.0
- rebuild

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.9-0.r235759.1mdk
- fix versioning

* Wed Aug 24 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.9-0.r235759.2mdk
- forgot the header file

* Tue Aug 23 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.9-0.r235759.1mdk
- initial Mandriva package

