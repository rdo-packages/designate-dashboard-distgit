%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library designate-ui
%global module designatedashboard
%global upstream_name designate-dashboard
%global with_doc 1

%global common_desc \
OpenStack Designate Horizon plugin

Name:       openstack-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Designate UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{upstream_name}/

Source0:    https://tarballs.openstack.org/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:   python3-pbr
Requires:   python3-babel
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
%autosetup -n %{upstream_name}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=/usr/share/openstack-dashboard
%{__python3} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Move config to horizon
install -p -D -m 640 %{module}/enabled/_1710_project_dns_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1710_project_dns_panel_group.py
install -p -D -m 640 %{module}/enabled/_1721_dns_zones_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1721_dns_zones_panel.py
install -p -D -m 640 %{module}/enabled/_1722_dns_reversedns_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1722_dns_reversedns_panel.py


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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/designate-dashboard/commit/?id=03df77d5dd1c530ba52d6a014fbe76121fdb31c0
