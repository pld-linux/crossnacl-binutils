%define		gitver f412ed5
Summary:	Cross NaCL GNU binary utility development utilities - binutils
Name:		crossnacl-binutils
Version:	2.20.1
Release:	1.git%{gitver}
License:	GPL
Group:		Development/Tools
Source0:	nacl-binutils-%{version}-git%{gitver}.tar.bz2
# Source0-md5:	b49c25e5cb1bbfb5333aa82bcbda12df
Source1:	get-source.sh
URL:		http://sources.redhat.com/binutils/
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fslint
BuildRequires:	python-modules
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-nacl
%define		arch		%{_prefix}/%{target}

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
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for NaCL.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla NaCl.

%prep
%setup -q -n nacl-binutils-%{version}-git%{gitver}

%build
# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags} -fno-strict-aliasing" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target} \
	--enable-targets=%{_host} \
%ifarch ia64
	--enable-targets=i386-linux \
%endif
%ifarch ppc ppc64
	--enable-targets=spu \
%endif
%ifarch %{ix86} sparc sparc64 ppc ppc64 s390 sh arm
	--enable-64-bit-bfd \
%endif
	--disable-shared \
	--disable-nls \
	--disable-werror \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
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
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

# don't want this here
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# packaged in base binutils
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/ldscripts/*
%{_mandir}/man?/%{target}-*
