# copy-pasted from https://packages.altlinux.org/en/Sisyphus/srpms/openssl10/spec

Name: openssl-unsafe
Version: 1.0.2i
Release: alt1

Summary: OpenSSL - Secure Sockets Layer and cryptography shared libraries and tools, UNSAFE VERSION!
License: BSD-style
Group: System/Base
Url: http://www.openssl.org

Source: openssl-%version.tar
Source1: cc.sh

Patch03: openssl-alt-config.patch
Patch04: openssl-alt-fips_premain_dso.patch
Patch05: openssl-gosta-pkcs12-fix.patch
Patch06: openssl-rh-alt-soversion.patch
Patch07: openssl-rh-enginesdir.patch
Patch08: openssl-rh-no-rpath.patch
Patch09: openssl-rh-test-use-localhost.patch
Patch11: openssl-rh-pod2man-timezone.patch
Patch12: openssl-rh-perlpath.patch
Patch13: openssl-rh-default-paths.patch
Patch14: openssl-rh-issuer-hash.patch
Patch15: openssl-rh-X509_load_cert_file.patch
Patch16: openssl-rh-version-add-engines.patch
Patch18: openssl-rh-ipv6-apps.patch
Patch19: openssl-rh-env-zlib.patch
Patch21: openssl-rh-algo-doc.patch
Patch22: openssl-rh-apps-dgst.patch
Patch23: openssl-rh-xmpp-starttls.patch
Patch24: openssl-rh-chil-fixes.patch
Patch25: openssl-rh-alt-secure-getenv.patch
Patch27: openssl-rh-padlock64.patch
Patch84: openssl-rh-trusted-first-doc.patch
Patch87: openssl-rh-cc-reqs.patch
Patch90: openssl-rh-enc-fail.patch
Patch92: openssl-rh-system-cipherlist.patch

Patch100: unsafeopenssl-alt-hardcode-path.patch

%define shlib_soversion 10
%define openssldir /opt/unsafeopenssl/var/lib/ssl

BuildRequires: /usr/bin/pod2man bc zlib-devel

%package -n unsafelibcrypto%shlib_soversion
Summary: OpenSSL libcrypto shared library, UNSAFE VERSION!
Group: System/Libraries
Provides: unsafelibcrypto = %version-%release
Requires: ca-certificates

%package -n unsafelibssl%shlib_soversion
Summary: OpenSSL libssl shared library, UNSAFE VERSION!
Group: System/Libraries
Provides: unsafelibssl = %version
Requires: unsafelibcrypto%shlib_soversion = %version-%release

%package -n unsafelibssl-devel
Summary: OpenSSL include files and development libraries, UNSAFE VERSION!
Group: Development/C
Provides: unsafeopenssl-devel = %version
Requires: unsafelibssl%shlib_soversion = %version-%release

%package -n unsafelibssl-devel-static
Summary: OpenSSL static libraries, UNSAFE VERSION!
Group: Development/C
Provides: unsafeopenssl-devel-static = %version
Requires: unsafelibssl-devel = %version-%release

%package -n unsafeopenssl
Summary: OpenSSL tools, UNSAFE VERSION!
Group: System/Base
Provides: %openssldir
Requires: unsafelibssl%shlib_soversion = %version-%release

%package -n unsafeopenssl-doc
Summary: OpenSSL documentation and demos, UNSAFE VERSION!
Group: Development/C
Requires: unsafeopenssl = %version-%release
BuildArch: noarch

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

UNSAFE VERSION!

%description -n unsafelibcrypto%shlib_soversion
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL libcrypto shared library.

UNSAFE VERSION!

%description -n unsafelibssl%shlib_soversion
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL libssl shared library.

UNSAFE VERSION!

%description -n unsafelibssl-devel
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL include files and development libraries
required when building OpenSSL-based applications.

UNSAFE VERSION!

%description -n unsafelibssl-devel-static
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains static libraries required when developing
OpenSSL-based statically linked applications.

UNSAFE VERSION!

%description -n unsafeopenssl
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the base OpenSSL cryptography and SSL/TLS tools.

UNSAFE VERSION!

%description -n unsafeopenssl-doc
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL cryptography and SSL/TLS extra
documentation and demos required when developing applications.

UNSAFE VERSION!

%prep
%setup -n openssl-%version
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1

%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch18 -p1
%patch19 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%patch24 -p1

%patch25 -p1
%patch27 -p1
%patch84 -p1
%patch87 -p1
%patch90 -p1
%patch92 -p1

%patch100 -p1

find -type f -name \*.orig -delete

# Correct shared library name.
sed -i 's/@SHLIB_SOVERSION@/%shlib_soversion/g' Configure Makefile.*
sed -i 's/\\\$(SHLIB_MAJOR)\.\\\$(SHLIB_MINOR)/\\$(VERSION)/g' Configure
sed -i 's/\$(SHLIB_MAJOR)\.\$(SHLIB_MINOR)/\$(VERSION)/g' Makefile.org
sed -i 's/\(^#define[[:space:]]\+SHLIB_VERSION_NUMBER[[:space:]]\+\).*/\1"%version"/' crypto/opensslv.h

# Correct compilation options.
%add_optflags -fno-strict-aliasing -Wa,--noexecstack
sed -i 's/-O\([0-9s]\>\)\?\( -fomit-frame-pointer\)\?\( -m.86\)\?/\\\$(RPM_OPT_FLAGS)/' \
	Configure

# Be more verbose.
sed -i 's/^\([[:space:]]\+\)@[[:space:]]*/\1/' Makefile*

%build

%set_gcc_version 5
%set_verify_elf_method skip

ADD_ARGS=%_os-%_arch
%ifarch %ix86
	ADD_ARGS=linux-elf
%ifarch i386
	ADD_ARGS="$ADD_ARGS 386"
%endif
%endif
%ifarch %arm
ADD_ARGS=linux-generic32
%endif
%ifarch x32
ADD_ARGS=linux-x32
%endif

if echo 'extern __uint128_t i;' |
   gcc %optflags -Werror -c -o/dev/null -xc -; then
	ADD_ARGS="enable-ec_nistp_64_gcc_128 $ADD_ARGS"
fi

./Configure shared \
	--prefix=/opt/unsafeopenssl/usr \
	--libdir=%_lib \
	--openssldir=%openssldir \
	--enginesdir=/opt/unsafeopenssl/%_libdir/openssl/engines \
	--system-ciphers-file=/opt/unsafeopenssl/%_sysconfdir/openssl/cipher-list.conf \
	enable-md2 \
	enable-rfc3779 \
	enable-ssl2 \
	zlib \
    enable-ssl2 enable-ssl3 enable-ssl3-method enable-weak-ssl-ciphers \
	$ADD_ARGS

# SMP-incompatible build.
make

# Make soname symlinks.
/sbin/ldconfig -nv .

# Save library timestamps for later check.
touch -r libcrypto.so.%version libcrypto-stamp
touch -r libssl.so.%version libssl-stamp

LD_LIBRARY_PATH=`pwd` make rehash

%install
# The make_install macro doesn't work here.
make install \
	CC=%_sourcedir/cc.sh \
	INSTALL_PREFIX=%buildroot \
	MANDIR=/opt/unsafeopenssl/%_mandir

# Fail if one of shared libraries was rebuit.
if [ libcrypto.so.%version -nt libcrypto-stamp -o \
     libssl.so.%version -nt libssl-stamp ]; then
	echo 'Shared library was rebuilt by "make install".'
	exit 1
fi

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd %buildroot/opt/unsafeopenssl%_bindir/openssl |tee openssl.libs
grep -qw libssl openssl.libs
grep -qw libcrypto openssl.libs

# Relocate shared libraries from %_libdir/ to /lib/.
mkdir -p %buildroot{/opt/unsafeopenssl/%_lib,/opt/unsafeopenssl%_libdir/openssl,/opt/unsafeopenssl%_sbindir}
for f in %buildroot/opt/unsafeopenssl%_libdir/*.so; do
	t=$(readlink "$f") || continue
	ln -snf ../../%_lib/"$t" "$f"
done
mv %buildroot/opt/unsafeopenssl%_libdir/*.so.* %buildroot/opt/unsafeopenssl/%_lib/

# Relocate engines.
mv %buildroot/opt/unsafeopenssl%_libdir/engines %buildroot/opt/unsafeopenssl%_libdir/openssl/

# Relocate openssl.cnf from %%openssldir/ to %_sysconfdir/openssl/.
mkdir -p %buildroot/opt/unsafeopenssl%_sysconfdir/openssl
mv %buildroot%openssldir/openssl.cnf %buildroot/opt/unsafeopenssl%_sysconfdir/openssl/
ln -s -r %buildroot/opt/unsafeopenssl%_sysconfdir/openssl/openssl.cnf %buildroot%openssldir/

ln -s -r %buildroot%_datadir/ca-certificates/ca-bundle.crt \
	%buildroot%openssldir/cert.pem

mv %buildroot%openssldir/misc/CA{.sh,}
rm %buildroot%openssldir/misc/CA.pl

%define docdir %_docdir/openssl-%version
mkdir -p %buildroot/opt/unsafeopenssl%docdir
install -pm644 CHANGES* LICENSE NEWS README* engines/ccgost/README.gost \
	%buildroot/opt/unsafeopenssl%docdir/
bzip2 -9 %buildroot/opt/unsafeopenssl%docdir/CHANGES*
cp -a demos doc %buildroot/opt/unsafeopenssl%docdir/
rm -rf %buildroot/opt/unsafeopenssl%docdir/doc/{apps,crypto,ssl}

# Create default cipher-list.conf from SSL_DEFAULT_CIPHER_LIST
sed -n -r 's,^#.*SSL_DEFAULT_CIPHER_LIST[[:space:]]+"([^"]+)",\1,p' \
	ssl/ssl.h > %buildroot/opt/unsafeopenssl%_sysconfdir/openssl/cipher-list.conf

rm -f %buildroot%openssldir/misc/tsget

%files -n unsafelibcrypto%shlib_soversion
/opt/unsafeopenssl/%_lib/libcrypto*
%config(noreplace) /opt/unsafeopenssl%_sysconfdir/openssl/openssl.cnf
%dir /opt/unsafeopenssl%_sysconfdir/openssl/
%dir %openssldir
%openssldir/*.cnf
%openssldir/*.pem
%dir /opt/unsafeopenssl%docdir
/opt/unsafeopenssl%docdir/[A-Z]*

%files -n unsafelibssl%shlib_soversion
%config(noreplace) /opt/unsafeopenssl%_sysconfdir/openssl/cipher-list.conf
%dir /opt/unsafeopenssl%_sysconfdir/openssl/
/opt/unsafeopenssl/%_lib/libssl*

%files -n unsafelibssl-devel
/opt/unsafeopenssl%_libdir/*.so
/opt/unsafeopenssl%_libdir/pkgconfig/*
/opt/unsafeopenssl%_includedir/*

%files -n unsafelibssl-devel-static
/opt/unsafeopenssl%_libdir/*.a

%files -n unsafeopenssl
/opt/unsafeopenssl%_bindir/*
%dir %openssldir
%openssldir/misc
%openssldir/certs
%dir %attr(700,root,root) %openssldir/private
/opt/unsafeopenssl%_mandir/man[157]/*

%changelog
* Mon May 14 2018 Pavel Nakonechnyi <pavel@gremwell.com> 1.0.2i-alt1
- Initial build based on 1.0.2i
