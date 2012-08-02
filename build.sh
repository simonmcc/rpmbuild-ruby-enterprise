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
