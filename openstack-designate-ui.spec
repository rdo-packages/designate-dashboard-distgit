# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library designate-ui
%global module designatedashboard
%global upstream_name designate-dashboard
%global with_doc 1

%global common_desc \
OpenStack Designate Horizon plugin

Name:       openstack-%{library}
Version:    9.0.1
Release:    2%{?dist}
Summary:    OpenStack Designate UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{upstream_name}/

Source0:    https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

#

BuildArch:  noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-babel
Requires:   python%{pyver}-designateclient >= 2.7.0
Requires:   openstack-dashboard >= 1:14.0.0
Requires:   python%{pyver}-oslo-log >= 3.36.0

%description
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-sphinxcontrib-rsvgconverter

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=/usr/share/openstack-dashboard
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Move config to horizon
install -p -D -m 644 %{module}/enabled/_1710_project_dns_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1710_project_dns_panel_group.py
install -p -D -m 644 %{module}/enabled/_1721_dns_zones_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1721_dns_zones_panel.py
install -p -D -m 644 %{module}/enabled/_1722_dns_reversedns_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1722_dns_reversedns_panel.py


%files
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_17*

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif


%changelog
* Wed Nov 10 2021 Tobias Urdin <tobias.urdin@binero.com> 9.0.1-2
- Fix Horizon enabled files permission

* Thu Apr 15 2021 Tobias Urdin <tobias.urdin@binero.com> 9.0.1-1
- Update to 9.0.1

* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 9.0.0-1
- Update to 9.0.0

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 9.0.0-0.1.0rc1
- Update to 9.0.0.0rc1

