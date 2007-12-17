%define gclver	2.6.7

Summary:	GNU Common Lisp
Name:		gcl
Version:	%{gclver}
Release:	%mkrel 5
License:	LGPL
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Patch0:		gcl-%{version}-conf.patch
URL:		http://savannah.gnu.org/projects/gcl
BuildRequires:	automake1.7
BuildRequires:	binutils-devel
BuildRequires:  tetex-dvipdfm
BuildRequires:	tcl tcl-devel tk tk-devel
BuildRequires:	emacs-X11
BuildRequires:  texinfo

%description
GCL is a Common Lisp currently compliant with the CLtL1 standard. Lisp
compilation produces native code through the intermediary of the system's C
compiler, from which GCL derives efficient performance and facile
portability. Currently uses TCL/Tk as GUI.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .config

%build
WANT_AUTOCONF_2_1=1
aclocal-1.7
autoconf
%configure2_5x --enable-notify=no --enable-ansi
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
(cd info
make gcl-tk.dvi gcl-si.dvi
dvipdfm gcl-tk.dvi
dvipdfm gcl-si.dvi)
%makeinstall DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/gcl-%{gclver}/info
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
install -m 644 man/man1/gcl.1 $RPM_BUILD_ROOT%{_mandir}/man1
find $RPM_BUILD_ROOT%{_datadir} -type f -perm 640 -print0 | xargs -0 chmod 644 || :
find $RPM_BUILD_ROOT%{_datadir} -type f -perm 750 -print0 | xargs -0 chmod 644 || :
find $RPM_BUILD_ROOT%{_prefix}/lib/gcl-%{version} -type f -perm 750 -print0 | xargs -0 chmod 755 || :
find $RPM_BUILD_ROOT%{_prefix}/lib/gcl-%{version} -type f -perm 640 -print0 | xargs -0 chmod 644 || :
chmod 644 readme faq ChangeLog

%post
%_install_info gcl.info
%_install_info gcl-si.info
%_install_info gcl-tk.info

%postun
%_remove_install_info gcl.info
%_remove_install_info gcl-si.info
%_remove_install_info gcl-tk.info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc readme faq ChangeLog info/*.pdf
%dir %{_prefix}/lib/gcl-%{gclver}
%{_bindir}/gcl
%{_prefix}/lib/gcl-%{gclver}/cmpnew
%{_prefix}/lib/gcl-%{gclver}/gcl-tk
%{_prefix}/lib/gcl-%{gclver}/h
%{_prefix}/lib/gcl-%{gclver}/lsp
%{_prefix}/lib/gcl-%{gclver}/unixport
%{_prefix}/lib/gcl-%{gclver}/clcs
%{_prefix}/lib/gcl-%{gclver}/pcl
%{_datadir}/emacs/*
%{_infodir}/gcl*.info*
%{_mandir}/man1/*


