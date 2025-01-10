%global debug_package %{nil}

# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%global commit_tag %{nil}

# set with the commit date only if commit_tag not nil 
# git version (i.e. master) in format date +Ymd
%if "%{commit_tag}" != "%{nil}"
%global commit_date %(git show -s --date=format:'%Y%m%d' %{commit_tag})
%endif

# repack non-release git branches as .xz with the commit date
# in the following format <name>-<version>-<commit_date>.xz
# the short commit tag should be 7 characters long

Name:		       slock
Version:        1.5
Release:	      %{?commit_date:~0.%{commit_date}.}1
Summary:	      Simple X display locker
Group:		      System
License:	      MIT
URL:		        https://tools.suckless.org/slock/

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Source0:        https://github.com/<org_name>/<project_name>/archive/%{commit_tag}.tar.gz#/%{name}-%{version}.xz
%else
Source0:        https://dl.suckless.org/tools/%{name}-%{version}.tar.gz
%endif

Patch0:       fix-config-64.patch

BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrandr)

Requires:	x11-server

%description
Simple X display locker. This is the simplest X screen locker we are aware of. It is stable and quite a lot of people in our community are using it every day when they are out with friends or fetching some food from the local pub.

%prep
%autosetup

%build
export CFLAGS="%optflags"
%make_build 

%install
%make_install DESTDIR=%{buildroot} PREFIX=%{_prefix}

%files
%license LICENSE
%doc README
%attr(4755, root, root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

