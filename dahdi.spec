Summary: GNU asterisk
Name: dahdi-linux-complete
Version: 2.6.1
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Tools
Buildroot: %{_builddir}/%{name}-root
Requires: chkconfig

%description

%prep
%setup -q
%build
make
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
make DESTDIR=$RPM_BUILD_ROOT config

%files
%defattr(-,root,root)
/etc/
/usr/
/lib/

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%post
/sbin/chkconfig --add dahdi

%preun

if [ "$1" == "0" ]; then
    /sbin/chkconfig --del dahdi
    service dahdi stop
fi

