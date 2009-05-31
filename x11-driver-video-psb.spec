%define name		x11-driver-video-%{chipset}
%define chipset		psb
%define snapshot	0
%define version		0.29.0
%if %snapshot
%define release		%mkrel 0.%{snapshot}.1
%define sname		xf86-video-%{chipset}-%{snapshot}
%define dname		%{distname}
%else
%define release		%mkrel 1
%define sname		xserver-xorg-video-%{chipset}_%{version}
%define dname		xf86-video-%{chipset}
%endif

# act as if we don't use mmListEmpty and other drm functions...
%define _disable_ld_no_undefined 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The X.org driver for Poulsbo chipsets
Group:		System/X11
URL:		http://git.moblin.org/cgit.cgi/deprecated/xf86-video-psb/
# http://moblin.org/repos/projects/xf86-video-psb.git
# DATE=20081006; git archive --format=tar --prefix=xf86-video-psb-$DATE/ origin/GASTON | gzip > xf86-video-psb-$DATE.tar.gz
Source:		%{sname}.tar.gz
License:	MIT
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	x11-proto-devel
BuildRequires:	x11-server-devel
BuildRequires:	libdrm-psb-devel
BuildRequires:	GL-devel

%description
The X.org driver for the video chipset from the Poulsbo SCH.
 
%prep
%setup -q -n %{dname}

%build
# inline drm.pc and xf86driproto.pc flags to use libdrm-psb instead
export DRI_CFLAGS="-I%{_includedir}/libdrm-psb -I%{_includedir}/libdrm-psb/drm -I%{_includedir}/X11/dri"
export DRI_LIBS="-L%{_libdir}/libdrm-psb -ldrm"
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# custom libexa is not needed for xorg > 1.3
rm -f %{buildroot}%{_libdir}/xorg/modules/libexa.*
rm -f %{buildroot}%{_mandir}/man4/exa.*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/xorg/modules/drivers/libmm.so
%{_libdir}/xorg/modules/drivers/libmm.la
%{_libdir}/xorg/modules/drivers/psb_drv.so
%{_libdir}/xorg/modules/drivers/psb_drv.la
%{_mandir}/man4/psb.*
