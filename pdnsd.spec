Summary: A caching dns proxy for small networks or dialin accounts
Name: pdnsd
Version: 1.0.3
Release: 1
Copyright: GPL
Group: Daemons
Source: pdnsd-1.0.3.tar.bz2
vendor: Thomas Moestl
distribution: RedHat 6.2 Linux
packager: Daniel Smolik <smolik@corpus.cz>
URL: http://home.t-online.de/home/Moestl/
BuildRoot: /tmp/psnd-root
%description
pdnsd is a proxy DNS daemon with permanent (disk-)cache and the ability
to serve local records. It is designed to detect network outages or hangups
and to prevent DNS-dependent applications like Netscape Navigator from hanging.
%prep
%setup
%build
make

%install
install -d -m 755  $RPM_BUILD_ROOT/etc
install -d -m 755  $RPM_BUILD_ROOT/usr/sbin
install  -o root -g root -m600 $RPM_BUILD_DIR/pdnsd-%{version}/doc/pdnsd.conf $RPM_BUILD_ROOT/etc/pdnsd.conf
install  -o root -g root -m755 $RPM_BUILD_DIR/pdnsd-%{version}/pdnsd $RPM_BUILD_ROOT/usr/sbin/pdnsd
install -d -o root -g root -m600   $RPM_BUILD_ROOT/var/cache/pdnsd

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 $RPM_BUILD_DIR/pdnsd-%{version}/rc/Redhat/pdnsd $RPM_BUILD_ROOT/etc/rc.d/init.d/pdnsd

%clean                                                                          
rm -rf $RPM_BUILD_ROOT                                                          
                                                                                
%post                                                                           
/sbin/chkconfig --add pdnsd
                                                                                
%preun                                                                          
if [ $1 = 0 ]; then                                                             
   /sbin/chkconfig --del pdnsd
fi                      



%files
%doc AUTHORS COPYING ChangeLog  INSTALL NEWS README TODO doc/html/index.html doc/html/dl.html doc/html/doc.html doc/html/faq.html
%doc doc/txt/intro.txt doc/txt/manual.txt doc/txt/faq.txt
%config /etc/pdnsd.conf
%dir /var/cache/pdnsd

/usr/sbin/pdnsd
/etc/rc.d/init.d/pdnsd
