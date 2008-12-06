%define gclver	2.6.7

Summary:	GNU Common Lisp
Name:		gcl
Version:	%{gclver}
Release:	%mkrel 10
License:	GPLv2+
Group:		Development/Other
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Patch1:		gcl_2.6.7-44.diff
URL:		http://savannah.gnu.org/projects/gcl
BuildRequires:	binutils-devel
BuildRequires:  tetex-dvipdfm
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	emacs-X11
BuildRequires:  texinfo
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
GCL is a Common Lisp currently compliant with the CLtL1 standard. Lisp
compilation produces native code through the intermediary of the system's C
compiler, from which GCL derives efficient performance and facile
portability. Currently uses TCL/Tk as GUI.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .debian

%build
%configure2_5x --enable-notify=no --enable-ansi --enable-emacsdir=%{_datadir}/emacs/site-lisp \
		--enable-locbfd \
		--disable-dynsysbfd \
		--disable-statsysbfd \
		--enable-dynsysgmp

make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
(cd info
make gcl-tk.dvi gcl-si.dvi
dvipdfm gcl-tk.dvi
dvipdfm gcl-si.dvi)
%makeinstall DESTDIR=%{buildroot} \
	prefix=%{_prefix}
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_prefix}/lib/gcl-%{gclver}/info
rm -rf %{buildroot}%{_datadir}/doc
install -m 644 man/man1/gcl.1 %{buildroot}%{_mandir}/man1
find %{buildroot}%{_datadir} -type f -perm 640 -print0 | xargs -0 chmod 644 || :
find %{buildroot}%{_datadir} -type f -perm 750 -print0 | xargs -0 chmod 644 || :
find %{buildroot}%{_prefix}/lib/gcl-%{version} -type f -perm 750 -print0 | xargs -0 chmod 755 || :
find %{buildroot}%{_prefix}/lib/gcl-%{version} -type f -perm 640 -print0 | xargs -0 chmod 644 || :
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
rm -rf %{buildroot}

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
%{_prefix}/lib/gcl-%{gclver}/xgcl-2
%{_datadir}/emacs/*
%{_infodir}/gcl*.info*
%{_mandir}/man1/*

