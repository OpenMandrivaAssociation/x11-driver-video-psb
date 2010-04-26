%define name		x11-driver-video-%{chipset}
%define chipset		psb
%define snapshot	0
%define version		0.31.0
%if %snapshot
%define release		%mkrel 0.%{snapshot}.1
%define sname		xf86-video-%{chipset}-%{snapshot}
%define dname		%{distname}
%else
%define release		%mkrel 6
%define sname		xserver-xorg-video-%{chipset}_%{version}
%define dname		xserver-xorg-video-%{chipset}-%{version}
%endif

# act as if we don't use mmListEmpty and other drm functions...
%define _disable_ld_no_undefined 1

# we want libmm.so
%define _disable_ld_as_needed 1

%define _enable_libtoolize 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The X.org driver for Poulsbo chipsets
Group:		System/X11
URL:		http://git.moblin.org/cgit.cgi/deprecated/xf86-video-psb/
# http://moblin.org/repos/projects/xf86-video-psb.git
# DATE=20081006; git archive --format=tar --prefix=xf86-video-psb-$DATE/ origin/GASTON | gzip > xf86-video-psb-$DATE.tar.gz
Source:		%{sname}.tar.gz
Patch0:		xorg-x11-drv-psb-0.31.0-ignoreacpi.patch
Patch1:		xserver-xorg-video-psb-0.31.0-greedy.patch
Patch2:		xorg-x11-drv-psb-0.31.0-xserver17.patch
Patch3:		xserver-xorg-video-psb-0.31.0-loader.patch
Patch4:		xserver-xorg-video-psb-0.31.0-comment_unused.patch
Patch5:		xserver-xorg-video-psb-0.31.0-assert.patch
License:	MIT
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	x11-proto-devel
BuildRequires:	x11-server-devel
BuildRequires:	libdrm-psb-devel
BuildRequires:	GL-devel
Requires:	libdrm-%{chipset}
Requires:	kmod(%{chipset})
Suggests:	x11-driver-video-psb-binary-blobs

%description
The X.org driver for the video chipset from the Poulsbo SCH.
 
%prep
%setup -q -n %{dname}
%patch0 -p1 -b .ignoreACPI
%patch1 -p1 -b .greedy
%patch2 -p1 -b .xserver17
%patch3 -p1 -b .loader
%patch4 -p1 -b .comment_unused
%patch5 -p1 -b .assert

%build
# inline drm.pc and xf86driproto.pc flags to use libdrm-psb instead
export DRI_CFLAGS="-I%{_includedir}/libdrm-psb -I%{_includedir}/libdrm-psb/drm -I%{_includedir}/X11/dri"
export DRI_LIBS="-L%{_libdir}/libdrm-psb -ldrm"
# regenerate not to build EXA fork (not necessary for Xorg server >= 1.4.99)
autoreconf -v --install
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std DRIVER_MAN_DIR=%{_mandir}/man4

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/xorg/modules/drivers/libmm.so
%{_libdir}/xorg/modules/drivers/libmm.la
%{_libdir}/xorg/modules/drivers/psb_drv.so
%{_libdir}/xorg/modules/drivers/psb_drv.la
%{_mandir}/man4/psb.*
