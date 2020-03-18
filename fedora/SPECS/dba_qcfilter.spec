%{!?srcarchivename: %global srcarchivename %{name}-%{version}-%{release}}

Name:           dba_qcfilter
Version:        0.0.2
Release:        1
Summary:        QC filter for generic BUFR data

License:        GPLv2+
URL:            https://github.com/arpa-simc/dba_qcfilter
Source0:        https://github.com/arpa-simc/%{name}/archive/v%{version}-%{release}.tar.gz#/%{srcarchivename}.tar.gz

BuildArch:      noarch

# Python 3 package names
%if 0%{?rhel} == 7
%define python3_vers python36
%else
%define python3_vers python3
%endif
BuildRequires:  %{python3_vers}
BuildRequires:  %{python3_vers}-devel
BuildRequires:  %{python3_vers}-dballe
Requires:       %{python3_vers}
Requires:       %{python3_vers}-dballe
Conflicts:      libsim < 6.4.3-4

%description
QC filter for generic BUFR data.

%prep
%autosetup -n %{srcarchivename}


%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
# %license 
# %doc add-docs-here
%{_bindir}/dba_qcfilter
%{python3_sitelib}/dba_qcfilter/
%{python3_sitelib}/dba_qcfilter-*.egg-info/


%changelog
* Wed Mar 18 2020 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.0.2-1
- Fixed bin script

* Wed Mar 18 2020 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.0.1-1
- First release
