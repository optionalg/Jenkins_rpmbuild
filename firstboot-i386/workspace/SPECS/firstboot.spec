Summary: Ceict server firstboot
Name: firstboot
Version: 1.0
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Tools
Buildroot: %{_builddir}/%{name}-root
Requires: chkconfig mysql mysql-server

%description

%prep
%setup -q
%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/boot/grub
mkdir -p $RPM_BUILD_ROOT/var/lib
cp ./splash.xpm.gz $RPM_BUILD_ROOT/boot/grub
cp ./ceict-firstboot $RPM_BUILD_ROOT/etc/init.d
cp ./ceict-my.cnf $RPM_BUILD_ROOT/etc/
cp -r ./license $RPM_BUILD_ROOT/var/lib

%files
%defattr(-,root,root)
/boot/grub/splash.xpm.gz
/etc/init.d/ceict-firstboot
/etc/ceict-my.cnf
/var/lib/*

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%pre
MY=/etc/my.cnf
if [ -f $MY ]; then
	mv $MY ${MY}.bak
fi

%post
mv /etc/ceict-my.cnf /etc/my.cnf
/sbin/chkconfig --add ceict-firstboot

%preun
chkconfig --del ceict-firstboot


