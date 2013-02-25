Summary: Ffmpeg
Name: ffmpeg
Version: 0.5
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Tools
Buildroot: %{_builddir}/%{name}-root

%description

%prep
%setup -q
%build
./configure
make
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root)
/usr/local/bin/*
/usr/local/include/*
/usr/local/lib/*
/usr/local/share/*

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

