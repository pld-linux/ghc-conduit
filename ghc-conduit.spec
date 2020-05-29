#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	conduit
Summary:	Streaming data processing library
Summary(pl.UTF-8):	Biblioteka przetwarzania danych strumieniowych
Name:		ghc-%{pkgname}
Version:	1.3.2
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/conduit
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	162fbaa267a0412d98b0536e71bccd6a
URL:		http://hackage.haskell.org/package/conduit
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-directory
BuildRequires:	ghc-exceptions
BuildRequires:	ghc-filepath
BuildRequires:	ghc-mono-traversable >= 1.0.7
BuildRequires:	ghc-mtl
BuildRequires:	ghc-primitive
BuildRequires:	ghc-resourcet >= 1.2
BuildRequires:	ghc-text
BuildRequires:	ghc-transformers >= 0.4
BuildRequires:	ghc-unix
BuildRequires:	ghc-unliftio-core
BuildRequires:	ghc-vector
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-directory-prof
BuildRequires:	ghc-exceptions-prof
BuildRequires:	ghc-filepath-prof
BuildRequires:	ghc-mono-traversable-prof >= 1.0.7
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-primitive-prof
BuildRequires:	ghc-resourcet-prof >= 1.2
BuildRequires:	ghc-text-prof
BuildRequires:	ghc-transformers-prof >= 0.4
BuildRequires:	ghc-unix-prof
BuildRequires:	ghc-unliftio-core-prof
BuildRequires:	ghc-vector-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-bytestring
Requires:	ghc-directory
Requires:	ghc-exceptions
Requires:	ghc-filepath
Requires:	ghc-mono-traversable >= 1.0.7
Requires:	ghc-mtl
Requires:	ghc-primitive
Requires:	ghc-resourcet >= 1.2
Requires:	ghc-text
Requires:	ghc-transformers >= 0.4
Requires:	ghc-unix
Requires:	ghc-unliftio-core
Requires:	ghc-vector
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
conduit is a solution to the streaming data problem, allowing for
production, transformation, and consumption of streams of data in
constant memory. It is an alternative to lazy I/O which guarantees
deterministic resource handling, and fits in the same general solution
space as enumerator/iteratee and pipes.

%description -l pl.UTF-8
conduit to rozwiązanie problemu danych strumieniowych, pozwalające na
produkcję, przekształcanie oraz konsumpcję strumieni danych ze stałą
złożonością pamięciową. Jest to alternatywa dla leniwego we/wy,
gwarantująca deterministyczną obsługę zasobów, mieszcząca się w tej
samej przestrzeni rozwiązań ogólnych, co enumerator/iteratee oraz
potoki.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-bytestring-prof
Requires:	ghc-directory-prof
Requires:	ghc-exceptions-prof
Requires:	ghc-filepath-prof
Requires:	ghc-mono-traversable-prof >= 1.0.7
Requires:	ghc-mtl-prof
Requires:	ghc-primitive-prof
Requires:	ghc-resourcet-prof >= 1.2
Requires:	ghc-text-prof
Requires:	ghc-transformers-prof >= 0.4
Requires:	ghc-unix-prof
Requires:	ghc-unliftio-core-prof
Requires:	ghc-vector-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSconduit-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSconduit-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSconduit-%{version}-*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Combinators
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Combinators/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Combinators/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/List
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/List/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/List/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/*.dyn_hi


%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSconduit-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Combinators/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Conduit/Internal/List/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Streaming/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
