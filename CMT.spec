Summary: Ceict server process
Name: CMT
Version: 1.2.1.20120928
Release: 1
Source0: %{name}-%{version}-%{release}.tar.gz
License: Ceict
Group: Development/Tools
Buildroot: %{_builddir}/%{name}-%{version}-%{release}-root
Requires: chkconfig initscripts dahdi-linux-complete libpri

%description
Ceict Server process

%prep
%setup -n %{name}-%{version}-%{release}
%build
./configure
make
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT samples
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/
make DESTDIR=$RPM_BUILD_ROOT config

%files
%defattr(-,root,root)
/etc/
/usr/
/var/

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}-%{release}

%pre
if [ -f /etc/rc.d/init.d/ceictims ]; then
    /sbin/service ceictims stop > /dev/null 2>&1
fi

%post
for filename in `ls /etc/ceictims/ceict_*`; do
	if [ -f ${filename/ceict_/} ]; then
		rm -f $filename
	else
		mv $filename ${filename/ceict_/}
	fi
done
chkconfig --list ceictims > /dev/null 2>&1
if [ $? -ne 0 ]; then
    /sbin/chkconfig --add ceictims
fi
/sbin/service ceictims start > /dev/null 2>&1

%preun
if [ "$1" == "0" ]; then
    /sbin/chkconfig --del ceictims
    service ceictims stop > /dev/null 2>&1
fi
