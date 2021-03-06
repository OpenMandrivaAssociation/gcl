%define _disable_ld_as_needed		1
%define _disable_ld_no_undefined	1
%define	with_selinux			0
%define static_libbfd			1
%define with_xemacs			0

# If the emacs-el package has installed a pkgconfig file, use that to determine
# install locations and Emacs version at build time, otherwise set defaults.
%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 22.2
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%else
%define emacs_version %(pkg-config emacs --modversion)
%define emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%endif

# Prerelease of 2.6.8
%global alphatag 20130521cvs

Name:		gcl
Version:	2.6.8
Release:	0.1.%{alphatag}
Summary:	GNU Common Lisp

Group:		Development/Other
License:	GPL+ and LGPLv2+
URL:		http://www.gnu.org/software/gcl/
# The source for this package was pulled from upstream's CVS repository.  Use
# the following commands to generate the tarball:
#   cvs -d:pserver:anonymous@cvs.savannah.gnu.org:/sources/gcl export \
#     -r Version_2_6_8pre -D 2013-05-22 -d gcl-2.6.8 gcl
#   tar cvJf gcl-2.6.8.tar.xz gcl-2.6.8
Source0:        %{name}-%{version}.tar.xz
Source1:        gcl.el
# This is some info files that are needed for the DESCRIBE function to do
# something useful.  These files are present in CVS HEAD (i.e., the upcoming
# 2.7.0 release), but are missing in the 2.6 branch.
Source2:        %{name}-2.6.8-info.tar.xz
# This patch was last sent upstream on 29 Dec 2008.  It fixes a file descriptor
# leak, as well as combining 4 system calls into only 2 on an exec().
Patch0:         %{name}-2.6.8-fd-leak.patch
# This patch was last sent upstream on 29 Dec 2008.  It updates one source file
# from LaTeX 2.09 to LaTeX 2e, thereby eliminating LaTeX warnings about running
# in compatibility mode.
Patch1:         %{name}-2.6.8-latex.patch
# This patch was last sent upstream on 29 Dec 2008.  It adapts to texinfo 5.0.
Patch2:         %{name}-2.6.8-texinfo.patch
# This patch was last sent upstream on 29 Dec 2008.  It fixes a large number of
# compile- and run-time problems with the Emacs interface code.
Patch3:         %{name}-2.6.8-elisp.patch
# This patch was last sent upstream on 17 Jan 2009.  It adds support for
# compiling and running on an SELinux-enabled host.
Patch4:         %{name}-2.6.8-selinux.patch
# This patch was last sent upstream on 29 Dec 2008.  It uses the rename()
# system call when it is available to avoid spawning a subshell and suffering a
# context switch just to rename a file.
Patch5:         %{name}-2.6.8-rename.patch
# This patch was last sent upstream on 29 Dec 2008.  It eliminates a
# compilation problem due to the fact that, at high optimization levels,
# getcwd() is an inline function.
Patch6:         %{name}-2.6.8-getcwd.patch
# This patch was last sent upstream on 29 Dec 2008.  It updates the autoconf
# and libtool files to newer versions.  By itself, this patch accomplishes
# little of interest.  However, some of the later patches change configure.in.
# Without this patch, autoconf appears to run successfully, but generates a
# configure script that contains invalid shell script syntax.
Patch7:         %{name}-2.6.8-infrastructure.patch
# This patch was last sent upstream on 29 Dec 2008.  It simplifies the handling
# of alloca() detection in the configure script.
Patch8:         %{name}-2.6.8-alloca.patch
# This patch was last sent upstream on 29 Dec 2008.  It rationalizes the
# handling of system extensions.  For example, on glibc-based systems, some
# functionality is available only when _GNU_SOURCE is defined.
Patch9:         %{name}-2.6.8-extension.patch
# This patch was last sent upstream on 29 Dec 2008.  It fixes a compilation
# error on newer GCC systems due to an include inside a function.  This affects
# the "unrandomize" sbrk() functionality, hence the name of the patch.
Patch10:        %{name}-2.6.8-unrandomize.patch
# This is a Fedora-specific patch.  Do not delete C files produced from D files
# so they can be pulled into the debuginfo package.
Patch11:        %{name}-2.6.8-debuginfo.patch
# The need for this patch was last communicated to upstream on 21 May 2009.
# Without this patch, compilation fails due to conflicting type definitions
# between glibc and Linux kernel headers.  This patch prevents the kernel
# headers from being used.
Patch12:        %{name}-2.6.8-asm-signal-h.patch
# This patch was last sent upstream on 13 Oct 2009.  It fixes two bugs in the
# reading of PLT information.
Patch13:        %{name}-2.6.8-plt.patch
# This patch was last sent upstream on 13 Oct 2009.  It fixes several malformed
# function prototypes involving an ellipsis.
Patch14:        %{name}-2.6.8-ellipsis.patch
# This patch was last sent upstream on 30 Dec 2010.  It fixes some malformed
# man page constructions.
Patch15:        %{name}-2.6.8-man.patch
# This patch was last sent upstream on 30 Oct 2012.  It provides more
# information when an unknown reloc type is encountered.
Patch16:        %{name}-2.6.8-reloc-type.patch
# This patch is still experimental.  Enable large file support.
Patch17:        %{name}-2.6.8-largefile.patch
Patch18:	%{name}-2.6.8-tcl8.6.patch

BuildRequires:	readline-devel
BuildRequires:	binutils-devel
BuildRequires:	tk-devel
BuildRequires:	tcl-devel
BuildRequires:	gmp-devel
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:	emacs-bin, emacs-el
BuildRequires:	xaw-devel
%if %{with_xemacs}
BuildRequires:	xemacs, xemacs-devel
%endif
%if %{with_selinux}
BuildRequires:	selinux-policy
%endif
BuildRequires:	x11-server-common

%if %{with_selinux}
Requires:	gcl-selinux
%endif

# GCL currently fails to build on PPC64 platforms.  See bugzilla #480519.
ExcludeArch:	ppc64

%description
GCL is a Common Lisp currently compliant with the ANSI standard.  Lisp
compilation produces native code through the intermediary of the
system's C compiler, from which GCL derives efficient performance and
facile portability. Currently uses TCL/Tk as GUI.


%package emacs
Group:		Development/Other
Summary:	Emacs mode for interacting with GCL
Requires:	%{name} = %{version}-%{release}
Requires:	emacs >= %{emacs_version}
# Don't make subpackages noarch as our bs does not deal with this yet
#BuildArch:      noarch

%description emacs
Emacs mode for interacting with GCL

%package emacs-el
Group:		Development/Other
Summary:	Source for Emacs mode for interacting with GCL
Requires:	%{name}-emacs = %{version}-%{release}
#BuildArch:      noarch

%description emacs-el
Source Elisp code for Emacs mode for interacting with GCL

%if %{with_xemacs}
%package xemacs
Group:		Development/Other
Summary:	XEmacs mode for interacting with GCL
Requires:	%{name} = %{version}-%{release}
Requires:	xemacs >= %{xemacs_version}, xemacs-extras
#BuildArch:      noarch

%description xemacs
XEmacs mode for interacting with GCL

%package xemacs-el
Group:		Development/Other
Summary:	Source for XEmacs mode for interacting with GCL
Requires:	%{name}-xemacs = %{version}-%{release}
#BuildArch:      noarch

%description xemacs-el
Source Elisp code for XEmacs mode for interacting with GCL
%endif

%if %{with_selinux}
%package selinux
Group:		Development/Other
Summary:	SELinux policy for GCL images
Requires(post):	policycoreutils
Requires(postun): policycoreutils

%description selinux
SELinux policy for GCL images.  All programs that dump GCL images to be run on
SELinux-enabled hosts should Require this package, and give the image the type
gcl_exec_t.
%endif

%prep
%setup -q
%setup -q -T -D -a 2
%patch0
%patch1
%patch2
%patch3
%if %{with_selinux}
%patch4 -p1
%endif
%patch5
%patch6
%patch7
%patch8
%patch9
%patch10
%patch11
%patch12
%patch13
%patch14
%patch15
%patch16
%patch17
%patch18 -p1

# Don't let the configure script add compiler flags we don't want
sed -e 's/"-fomit-frame-pointer"/""/' \
%ifarch %ix86
    -e 's/-O3/& -fno-omit-frame-pointer/g' \
%endif
    -i configure

# Fix a path in the launch script
sed -i -e 's|/usr/lib/tk|%{_datadir}/tk|' debian/gcl.sh

# Get a version of texinfo.tex that works with the installed version of texinfo
cp -p %{_datadir}/texmf-dist/tex/texinfo/texinfo.tex info

# The archive is so full of spurious executable bits that we just remove them
# all here, then add back the ones that should exist
find . -type f -perm /0111 | xargs chmod a-x
chmod a+x add-defs add-defs1 config.guess config.sub configure install.sh
chmod a+x bin/info bin/info1 gcl-tk/gcltksrv.in gcl-tk/ngcltksrv mp/gcclab
chmod a+x o/egrep-def utils/replace xbin/*

%build
ln -sf %{_bindir}/ld.bfd bin/ld
export PATH=$PWD/bin:$PATH
CFLAGS="-O2 -g -pipe -fuse-ld=bfd"

%ifarch %ix86
CFLAGS="$CFLAGS -fno-omit-frame-pointer"
%endif

export CFLAGS
%configure2_5x --enable-readline --enable-ansi --enable-dynsysgmp --enable-xgcl \
  --enable-statsysbfd --disable-custreloc --disable-pic \
  --enable-tclconfig=%{_libdir} --enable-tkconfig=%{_libdir}
# FIXME: %%{?_smp_mflags} breaks the build
make 

# Build gcl.info, which is needed for DESCRIBE to work properly
make -C info gcl.info

# dwdoc needs one extra LaTeX run to resolve references
cd xgcl-2
pdflatex dwdoc.tex

%if %{with_selinux}
# Build the SELinux policy
cd ../selinux
make -f %{_datadir}/selinux/devel/Makefile
%endif

%install
make install DESTDIR=%{buildroot}

# Get rid of the parts that we don't want
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_datadir}/emacs
rm -rf %{buildroot}%{_prefix}/lib/gcl-*/info

# Install the man page
mkdir -p %{buildroot}%{_mandir}/man1
cp -pf man/man1/* %{buildroot}%{_mandir}/man1

# Install the HTML documentation
mkdir -p html
cp -pfr info/gcl-si info/gcl-tk html

# Install and compile the Emacs code
mkdir -p %{buildroot}%{emacs_lispdir}/gcl
cp -pfr elisp/* %{buildroot}%{emacs_lispdir}/gcl
rm -f %{buildroot}%{emacs_lispdir}/gcl/makefile
rm -f %{buildroot}%{emacs_lispdir}/gcl/readme
mkdir -p %{buildroot}%{emacs_lispdir}/site-start.d
sed -e "s|%LISP_DIR%|%{emacs_lispdir}|" %{SOURCE1} > %{buildroot}%{emacs_lispdir}/site-start.d/gcl.el
pushd %{buildroot}%{emacs_lispdir}/gcl
emacs -batch -no-site-file --eval "(push \"`pwd`\" load-path)" \
  -f batch-byte-compile *.el
popd

%if %{with_xemacs}
# Install and compile the XEmacs code
mkdir -p %{buildroot}%{xemacs_lispdir}/gcl
cp -fr elisp/* %{buildroot}%{xemacs_lispdir}/gcl
rm -f %{buildroot}%{xemacs_lispdir}/gcl/makefile
rm -f %{buildroot}%{xemacs_lispdir}/gcl/readme
mkdir -p %{buildroot}%{xemacs_lispdir}/site-start.d
sed -e "s|%LISP_DIR%|%{xemacs_lispdir}|" %{SOURCE1} > %{buildroot}%{xemacs_lispdir}/site-start.d/gcl.el
pushd %{buildroot}%{xemacs_lispdir}/gcl
xemacs -batch -no-site-file -eval "(push \"`pwd`\" load-path)" \
  -f batch-byte-compile *.el
popd
%endif

%if %{with_selinux}
# Save the policy file away for later installation
mkdir -p %{buildroot}%{_datadir}/selinux/packages/gcl
cp -p selinux/gcl.pp %{buildroot}%{_datadir}/selinux/packages/gcl
%endif

# The image has garbage strings containing RPM_BUILD_ROOT
export QA_SKIP_BUILD_ROOT=1

%if %{with_selinux}
%post selinux
/usr/sbin/semodule -i %{_datadir}/selinux/packages/gcl/gcl.pp || :
/sbin/fixfiles -R gcl restore || :
%endif

%if %{with_selinux}
%postun selinux
if [ $1 = 0 ]; then
    /usr/sbin/semodule -r gcl || :
fi
%endif

%files
%{_bindir}/gcl
%{_prefix}/lib/gcl*
%{_infodir}/*
%{_mandir}/man*/*
%doc COPYING* readme readme.xgcl RELEASE* ChangeLog* faq doc
%doc gcl*.jpg gcl.ico gcl.png
%doc --parent html

%files emacs
%doc elisp/readme
%dir %{emacs_lispdir}/gcl
%{emacs_lispdir}/gcl/*.elc
%{emacs_lispdir}/site-start.d/*

%files emacs-el
%{emacs_lispdir}/gcl/*.el

%if %{with_xemacs}
%files xemacs
%doc elisp/readme
%dir %{xemacs_lispdir}/gcl
%{xemacs_lispdir}/gcl/*.elc
%{xemacs_lispdir}/site-start.d/*

%files xemacs-el
%{xemacs_lispdir}/gcl/*.el
%endif

%if %{with_selinux}
%files selinux
%{_datadir}/selinux/packages/gcl
%endif
