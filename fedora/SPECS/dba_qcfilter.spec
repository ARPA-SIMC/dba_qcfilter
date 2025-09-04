%{!?srcarchivename: %global srcarchivename %{name}-%{version}-%{release}}

Name:           dba_qcfilter
Version:        0.1
Release:        3
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
BuildRequires:  %{python3_vers}-setuptools
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
%{__python3} tests/runtests.py


%files
# %license 
# %doc add-docs-here
%{_bindir}/dba_qcfilter
%{python3_sitelib}/dba_qcfilter/
%{python3_sitelib}/dba_qcfilter-*.egg-info/


%changelog
* Thu Sep  4 2025 Daniele Branchini <dbranchini@arpae.it> - 0.1-3
- Removed deprecated setup.py test from spec file

* Tue Oct  2 2024 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.1-2
- Rebuild package for F40

* Wed Mar 27 2024 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.1-1
- Remove attributes involved in QC and keep the others (#1)

* Tue May 30 2023 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.0.3-1
- Bump version to reflect upstream changes

* Wed Sep 21 2022 Daniele Branchini <dbranchini@arpae.it> - 0.0.2-2
- bogus release - rebuild on F36/python 3.10

* Wed Mar 18 2020 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.0.2-1
- Fixed bin script

* Wed Mar 18 2020 Emanuele Di Giacomo <edigiacomo@arpae.it> - 0.0.1-1
- First release
