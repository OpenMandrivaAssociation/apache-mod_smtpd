#Module-Specific definitions
%define mod_name mod_smtpd
%define mod_conf A38_%{mod_name}.conf
%define mod_so %{mod_name}.so

%define snap r235759

Summary:	A SMTP protocol enabled module for apache 2.x based on qpsmtpd
Name:		apache-%{mod_name}
Version:	0.9
Release:	%mkrel 1.%{snap}.6
Group:		System/Servers
License:	Apache License
URL:		http://www.mail-archive.com/dev@httpd.apache.org/msg27099.html
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%{_sbindir}/apxs -c mod_smtpd.c smtp_protocol.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CREDITS NOTICE STATUS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h


