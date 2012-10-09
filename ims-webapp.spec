Summary: ims-rpm
Name: ims-webapp
Version: 1.0.0
Release: 1
Source0: %{name}-%{version}.tar.gz
License: 2010-2012, CEICT
Group: Applications/System
Buildroot: %{_builddir}/%{name}-root
Requires: chkconfig shadow-utils

%description

%prep
%setup -q
%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cp -r ./opt $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/opt/

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%pre
/usr/sbin/groupadd ceict 2>/dev/null
/usr/sbin/useradd -r -g ceict cws 2>/dev/null
%post
chmod +x /opt/ceict-webapp-server/jre/bin/*
chmod +x /opt/ceict-webapp-server/jetty/bin/*
chmod +x /opt/ceict-webapp-server/cws.sh
mv -f /opt/ceict-webapp-server/cws.sh /etc/init.d/cws
chkconfig --add cws

%preun
service cws stop
%postun
chkconfig --del cws
rm -rf /opt/ceict-webapp-server>/dev/null
rm -rf /etc/init.d/cws
userdel -f cws
