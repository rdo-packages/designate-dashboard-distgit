%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library designate-ui
%global module designatedashboard
%global upstream_name designate-dashboard

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

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git

Requires:   python2-pbr
Requires:   python2-babel
Requires:   python2-designateclient >= 2.7.0
Requires:   openstack-dashboard >= 1:8.0.0
Requires:   python2-oslo-log >= 3.36.0

%description
%{common_desc}

%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-django
BuildRequires: python2-django-nose
BuildRequires: python-django-compressor
BuildRequires: openstack-dashboard
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-designateclient
BuildRequires: python2-mock
BuildRequires: openstack-macros
BuildRequires: python2-oslo-config

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
%py_req_cleanup


%build
%py2_build

# generate html docs
export PYTHONPATH=/usr/share/openstack-dashboard
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install

# Move config to horizon
install -p -D -m 640 %{module}/enabled/_1710_project_dns_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1710_project_dns_panel_group.py
install -p -D -m 640 %{module}/enabled/_1720_project_dns_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1720_project_dns_panel.py
install -p -D -m 640 %{module}/enabled/_1721_dns_zones_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1721_dns_zones_panel.py
install -p -D -m 640 %{module}/enabled/_1722_dns_reversedns_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1722_dns_reversedns_panel.py


%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_17*

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst


%changelog
