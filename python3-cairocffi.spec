#
# This is template for pure python 3 modules
# use template-specs/python.spec for pure python2/python3 packages
# use template-specs/python3-ext.spec for binary python3 packages
#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests

%define		module	cairocffi
Summary:	-
Name:		python3-%{module}
Version:	1.2.0
Release:	0.1
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/Kozea/cairocffi/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	37f8131cfab841dbec3a17f317d9f28b
URL:		https://github.com/Kozea/cairocffi
BuildRequires:	python3-modules >= 1:3.2
#BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-numpy
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:        sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

# fix #!/usr/bin/env python -> #!/usr/bin/python:
#%{__sed} -i -e '1s,^#!.*python3,#!%{__python3},' %{name}.py

%build
%py3_build %{?with_tests:test}

%if %{with doc}
sphinx-build-3 docs html
rm -rf html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%if %{with enable_if_there_are_examples_provided_in_package}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS.rst README.rst
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/VERSION
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%dir %{py3_sitescriptdir}/%{module}/_generated
%{py3_sitescriptdir}/%{module}/_generated/*.py
%{py3_sitescriptdir}/%{module}/_generated/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc html/*
%endif
