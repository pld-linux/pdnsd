Summary:	A caching dns proxy for small networks or dialin accounts
Summary(pl):	DNS proxy serwer dla ma³ej sieci lub jednostki z po³±czeniem dialup
Name:		pdnsd
Version:	1.1.2a
Release:	3
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Vendor:		Thomas Moestl
Source0:	http://home.t-online.de/home/Moestl/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
URL:		http://home.t-online.de/home/Moestl/
BuildRequires:	flex
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pdnsd is a proxy DNS daemon with permanent (disk-)cache and the
ability to serve local records. It is designed to detect network
outages or hangups and to prevent DNS-dependent applications like
Netscape Navigator from hanging.

%description -l pl
pdnsd jest serwerem proxy do us³ugi DNS zapisujacym bufor ze zgromadzonymi
informacjami na dysku. Bêdzie on szczególnie u¿yteczny dla jednostki
pracujacej w trybie off-line (np. poprzez po³±czenie dialup).

%prep
%setup -q

%build
%configure \
	--enable-ipv6
%{__make}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pdnsd
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/pdnsd.conf.sample \
	$RPM_BUILD_ROOT%{_sysconfdir}/pdnsd.conf

%{__gzip} -9nf AUTHORS ChangeLog NEWS README TODO \
	doc/txt/*.txt

%clean
%{__rm} -rf $RPM_BUILD_ROOT
                                                                                
%post
/sbin/chkconfig --add pdnsd
if [ -f %{_localstatedir}/lock/subsys/pdnsd ]; then
	%{_sysconfdir}/rc.d/init.d/pdnsd restart >&2
else
	echo "Run \"%{_sysconfdir}/rc.d/init.d/pdnsd start\" to start pdnsd." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_localstatedir}/lock/subsys/pdnsd ]; then
		%{_sysconfdir}/rc.d/init.d/pdnsd stop
	fi
	/sbin/chkconfig --del pdnsd
fi

%files
%defattr(644,root,root,755)
%doc {*,doc/txt/*}.gz doc/html/{index,dl,doc,faq}.html
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/pdnsd
%attr(755,root,root) %{_sbindir}/pdnsd
%attr(770,nobody,nobody) %dir %{_localstatedir}/cache/pdnsd
%attr(660,nobody,nobody) %config(noreplace) %verify(not md5 size link mtime) %{_localstatedir}/cache/pdnsd/pdnsd.cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pdnsd.conf
