Summary:	A caching dns proxy for small networks or dialin accounts
Summary:	DNS proxy serwer dla ma³ej sieci lub jednostli z po³±czeniem dialup
Name:		pdnsd
Version:	1.1.2
Release:	1
License:	GPL
Vendor:		Thomas Moestl
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://home.t-online.de/home/Moestl/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
BuildRequires:	flex
URL:		http://home.t-online.de/home/Moestl/
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pdnsd is a proxy DNS daemon with permanent (disk-)cache and the
ability to serve local records. It is designed to detect network
outages or hangups and to prevent DNS-dependent applications like
Netscape Navigator from hanging.

%description -l pl
pdnsd jest serwerem proxy do us³ugi DNS zapisujacym bufor ze zgromadzony,mi
informacjami na dysku. Bêdzie on szczególnie u¿yteczny dla jednostki z
pracujacej w trybie off-line (np. poprzez po³±czenie dialup).

%prep
%setup -q

%build
%configure \
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pdnsd

mv $RPM_BUILD_ROOT%{_sysconfdir}/pdnsd.conf.sample \
	$RPM_BUILD_ROOT%{_sysconfdir}/pdnsd.conf

gzip -9nf AUTHORS ChangeLog NEWS README TODO \
	doc/txt/*.txt

%clean
rm -rf $RPM_BUILD_ROOT
                                                                                
%post
/sbin/chkconfig --add pdnsd
if [ -f /var/lock/subsys/pdnsd ]; then
	/etc/rc.d/init.d/pdnsd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pdnsd start\" to start pdnsd." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pdnsd ]; then
		/etc/rc.d/init.d/pdnsd stop
	fi
	/sbin/chkconfig --del pdnsd
	rm -f /var/cache/pdnsd/pdnsd.cache
fi

%files
%defattr(644,root,root,755)
%doc *.gz doc/txt/*.gz doc/html/index.html doc/html/dl.html doc/html/doc.html doc/html/faq.html
%attr(754,root,root) /etc/rc.d/init.d/pdnsd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pdnsd.conf
%attr(755,root,root) %{_sbindir}/pdnsd
%attr(770,nobody,nobody) %dir /var/cache/pdnsd
%attr(660, nobody, nobody) %config /var/cache/pdnsd/pdnsd.cache
