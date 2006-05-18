Summary:	Flash Operator Panel - a switchboard application for the Asterisk PBX
Summary(pl):	Flash Operator Panel - pulpit kontrolny dla centralki Asterisk PBX
Name:		op_panel
Version:	0.26
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://www.asternic.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	54b4f328c11172cbe0be3361c2a3160c
Patch0:		%{name}-path.patch
Patch1:		%{name}-cfg_path.patch
URL:		http://www.asternic.org/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
#Requires:	apache >= 2
#Requires:	asterisk >= 1.2
#Requires:	mysql-client
#Requires:	mysql
Requires:	perl-CPAN
Requires:	perl-IPC-Signal
Requires:	perl-Net-Telnet
Requires:	php-gettext
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-pear-DB
Requires:	php-posix
Requires:	php-program
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flash Operator Panel is a switchboard type application for the
Asterisk PBX. It runs on a web browser with the Flash plugin. It is
able to display information about your PBX activity in real time. The
layout is configurable (button sizes and colors, icons, etc). You can
have more than 100 buttons active per screen. It also supports
contexts: you can have one server running and many different client
displays (for hosted PBX, different departments, etc). It can
integrate with CRM software, by poping up a web page (and passing the
CLID) when a specified button is ringing.

%description -l pl
Flash Operator Panel to aplikacja w stylu pulpitu kontrolnego dla
centralki Asterisk PBX. Dzia�a z poziomu przegl�darki WWW z wtyczk�
Flash. Mo�e wy�wietla� informacje o aktywno�ci centralki w czasie
rzeczywistym. Wygl�d jest konfigurowalny (rozmiary przycisk�w i
kolory, ikony itp.). Mo�na mie� na ekranie ponad 100 aktywnych
przycisk�w. Obs�uguje tak�e konteksty: mo�na mie� jeden dzia�aj�cy
serwer i wiele r�nych ekran�w klienckich (dla hostowanych PBX-�w,
r�nych wydzia��w itp.). Potrafi integrowa� si� z oprogramowaniem CRM
poprzez wywo�ywanie strony WWW (i przekazywanie CLID) po uaktywnieniu
okre�lonego przycisku.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{dhtml,flash}
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/asterisk/%{name}}
install -d $RPM_BUILD_ROOT%{_bindir}

cp -R dhtml/* $RPM_BUILD_ROOT%{_datadir}/%{name}/dhtml
cp -R flash/* $RPM_BUILD_ROOT%{_datadir}/%{name}/flash
install init/op_panel_redhat.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install op_server.pl	$RPM_BUILD_ROOT%{_bindir}
install *.cfg $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGES RECIPES FAQ README UPGRADE TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/asterisk/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/%{name}/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
