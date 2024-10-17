%global install_loc     %{_datadir}/eclipse/dropins/

%define pkgname           veditor

Name:           eclipse-%{pkgname}
Version:        0.6.3
Release:        7
Summary:        Eclipse-based Verilog/VHDL plugin

Group:          Development/Java
License:        EPL
URL:            https://veditor.sourceforge.net/

Source0:        http://downloads.sourceforge.net/sourceforge/%{pkgname}/%{pkgname}_0_6_3.tar.bz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  eclipse-platform
BuildRequires:  javacc
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  ant

Requires:       eclipse-platform
Requires:       freehdl
Requires:       iverilog

BuildArch:      noarch

%description
Eclipse Verilog editor is a plugin for the Eclipse IDE.
It provides Verilog(IEEE-1364) and VHDL language specific code
viewer, contents outline, code assist etc. It helps coding and
debugging in hardware development based on Verilog or VHDL.


%prep
%setup -q -c
find -name '*.jar' -exec rm -f '{}' \;

#Fixing Versions
sed -i "s|0.6.1|0.6.3|" %{pkgname}/buildjavacc.xml

#fixing rpmlint warnings
#  spurious-executable-perm and end-of-type encodings
for f in CONTRIBUTORS.txt ChangeLog.txt about.html ;
do
    sed 's|\r||' %{pkgname}/$f > $f ;
    chmod -x $f;
done

%build
export JAVACC_HOME=%{_datadir}/java
export ECLIPSE_HOME=%{_libdir}/eclipse

ant -verbose -f %{pkgname}/buildjavacc.xml export


%install
%{__rm} -rf %{buildroot}


%{__install} -d -m 755 %{buildroot}%{install_loc}
%{__install} -pm 0644 \
    %{pkgname}/net.sourceforge.%{pkgname}_%{version}.jar \
    %{buildroot}%{install_loc}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS.txt ChangeLog.txt about.html
%{install_loc}/*


