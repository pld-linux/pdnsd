%define	par	par
Summary:	A caching dns proxy for small networks or dialin accounts
Summary(pl):	DNS proxy serwer dla ma³ej sieci lub jednostki z po³±czeniem dialup
Name:		pdnsd
Version:	1.2.5
Release:	0.par0.0
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.phys.uu.nl/~rombouts/pdnsd/releases/%{name}-%{version}-%{par}.tar.gz
# Source0-md5:	8b1bb9b6b40383a484a90de5d992b4ee
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-threads_signals.patch
Patch1:		%{name}-ac_am.patch
# Old URL:	http://home.t-online.de/home/Moestl/
URL:		http://www.phys.uu.nl/~rombouts/pdnsd.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	caching-nameserver
Provides:	group(pdnsd)
Provides:	user(pdnsd)
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
	--with-default-id=pdnsd \
	--enable-ipv6 \
	--with-thread-lib=LinuxThreads2 \
	--enable-tcp-subseq
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pdnsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pdnsd

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pdnsd.conf{.sample,}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 140 pdnsd
%useradd -u 140 -d /tmp -s /bin/false -c "pdnsd user" -g pdnsd pdnsd

%post
/sbin/chkconfig --add pdnsd
%service pdnsd restart

%preun
if [ "$1" = "0" ]; then
	%service pdnsd stop
	/sbin/chkconfig --del pdnsd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove pdnsd
	%groupremove pdnsd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/txt/*.txt doc/html/*.html
%attr(754,root,root) /etc/rc.d/init.d/pdnsd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pdnsd
%attr(755,root,root) %{_sbindir}/pdnsd
%attr(755,root,root) %{_sbindir}/pdnsd-ctl
%attr(775,pdnsd,pdnsd) %dir %{_var}/cache/pdnsd
%attr(664,pdnsd,pdnsd) %config(noreplace) %verify(not md5 mtime size) %{_var}/cache/pdnsd/pdnsd.cache
%attr(640,root,pdnsd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pdnsd.conf
%{_mandir}/man[58]/*
