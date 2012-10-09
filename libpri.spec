Summary: GNU asterisk
Name: libpri 
Version: 1.4.12
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Tools
Buildroot: %{_builddir}/%{name}-root

%description

%prep
%setup -q
%build
make
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root)
/usr/

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

