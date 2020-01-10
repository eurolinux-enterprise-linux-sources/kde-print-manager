
#if 0%{?fedora} > 17
# whether to make this the default printer manager in KDE Plasma Desktop
%global makedefault 1
#endif

Summary: Printer management for KDE
Name:    kde-print-manager
Version: 4.10.5
Release: 2%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdeutils/print-manager
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/print-manager-%{version}.tar.xz
# Plasma init/upgrade script
Source1: 01-print-manager-applet.js

## upstream patches

BuildRequires: gettext
BuildRequires: kdelibs4-devel
BuildRequires: cups-devel >= 1.5.0

Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}
# currently requires local cups for majority of proper function
Requires: cups
# required for the com.redhat.NewPrinterNotification D-Bus service
Requires: system-config-printer-libs

%if 0%{?makedefault}
# Fedora 17 will only get upgraded to 4.9.x, Fedora 18 will not ship these.
Obsoletes: system-config-printer-kde < 7:4.10
Obsoletes: kde-printer-applet < 4.10
%endif

%description
Printer management for KDE.


%prep
%setup -q -n print-manager-%{version}


%build
if [ -x %{_bindir}/plasma-dataengine-depextractor ] ; then
  plasma-dataengine-depextractor plasmoid-package
fi

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%if 0%{?makedefault}
# show print-manager plasmoid by default
install -m644 -p -D %{SOURCE1} %{buildroot}%{_kde4_appsdir}/plasma-desktop/init/01-print-manager-applet.js
mkdir %{buildroot}%{_kde4_appsdir}/plasma-desktop/updates
ln %{buildroot}%{_kde4_appsdir}/plasma-desktop/init/01-print-manager-applet.js %{buildroot}%{_kde4_appsdir}/plasma-desktop/updates/01-print-manager-applet.js
%endif


%files
%{_kde4_libdir}/kde4/kcm_printer_manager.so
%{_kde4_libdir}/kde4/kded_printmanager.so
%{_kde4_libexecdir}/add-printer
%{_kde4_libexecdir}/configure-printer
%{_kde4_libexecdir}/print-queue
%{_kde4_libdir}/kde4/plasma_engine_printers.so
%{_kde4_libdir}/kde4/plasma_engine_printjobs.so
# private unversioned library
%{_kde4_libdir}/libkcupslib.so
%{_kde4_appsdir}/plasma/plasmoids/printmanager/
%{_kde4_appsdir}/plasma/services/org.kde.printers.operations
%{_kde4_appsdir}/plasma/services/org.kde.printjobs.operations
%{_kde4_appsdir}/printmanager/
%{_kde4_datadir}/kde4/services/kcm_printer_manager.desktop
%{_kde4_datadir}/kde4/services/kded/printmanager.desktop
%{_kde4_datadir}/kde4/services/plasma-applet-printmanager.desktop
%{_kde4_datadir}/kde4/services/plasma-engine-printers.desktop
%{_kde4_datadir}/kde4/services/plasma-engine-printjobs.desktop
%{_datadir}/dbus-1/services/org.kde.AddPrinter.service
%{_datadir}/dbus-1/services/org.kde.ConfigurePrinter.service
%{_datadir}/dbus-1/services/org.kde.PrintQueue.service
%if 0%{?makedefault}
%{_kde4_appsdir}/plasma-desktop/*/01-print-manager-applet.js
%endif


%changelog
* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-2
- Branding fix in the applet setting script

* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.1-1.1
- set %%makedefault everywhere (including f17, #711719)

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Fri Dec 21 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.95-1
- 4.9.95

* Fri Dec 14 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90

* Fri Dec 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-8
- Requires: cups

* Fri Dec 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-7
- fix cups renew spam (#885541)

* Fri Nov 09 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.2.0-6
- Requires: system-config-printer-libs (for com.redhat.NewPrinterNotification)

* Fri Nov 09 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.2.0-5
- add missing Epoch for cups-devel dependency

* Fri Nov 09 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.2.0-4
- run the plasma-dataengine-depextractor (if available)

* Fri Nov 09 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.2.0-2
- make this the default printer manager for KDE Plasma Desktop on F18+ (#873746)

* Thu Aug 23 2012 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-1
- 0.2.0
- BR: gettext
- simplified %%description

* Tue Aug 07 2012 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-1
- first try

