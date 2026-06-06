#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	cairocffi
Summary:	cffi-based cairo bindings for Python
Summary(pl.UTF-8):	Wiązania cairo dla Pythona oparte na cffi
Name:		python3-%{module}
Version:	1.7.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/Kozea/cairocffi/releases
Source0:	https://github.com/Kozea/cairocffi/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	90ca42f574320c8d95e9e30c1f62426a
URL:		https://github.com/Kozea/cairocffi
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.2
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-cffi >= 1.1.0
BuildRequires:	python3-numpy
BuildRequires:	python3-pikepdf
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cairocffi is a CFFI-based drop-in replacement for Pycairo, a set of
Python bindings and object-oriented API for cairo. Cairo is a 2D
vector graphics library with support for multiple backends including
image buffers, PNG, PostScript, PDF, and SVG file output.

%description -l pl.UTF-8
cairocffi to party na CFFI zamiennik Pycairo - zbioru wiązań Pythona i
zorientowane obiektowo API do cairo. Cairo to biblioteka grafiki
wektorowej 2D z obsługą wielu backendów, w tym buforów obrazów oraz
wyjścia do plików PNG, PostScript, PDF i SVG.

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
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest cairocffi
%endif

%if %{with doc}
PYTHONPATH=$PWD \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
