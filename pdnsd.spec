Summary:	A caching dns proxy for small networks or dialin accounts
Name:		pdnsd
Version:	1.0.10
Release:	1
License:	GPL
Vendor:		Thomas Moestl
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://home.t-online.de/home/Moestl/%{name}-%{version}.tar.bz2
URL:		http://home.t-online.de/home/Moestl/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pdnsd is a proxy DNS daemon with permanent (disk-)cache and the
ability to serve local records. It is designed to detect network
outages or hangups and to prevent DNS-dependent applications like
Netscape Navigator from hanging.

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

gzip -9nf AUTHORS ChangeLog NEWS README TODO

%clean
rm -rf $RPM_BUILD_ROOT
                                                                                
%post
/sbin/chkconfig --add pdnsd

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del pdnsd
fi

%files
%defattr(644,root,root,755)
%doc *.gz doc/html/index.html doc/html/dl.html doc/html/doc.html doc/html/faq.html
%doc doc/txt/intro.txt doc/txt/manual.txt doc/txt/faq.txt
%config %{_sysconfdir}/pdnsd.conf
%dir /var/cache/pdnsd

%attr(755,root,root) %{_sbindir}/pdnsd
%attr(754,root,root) /etc/rc.d/init.d/pdnsd
