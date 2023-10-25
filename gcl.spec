%define _disable_lto 1

# Address randomization breaks gcl's memory management scheme
%undefine _hardened_build

# GCL wants to read uncompressed info files.  Turn off automatic compression.
%global __brp_compress %{_bindir}/true

# FASL file loads fail with an unexpected EOF error without this.  I do not yet
# know why.
%global __brp_strip_lto %{_bindir}/true

# Use of LTO leads to strange segfaults, reason as yet unknown.
%global _lto_cflags %{nil}

# Upstream prerelease number
%global prerel 102

%global rel 1

# define missing macro
%{?!%_emacs_bytecompile:%global _emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile}
%{?!%_emacs_sitelispdir:%global _emacs_sitelispdir %{_datadir}/emacs/site-lisp}
%{?!%_emacs_sitestartdir:%global _emacs_sitestartdir %{_datadir}/emacs/site-lisp/site-start.d}

Summary:        GNU Common Lisp
Name:           gcl
Version:        2.6.14
Release:        1
License:        GPL+ and LGPLv2+
URL:            https://www.gnu.org/software/gcl/
Source0:        https://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:        gcl.el

# Upstream builds point releases for Debian, and uploads the patches directly
# to the Debian Patch Tracker, but does not spin new tarballs.  These are the
# upstream patches from https://sources.debian.org/patches/gcl/.
Patch0:         https://sources.debian.org/data/main/g/gcl/2.6.14-4/debian/patches/Version_2_6_15pre1.patch
Patch1:         https://sources.debian.org/data/main/g/gcl/2.6.14-4/debian/patches/Version_2_6_15pre2.patch
Patch2:         https://sources.debian.org/data/main/g/gcl/2.6.14-4/debian/patches/Version_2_6_15pre3.patch
	

### Fedora patches
	
# This patch was last sent upstream on 29 Dec 2008.  It updates one source file
# from LaTeX 2.09 to LaTeX 2e, thereby eliminating LaTeX warnings about running
# in compatibility mode.
Patch500:       %{name}-2.6.11-latex.patch
# This patch was last sent upstream on 29 Dec 2008.  It adapts to texinfo 5.0.
Patch501:       %{name}-2.6.11-texinfo.patch
# This patch was last sent upstream on 29 Dec 2008.  It fixes a large number of
# compile- and run-time problems with the Emacs interface code.
Patch502:       %{name}-2.6.11-elisp.patch
# This is a Fedora-specific patch.  Do not delete C files produced from D files
# so they can be pulled into the debuginfo package.
Patch503:       %{name}-2.6.11-debuginfo.patch
# This patch was last sent upstream on 13 Oct 2009.  It fixes two bugs in the
# reading of PLT information.
Patch504:       %{name}-2.6.11-plt.patch
# This patch was last sent upstream on 13 Oct 2009.  It fixes several malformed
# function prototypes involving an ellipsis.
Patch505:       %{name}-2.6.11-ellipsis.patch
# Turn address randomization off early.  GCL is linked with libtirpc, which is
# linked with libselinux, which has a static initializer that calls malloc()
# and free() on systems that do not have /sys/fs/selinux or /selinux mounted,
# or have them mounted read-only.
Patch506:       %{name}-2.6.12-libselinux.patch
# This patch was last sent upstream on 29 Dec 2008.  It updates the autoconf
# and libtool files to newer versions.  By itself, this patch accomplishes
# little of interest.  However, some of the later patches change configure.in.
# Without this patch, autoconf appears to run successfully, but generates a
# configure script that contains invalid shell script syntax.
Patch507:       %{name}-2.6.12-infrastructure.patch
# This patch was last sent upstream on 29 Dec 2008.  It rationalizes the
# handling of system extensions.  For example, on glibc-based systems, some
# functionality is available only when _GNU_SOURCE is defined.
Patch508:       %{name}-2.6.12-extension.patch

BuildRequires:  binutils-devel
BuildRequires:  bzip2
BuildRequires:  gmp-devel
BuildRequires:  pkgconfig(libtirpc)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(tcl)
BuildRequires:  pkgconfig(tk)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  texlive
BuildRequires:	texlive-l3backend
BuildRequires:  texlive-texinfo
BuildRequires:	texlive-ec
BuildRequires:	texlive-unicode-data
BuildRequires:  texinfo
#BuildRequires:  texinfo-tex
BuildRequires:  emacs-nox

Requires:       gcc
Requires:       util-linux
Requires:       which

%description
GCL is a Common Lisp currently compliant with the ANSI standard.  Lisp
compilation produces native code through the intermediary of the
system's C compiler, from which GCL derives efficient performance and
facile portability. Currently uses TCL/Tk as GUI.

%files
%{_bindir}/gcl
%{_prefix}/lib/gcl*
%{_infodir}/*
%{_mandir}/man*/*
%doc readme readme.xgcl RELEASE* ChangeLog* faq doc
%doc gcl*.jpg gcl.ico gcl.png
%doc html/gcl-si html/gcl-tk
%license COPYING*

#--------------------------------------------------------------------

%package emacs
Summary:        Emacs mode for interacting with GCL
Requires:       %{name} = %{version}-%{release}
Requires:       emacs %{?_emacs_version:>= %{_emacs_version}}
BuildArch:      noarch

%description emacs
Emacs mode for interacting with GCL

%files emacs
%doc elisp/readme
%{_emacs_sitelispdir}/gcl/
%{_emacs_sitestartdir}/*

#--------------------------------------------------------------------

%prep
%autosetup -p1

# Don't insert line numbers into cmpinclude.h; the compiler gets confused
#sed -i 's,\($(CC) -E\) -I,\1 -P -I,' makefile

# The binary MUST be run with address randomization off.  The main() function
# has code to accomplish that, but it does not run early enough.  Ensure that
# randomization is off before GCL even starts.
sed -i 's,echo exec,& %{_bindir}/setarch -R,' makefile
 
# Ensure the frame pointer doesn't get added back
sed -i 's/"-fomit-frame-pointer"/""/' configure
 
# Fix a path in the launch script
sed -i 's|/usr/lib/tk|%{_datadir}/tk|' debian/gcl.sh
 
# Silence warnings about the obsolescence of egrep and fgrep
sed -i 's/egrep/grep -E/' o/egrep-def
sed -i 's/fgrep/grep -F/' configure.in configure mp/makefile o/unexec.c \
    o/unexec-19.29.c xbin/notify
 
# Get a version of texinfo.tex that works with the installed version of texinfo
#cp -p %{_texmf_main}/tex/texinfo/texinfo.tex info
cp -p %{_datadir}/texmf-dist/tex/texinfo/texinfo.tex info
 
# The archive is so full of spurious executable bits that we just remove them
# all here, then add back the ones that should exist
find . -type f -perm /0111 | xargs chmod a-x
chmod a+x add-defs add-defs1 config.guess config.sub configure install.sh
chmod a+x bin/info bin/info1 gcl-tk/gcltksrv.in gcl-tk/ngcltksrv mp/gcclab
chmod a+x o/egrep-def utils/replace xbin/*

%build
export CC=gcc
export CXX=g++

# SGC requires the frame pointer
export CFLAGS="%{optflags} -fno-omit-frame-pointer -fwrapv -fuse-ld=bfd" # -fuse-ld=bfd"
%configure \
	--enable-readline \
	--enable-ansi \
	--enable-dynsysgmp \
	--enable-xgcl \
  --enable-tclconfig=%{_libdir} \
	--enable-tkconfig=%{_libdir}
%make -j1

# Build gcl.info, which is needed for DESCRIBE to work properly
rm info/gcl.info
make -C info gcl.info

# dwdoc needs two extra LaTeX runs to resolve references
cd xgcl-2
pdflatex dwdoc.tex
pdflatex dwdoc.tex
cd -

%install
%make_install

# Get rid of the parts that we don't want
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/gcl-*/info

# Install the man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -pf man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1

# Install the HTML documentation
mkdir -p html
cp -pfr info/gcl-si info/gcl-tk html

# Install and compile the Emacs code
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitelispdir}/gcl
cp -pfr elisp/* $RPM_BUILD_ROOT%{_emacs_sitelispdir}/gcl
rm -f $RPM_BUILD_ROOT%{_emacs_sitelispdir}/gcl/makefile
rm -f $RPM_BUILD_ROOT%{_emacs_sitelispdir}/gcl/readme
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
sed -e "s|%LISP_DIR%|%{_emacs_sitelispdir}|" %{SOURCE1} > $RPM_BUILD_ROOT%{_emacs_sitestartdir}/gcl.el
pushd $RPM_BUILD_ROOT%{_emacs_sitelispdir}/gcl
%{_emacs_bytecompile} *.el


popd

# Help the debuginfo generator
ln -s ../h/cmpinclude.h cmpnew/cmpinclude.h
ln -s ../h/cmpinclude.h lsp/cmpinclude.h
ln -s ../h/cmpinclude.h xgcl-2/cmpinclude.h

# The image has garbage strings containing RPM_BUILD_ROOT
export QA_SKIP_BUILD_ROOT=1

# Since we disabled brp-compress, manually compress the man page
gzip -9v $RPM_BUILD_ROOT%{_mandir}/man1/gcl.1

