%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xa7475c5f2122fec3f90343223fe3bf5aad1080e4
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library designate-ui
%global module designatedashboard
%global upstream_name designate-dashboard
%global with_doc 1

%global common_desc \
OpenStack Designate Horizon plugin

Name:       openstack-%{library}
Version:    13.0.1
Release:    1%{?dist}
Summary:    OpenStack Designate UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{upstream_name}/

Source0:    https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz
#

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
BuildRequires:  openstack-macros

Requires:   python3-pbr
Requires:   python3-designateclient >= 2.7.0
Requires:   openstack-dashboard >= 1:17.1.0
Requires:   python3-oslo-log >= 3.36.0

%description
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python3-openstackdocstheme
BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-rsvgconverter

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{upstream_name}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=/usr/share/openstack-dashboard
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Move config to horizon
install -p -D -m 644 %{module}/enabled/_1710_project_dns_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1710_project_dns_panel_group.py
install -p -D -m 644 %{module}/enabled/_1721_dns_zones_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1721_dns_zones_panel.py
install -p -D -m 644 %{module}/enabled/_1722_dns_reversedns_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1722_dns_reversedns_panel.py


%files
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_17*

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif


%changelog
* Wed Jan 18 2023 RDO <dev@lists.rdoproject.org> 13.0.1-1
- Update to 13.0.1

* Wed Nov 10 2021 Tobias Urdin <tobias.urdin@binero.com> 13.0.0-2
- Fix Horizon enabled files permissions

* Wed Oct 06 2021 RDO <dev@lists.rdoproject.org> 13.0.0-1
- Update to 13.0.0

* Fri Sep 17 2021 RDO <dev@lists.rdoproject.org> 13.0.0-0.1.0rc1
- Update to 13.0.0.0rc1

