#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests

%define		module	cairocffi
Summary:	cffi-based cairo bindings for Python
Name:		python3-%{module}
Version:	1.2.0
Release:	5
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/Kozea/cairocffi/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	37f8131cfab841dbec3a17f317d9f28b
URL:		https://github.com/Kozea/cairocffi
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-numpy
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cairocffi is a CFFI-based drop-in replacement for Pycairo, a set of
Python bindings and object-oriented API for cairo.  Cairo is a 2D
vector graphics library with support for multiple backends including
image buffers, PNG, PostScript, PDF, and SVG file output.

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

%build
%py3_build %{?with_tests:test}

%if %{with doc}
sphinx-build-3 docs html
rm -rf html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

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
