%define		rel	2
%define		gitver	7dc2f25
Summary:	Cross NaCL GNU binary utility development utilities - binutils
Name:		crossnacl-binutils
Version:	2.24
Release:	0.git%{gitver}.%{rel}
License:	GPL v3+
Group:		Development/Tools
Source0:	nacl-binutils-%{version}-git%{gitver}.tar.xz
# Source0-md5:	62c1372814f7873be066fe316fbe1c9c
Source1:	get-source.sh
Patch0:		binutils-perl.patch
URL:		https://chromium.googlesource.com/native_client/nacl-binutils/
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fslint
BuildRequires:	perl-tools-pod
BuildRequires:	python-modules
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-nacl
%define		archprefix	%{_prefix}/%{target}
%define		archbindir	%{archprefix}/bin
%define		archlibdir	%{archprefix}/lib

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line.

This package contains the cross version for NaCL.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla NaCl.

%prep
%setup -q -n nacl-binutils-%{version}-git%{gitver}
%patch0 -p1

%build
# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags} -fno-strict-aliasing" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--enable-targets=%{_host} \
%ifarch %{ix86} sparc sparc64 ppc ppc64 s390 sh %{arm}
	--enable-64-bit-bfd \
%endif
	--disable-shared \
	--disable-nls \
	--disable-werror \
	--enable-plugins

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# fix copies to be hardlinks (maybe should symlink in the future)
findup -m $RPM_BUILD_ROOT

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windmc,*windres}.1

# packaged in base binutils
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README binutils/NEWS
%attr(755,root,root) %{_bindir}/%{target}-addr2line
%attr(755,root,root) %{_bindir}/%{target}-ar
%attr(755,root,root) %{_bindir}/%{target}-as
%attr(755,root,root) %{_bindir}/%{target}-c++filt
%attr(755,root,root) %{_bindir}/%{target}-elfedit
%attr(755,root,root) %{_bindir}/%{target}-gprof
%attr(755,root,root) %{_bindir}/%{target}-ld
%attr(755,root,root) %{_bindir}/%{target}-ld.bfd
%attr(755,root,root) %{_bindir}/%{target}-nm
%attr(755,root,root) %{_bindir}/%{target}-objcopy
%attr(755,root,root) %{_bindir}/%{target}-objdump
%attr(755,root,root) %{_bindir}/%{target}-ranlib
%attr(755,root,root) %{_bindir}/%{target}-readelf
%attr(755,root,root) %{_bindir}/%{target}-size
%attr(755,root,root) %{_bindir}/%{target}-strings
%attr(755,root,root) %{_bindir}/%{target}-strip
%dir %{archprefix}
%dir %{archbindir}
%attr(755,root,root) %{archbindir}/ar
%attr(755,root,root) %{archbindir}/as
%attr(755,root,root) %{archbindir}/ld
%attr(755,root,root) %{archbindir}/ld.bfd
%attr(755,root,root) %{archbindir}/nm
%attr(755,root,root) %{archbindir}/objcopy
%attr(755,root,root) %{archbindir}/objdump
%attr(755,root,root) %{archbindir}/ranlib
%attr(755,root,root) %{archbindir}/strip
%dir %{archlibdir}
%{archlibdir}/ldscripts
%{_mandir}/man1/%{target}-addr2line.1*
%{_mandir}/man1/%{target}-ar.1*
%{_mandir}/man1/%{target}-as.1*
%{_mandir}/man1/%{target}-c++filt.1*
%{_mandir}/man1/%{target}-elfedit.1*
%{_mandir}/man1/%{target}-gprof.1*
%{_mandir}/man1/%{target}-ld.1*
%{_mandir}/man1/%{target}-nm.1*
%{_mandir}/man1/%{target}-objcopy.1*
%{_mandir}/man1/%{target}-objdump.1*
%{_mandir}/man1/%{target}-ranlib.1*
%{_mandir}/man1/%{target}-readelf.1*
%{_mandir}/man1/%{target}-size.1*
%{_mandir}/man1/%{target}-strings.1*
%{_mandir}/man1/%{target}-strip.1*
