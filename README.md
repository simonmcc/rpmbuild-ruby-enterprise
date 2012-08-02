# rpmbuild-ruby-enterprise
**Simple rpmdev setup for building redis RPMs**

Original spec file from Adam Vollrath <adam@endpoint.com>
https://packages.endpoint.com/
http://blog.endpoint.com/2009/06/ruby-enterprise-edition-rpm-packages.html
https://raw.github.com/gist/108940/13121a024111e4c2a6c1fd66f125174e2fa8a839/ruby-enterprise.spec


Make sure you have check-rpath disabled in your ~/.rpmmacros
(http://fedoraproject.org/wiki/RPath_Packaging_Draft)

RPM dev setup from http://fedoraproject.org/wiki/A_Short_RPM_Tutorial

One off tool setup
```shell
\# yum install @development-tools
\# yum install fedora-packager
\# usermod -a -G mock <your username>
```

Building RPM as non-root outside ~/rpmbuild
```shell
$ rpmbuild -ba SPECS/ruby-enterprise.spec
```

