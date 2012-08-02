# rpmbuild-ruby-enterprise
**Simple rpmdev setup for building redis RPMs**

Original spec file from Adam Vollrath \<adam@endpoint.com\>
* https://packages.endpoint.com/
* http://blog.endpoint.com/2009/06/ruby-enterprise-edition-rpm-packages.html
* https://raw.github.com/gist/108940/13121a024111e4c2a6c1fd66f125174e2fa8a839/ruby-enterprise.spec


Make sure you have check-rpath disabled in your ~/.rpmmacros
(http://fedoraproject.org/wiki/RPath_Packaging_Draft)

RPM dev setup from http://fedoraproject.org/wiki/A_Short_RPM_Tutorial

**One off tool setup**
```shell
$ sudo yum install @development-tools
$ sudo yum install fedora-packager
$ sudo usermod -a -G mock <your username>
```

## Building RPM as non-root outside ~/rpmbuild
Make sure ~/.rpmmacros has %_topdir set to your "starting directory"
```shell
%_topdir                %{expand:%%(pwd)}
```
Then clone & build:

```shell
$ git clone https://github.com/simonmcc/rpmbuild-ruby-enterprise.git
$ cd rpmbuild-ruby-enterprise
$ ./build.sh   
```

build.sh is a simple wrapper that grabs the required source & creates the rest of the skeleton directories required to complete the RPM build:
```shell
$ cat build.sh
#!/bin/bash -x

VERSION=1.8.7
PHUSION_RELEASE=2012.02
SOURCE=ruby-enterprise-${VERSION}-${PHUSION_RELEASE}.tar.gz

mkdir -p BUILD SOURCES SRPMS RPMS/x86_64 RPMS/i386 RPMS/noarch
if [ ! -f $SOURCE ]
then
        (cd SOURCES ; wget http://rubyenterpriseedition.googlecode.com/files/$SOURCE)
fi

rpmbuild -ba SPECS/ruby-enterprise.spec
$
```

