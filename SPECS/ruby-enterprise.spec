# Must be built with an ~/.rpmmacros file like this:
# %HOME                   %{expand:%%(cd; pwd)}
# %_topdir                %{HOME}/rpm
# %debug_package          %nil
# %_signature             gpg
# %_gpg_name              hosting@endpoint.com
# %packager               Simon McCartney <simon@mccartney.ie>
# %vendor                 End Point Corporation https://packages.endpoint.com/

# %_exec_prefix           %{_prefix}
# %_bindir                %{_exec_prefix}/bin
# %_sbindir               %{_exec_prefix}/sbin
# %_libexecdir            %{_exec_prefix}/libexec
# %_datadir               %{_prefix}/share
# %_sysconfdir            %{_prefix}/etc
# %_sharedstatedir        %{_prefix}/com
# %_localstatedir         %{_prefix}/var
# %_lib                   lib64
# %_libdir                %{_exec_prefix}/%{_lib}
# %_includedir            %{_prefix}/include
# %_oldincludedir         /usr/include
# %_infodir               %{_prefix}/info
# %_mandir                %{_datadir}/man


# Package Maintainer: Increment phusion_release to match latest release available
%define phusion_release	2012.02

Summary: Ruby Enterprise Edition (Release %{phusion_release})
Name: ruby-enterprise
Vendor: Phusion.nl <info@phusion.nl>
Packager: Simon McCartney (simon@mccartney.ie)
Version: 1.8.7
#Release: el5
Release: recs
License: Ruby or GPL v2
Group: Development/Languages 
URL: http://www.rubyenterpriseedition.com/
Source0: http://rubyenterpriseedition.googlecode.com/files/ruby-enterprise-%{version}-%{phusion_release}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{phusion_release}-root-%(%{__id_u} -n)
BuildRequires: make patch gcc-c++ glibc-devel
BuildRequires: openssl-devel readline-devel
BuildRequires: zlib-devel

#
# we need to set _prefix as well for this to have any affect
# do we need to do %_sysconfdir, %_var, ect...
%define _prefix /opt/ruby-enterprise
Prefix: /opt/ruby-enterprise

%description 
Ruby Enterprise Edition is a server-oriented friendly branch of Ruby which includes various enhancements:
* A copy-on-write friendly garbage collector. Phusion Passenger uses this, in combination with a technique called preforking, to reduce Ruby on Rails applications' memory usage by 33% on average.
* An improved memory allocator called tcmalloc, which improves performance quite a bit.
* The ability to tweak garbage collector settings for maximum server performance, and the ability to inspect the garbage collector's state. (RailsBench GC patch)
* The ability to dump stack traces for all running threads (caller_for_all_threads), making it easier for one to debug multithreaded Ruby web applications.

%prep 
%setup -q -n ruby-enterprise-%{version}-%{phusion_release}

%package rubygems
Summary: The Ruby standard for packaging ruby libraries
Version: 1.8.15
License: Ruby or MIT
Vendor: Jim Weirich, Chad Fowler, and Eric Hodel <rubygems-developers@rubyforge.org>
Group: Development/Libraries
Requires: ruby-enterprise >= 1.8
Provides: ruby-enterprise(rubygems) = %{version}

%description rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.  This rubygems package is for ruby-enterprise in /opt.

%build 
# work around bug in "installer"
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/ruby/gems/1.8/gems

# Security patch for CVE-2011-0188
patch --strip=1 --directory=./source << EOF
--- trunk/ext/bigdecimal/bigdecimal.c
+++ trunk/ext/bigdecimal/bigdecimal.c
@@ -2032,11 +2032,11 @@
 VP_EXPORT void *
 VpMemAlloc(U_LONG mb)
 {
-    void *p = xmalloc((unsigned int)mb);
-    if(!p) {
-        VpException(VP_EXCEPTION_MEMORY,"failed to allocate memory",1);
+    void *p = xmalloc(mb);
+    if (!p) {
+        VpException(VP_EXCEPTION_MEMORY, "failed to allocate memory", 1);
     }
-    memset(p,0,mb);
+    memset(p, 0, mb);
 #ifdef _DEBUG
     gnAlloc++; /* Count allocation call */
 #endif /* _DEBUG */
EOF

# run installer
./installer --auto %{_prefix} --dont-install-useful-gems --no-dev-docs --destdir $RPM_BUILD_ROOT

%install
# no-op

%check
# Help the dynamic linker find the libtcmalloc files:
export LD_LIBRARY_PATH="${RPM_BUILD_ROOT}%{_prefix}/lib/"
# and the Ruby library files:
export RUBYLIB="${RPM_BUILD_ROOT}%{_prefix}/lib/ruby/1.8"
export RUBYLIB="${RUBYLIB}:${RPM_BUILD_ROOT}%{_prefix}/lib/ruby/1.8/%{_arch}-linux"
# Run Ruby's unit tests:
${RPM_BUILD_ROOT}%{_bindir}/ruby ./source/test/runner.rb | tee ./source/RPM_build_unit_tests || :

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_prefix}/lib/*
%{_prefix}/share/man/man1/ruby.1
%doc source/ChangeLog
%doc source/COPYING
%doc source/LEGAL
%doc source/LGPL
%doc source/NEWS
%doc source/README
%doc source/README.EXT
%doc source/ToDo
%doc source/RPM_build_unit_tests

# rubygems
%exclude %{_prefix}/bin/gem
%exclude %{_prefix}/lib/ruby/gems
%exclude %{_prefix}/lib/ruby/site_ruby/1.8/rubygems*
%exclude %{_prefix}/lib/ruby/site_ruby/1.8/ubygems.rb
%exclude %{_prefix}/lib/ruby/site_ruby/1.8/rbconfig

%files rubygems
%{_bindir}/gem
%{_prefix}/lib/ruby/gems
%{_prefix}/lib/ruby/site_ruby/1.8/rubygems*
%{_prefix}/lib/ruby/site_ruby/1.8/ubygems.rb
%{_prefix}/lib/ruby/site_ruby/1.8/rbconfig
%doc rubygems/LICENSE.txt
%doc rubygems/README.rdoc
%doc rubygems/UPGRADING.rdoc
%doc rubygems/MIT.txt
%doc rubygems/Manifest.txt
%doc rubygems/History.txt

%pre
# Do not install if %{_prefix}/bin/ruby exists and is not provided by an RPM
if ([ -e %{_bindir}/ruby ] && !(rpm -q --whatprovides %{_bindir}/ruby >/dev/null)); then
    exit 1
else
    exit 0
fi

%pre rubygems
# Do not install if %{_prefix}/bin/gem exists and is not provided by an RPM
if ([ -e %{_bindir}/gem ] && !(rpm -q --whatprovides %{_bindir}/gem >/dev/null)); then
    exit 1
else
    exit 0
fi

%changelog 
* Thu Aug 02 2012 Simon McCartney <simon@mccartney.ie>
- rpmbuild updates

* Wed Jul 11 2012 Jon Jensen <jon@endpoint.com>
- Updated for release 2012.02.

* Thu Aug 11 2011 Adam Vollrath <hosting@endpoint.com>
- Added upstream security patch for CVE-2011-0188

* Wed Apr 20 2011 Adam Vollrath <hosting@endpoint.com>
- Corrected Licenses

* Tue Apr 19 2011 Adam Vollrath <hosting@endpoint.com>
- Updated for 2011.03 and rubygems 1.5.2

* Tue Aug 24 2010 Adam Vollrath <hosting@endpoint.com>
- Updated package metadata
- Updated BuildRequires dependency lists after testing
- Run Ruby's unit tests during package building

* Wed Jun 30 2010 Adam Vollrath <hosting@endpoint.com>
- Updated for release 2010.02
- Updated rubygems version to 1.3.7
- Generalized all paths

* Mon Apr 19 2010 End Point Corporation <hosting@endpoint.com>
- Updated for release 2010.01
- Updated rubygems to 1.3.6

* Wed Dec 02 2009 Adam Vollrath <adam@endpoint.com>
- Updated for release 2009.10

* Wed Oct 07 2009 Adam Vollrath and Richard Templet <hosting@endpoint.com>
- Updated for release 20090928

* Wed Jun 10 2009 Adam Vollrath <adam@endpoint.com>
- Updated for release 20090610

* Tue Jun 02 2009 Adam Vollrath <adam@endpoint.com>
- Added check for existing /usr/local/bin/gem
- Added LICENSE and other important document files

* Mon Jun 01 2009 Adam Vollrath <adam@endpoint.com>
- Refactored to use Phusion's installer instead of building from source
- Changed prefix to just /usr/local
- Added check for existing /usr/local/bin/ruby
- Split rubygems into a subpackage

* Sat May 30 2009 Adam Vollrath <adam@endpoint.com>
- Changed Release number convention
- Added tcmalloc support and `make test`

* Tue May 26 2009 Adam Vollrath <adam@endpoint.com>
- Updated for 1.8.6-20090520
- Several small improvements to spec file

* Fri Dec 13 2008 Tim C. Harper <tim.harper@leadmediapartners.com>
- first build of REE package
