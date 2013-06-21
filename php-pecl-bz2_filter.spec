%define		php_name	php%{?php_suffix}
%define		modname	bz2_filter
%define		status		stable
Summary:	%{modname} - bz2 filter implementation backport for PHP 5.0
Summary(pl.UTF-8):	%{modname} - backport implementacji filtra bz2 dla PHP 5.0
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.0
Release:	7
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	c27893a03c6dadb70489473938ff0495
URL:		http://pecl.php.net/package/bz2_filter/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bzip2 compress/decompress stream filter implementation. Performs
inline compression/decompression using the bzip2 algorythm on any PHP
I/O stream. The data produced by this filter, while compatable with
the payload portion of a bz2 file, does not include headers or tailers
for full bz2 file compatability. To achieve this format, use the
compress.bzip2:// fopen wrapper built directly into PHP.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Implementacja filtra kompresji/dekompresji strumienia bzip2. Wykonuje
kompresję/dekompresję algorytmem bzip2 na dowolnym strumieniu I/O PHP.
Dane stworzone przez ten filtr, będąc kompatybilnymi z częścią pliku
bzip2 zawierającą payload, nie zawierają nagłówków ani końcówek dla
pełnej zgodności z bz2. Aby uzyskać ten format, trzeba użyć wrappera
fopen compress.bzip2:// wbudowanego bezpośrednio w PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
