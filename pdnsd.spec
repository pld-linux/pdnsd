# TODO: nobody MUST NOT own any files!
Summary:	A caching dns proxy for small networks or dialin accounts
Summary(pl):	DNS proxy serwer dla ma³ej sieci lub jednostki z po³±czeniem dialup
Name:		pdnsd
Version:	1.1.8b1
Release:	0.par8.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.phys.uu.nl/~rombouts/pdnsd/releases/%{name}-%{version}-par8.tar.gz
# Source0-md5:	00847e63641e241f07687387e0c2c1b4
Source1:	%{name}.init
Patch0:		%{name}-threads_signals.patch
Patch1:		%{name}-ac_am.patch
# Old URL:	http://home.t-online.de/home/Moestl/
URL:		http://www.phys.uu.nl/~rombouts/pdnsd.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	nobody-must-not-own-any-files
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	caching-nameserver
Obsoletes:	bind
Obsoletes:	maradns
Obsoletes:	maradns-zoneserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pdnsd is a proxy DNS daemon with permanent (disk-)cache and the
ability to serve local records. It is designed to detect network
outages or hangups and to prevent DNS-dependent applications like
Netscape Navigator from hanging.

%description -l pl
pdnsd jest serwerem proxy dla us³ugi DNS, zapisuj±cym bufor ze
zgromadzonymi informacjami na dysku. Bêdzie on szczególnie u¿yteczny
dla jednostki pracujacej w trybie off-line (np. poprzez po³±czenie
dialup).

%prep
%setup -q
#%patch0 -p0
%patch1 -p1

%build
rm -fr src/rc
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-ipv6 \
	--with-thread-lib=LinuxThreads2
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pdnsd
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pdnsd.conf{.sample,}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pdnsd
if [ -f %{_localstatedir}/lock/subsys/pdnsd ]; then
	/etc/rc.d/init.d/pdnsd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pdnsd start\" to start pdnsd." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_localstatedir}/lock/subsys/pdnsd ]; then
		/etc/rc.d/init.d/pdnsd stop
	fi
	/sbin/chkconfig --del pdnsd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/txt/*.txt doc/html/*.html
%attr(754,root,root) /etc/rc.d/init.d/pdnsd
%attr(755,root,root) %{_sbindir}/pdnsd
%attr(755,root,root) %{_sbindir}/pdnsd-ctl
%attr(775,nobody,nobody) %dir %{_var}/cache/pdnsd
%attr(664,nobody,nobody) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/pdnsd/pdnsd.cache
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pdnsd.conf
%{_mandir}/man8/*
