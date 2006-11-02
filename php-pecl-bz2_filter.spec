%define		_modname	bz2_filter
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - bz2 filter implementation backport for PHP 5.0
Summary(pl):	%{_modname} - backport implementacji filtra bz2 dla PHP 5.0
Name:		php-pecl-%{_modname}
Version:	1.1.0
Release:	5
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	c27893a03c6dadb70489473938ff0495
URL:		http://pecl.php.net/package/bz2_filter/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bzip2 compress/decompress stream filter implementation. Performs
inline compression/decompression using the bzip2 algorythm on any PHP
I/O stream. The data produced by this filter, while compatable with
the payload portion of a bz2 file, does not include headers or tailers
for full bz2 file compatability. To achieve this format, use the
compress.bzip2:// fopen wrapper built directly into PHP.

In PECL status of this extension is: %{_status}.

%description -l pl
Implementacja filtra kompresji/dekompresji strumienia bzip2. Wykonuje
kompresjê/dekompresjê algorytmem bzip2 na dowolnym strumieniu I/O PHP.
Dane stworzone przez ten filtr, bêd±c kompatybilnymi z czê¶ci± pliku
bzip2 zawieraj±c± payload, nie zawieraj± nag³ówków ani koñcówek dla
pe³nej zgodno¶ci z bz2. Aby uzyskaæ ten format, trzeba u¿yæ wrappera
fopen compress.bzip2:// wbudowanego bezpo¶rednio w PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
