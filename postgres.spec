# configurable build options
%{!?enable_icu:%global enable_icu 1}
%{!?enable_kerberos:%global enable_kerberos 1}
%{!?enable_ldap:%global enable_ldap 1}
%{!?enable_pam:%global enable_pam 1}
%{!?ebable_plpython2:%global enable_plpython2 1}
%{!?enable_pltcl:%global enable_pltcl 1}
%{!?enable_plperl:%global enable_plperl 1}
%{!?enable_ssl:%global enable_ssl 1}
%{!?enable_xml:%global enable_xml 1}
%{!?enable_sdt:%global enable_sdt 1}
%{!?enable_selinux:%global enable_selinux 1}
#broken
%{!?enable_plpython3:%global enable_plpython3 0}

%global cmd_update_alt		%{_sbindir}/update-alternatives

%global pkg_main		postgresql%pg_version_major
%global pkg_server		%pkg_main-server
%global pkg_server_devel	%pkg_main-server-devel
%global pkg_plpython2		%pkg_main-plpython2
%global pkg_plpython3		%pkg_main-plpython3
%global pkg_plperl		%pkg_main-plperl
%global pkg_pltcl		%pkg_main-pltcl
%global pkg_docs		%pkg_main-docs
%global pkg_contrib		%pkg_main-contrib
%global pkg_libs		%pkg_main-libs
%global pkg_devel		%pkg_main-devel
%global pkg_libpq5		%pkg_main-libpq5
%global pkg_timetravel		%pkg_main-timetravel
%global pkg_xml			%pkg_main-xml

%global pg_version_major	10
%global pg_version_minor	13
%global pg_version_prev		9

%global pg_alternative_prio	%{pg_version_major}00

%global pg_prefix		/usr/lib/postgresql%pg_version_major
%global pg_bindir		%pg_prefix/bin
%global pg_includedir		%pg_prefix/include
%global pg_mandir		%pg_prefix/share/man
%global pg_datadir		%pg_prefix/share
%global pg_libdir		%pg_prefix/%{_lib}
%global pg_docdir		%pg_datadir/doc
%global pg_extdir		%pg_datadir/extension
%global pg_localedir		%{_datadir}/locale
%global pg_dbdir		/var/lib/postgresql/%pg_version_major
%global pg_dbroot		/var/lib/postgresql
%global pg_rundir		/var/run/postgresql
%global pg_pamdir		%{_sysconfdir}/pam.d

%global pg_prev_prefix		/usr/postgresql%pg_version_prev
%global pg_prev_bindir		%pg_prev_prefix/bin
%global pg_prev_dbdir		/var/lib/postgresql/%pg_version_prev

%global pg_systemd_service	postgresql-%pg_version_major.service
%global pg_sysvinit_service	postgresql-%pg_version_major

%global pg_libs_conf		%pg_datadir/postgresql-%pg_version_major-libs.conf
%global pg_etc_sysconfig	/etc/sysconfig/pgsql/%pg_version_major

%global requires_main		Requires: %pkg_main%{?_isa} = %{version}-%{release}
%global requires_server		Requires: %pkg_server%{?_isa} = %{version}-%{release}
%global requires_libs		Requires: %pkg_libs%{?_isa} = %{version}-%{release}
%global requires_libpq5		Requires: %pkg_libpq5%{?_isa} = %{version}-%{release}
%global requires_server_devel	Requires: %pkg_server_devel%{?_isa} = %{version}-%{release}
%global requires_server		Requires: %pkg_server%{?_isa} = %{version}-%{release}

%global configure_call \\\
	./configure \\\
		--enable-rpath \\\
		--sysconfdir=%{_sysconfdir} \\\
		--prefix=%pg_prefix \\\
		--bindir=%pg_bindir \\\
		--includedir=%pg_includedir \\\
		--localedir=%pg_localedir \\\
		--mandir=%pg_mandir \\\
		--datadir=%pg_datadir \\\
		--libdir=%pg_libdir \\\
		--with-system-tzdata=%{_datadir}/zoneinfo \\\
		--docdir=%pg_docdir \\\
		--without-llvm \\\
		--enable-nls \\\
		%{?enable_icu:--with-icu} \\\
		%{?enable_plperl:--with-perl} \\\
		%{?enable_pltcl:--with-tcl --with-tclconfig=%{_libdir}} \\\
		%{?enable_plpython2:--with-python} \\\
		%{?enable_plpython3:--with-python} \\\
		%{?enable_ssl:--with-openssl} \\\
		%{?enable_pam:--with-pam} \\\
		%{?enable_kerberos:--with-gssapi} \\\
		%{?enable_sdt:--enable-dtrace} \\\
		--with-uuid=e2fs \\\
		%{?enable_xml:--with-libxml --with-libxslt} \\\
		%{?enable_ldap:--with-ldap} \\\
		%{?enable_selinux:--with-selinux}

%global generate_file \\\
	sed -e 's~@PG_VERSION_MAJOR@~%pg_version_major~g' | \\\
	sed -e 's~@PG_VERSION_PREV@~%pg_version_prev~g' | \\\
	sed -e 's~@PG_DOCDIR@~%pg_docdir~g' | \\\
	sed -e 's~@PG_BINDIR@~%pg_bindir~g' | \\\
	sed -e 's~@PG_DBDIR@~%pg_dbdir~g' | \\\
	sed -e 's~@PG_DBROOT@~%pg_dbroot~g' | \\\
	sed -e 's~@PG_PREV_BINDIR@~%pg_prev_bindir~g' | \\\
	sed -e 's~@PG_PREV_DBDIR@~%pg_prev_dbdir~g' | \\\
	sed -e 's~@PG_RUNDIR@~%pg_rundir~g'

%global pkg_main_cmd \\\
	clusterdb \\\
	createdb \\\
	createuser \\\
	dropdb \\\
	dropuser \\\
	pgbench \\\
	pg_archivecleanup \\\
	pg_basebackup \\\
	pg_config \\\
	pg_dump \\\
	pg_dumpall \\\
	pg_isready \\\
	pg_restore \\\
	pg_rewind \\\
	pg_test_fsync \\\
	pg_test_timing \\\
	pg_receivewal \\\
	pg_upgrade \\\
	pg_waldump \\\
	psql \\\
	reindexdb \\\
	vacuumdb

%global pkg_server_cmd initdb pg_controldata pg_ctl pg_resetwal postgres postmaster

Name:		postgres
Version:	%pg_version_major.%pg_version_minor
Release:	mtx.8
License:	PostgreSQL
Url:		https://www.postgresql.org/
Summary:	PostgreSQL client programs and libraries

Source0:	postgres-%{version}.tar.gz

BuildRequires:	perl
BuildRequires:	glibc-devel
BuildRequires:	bison
BuildRequires:	flex >= 2.5.31
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	docbook-xsl-stylesheets docbook5-xsl-stylesheets
BuildRequires:	gettext >= 0.10.35
BuildRequires:	libuuid-devel
BuildRequires:	opensp

%{?enable_icu:BuildRequires:		libicu-devel}
%{?enable_kerberos:BuildRequires:	krb5-devel}
%{?enable_ldap:BuildRequires:		openldap2-devel}
%{?enable_pam:BuildRequires:		pam-devel}
%{?enable_plpython2:BuildRequires:	python2-devel}
%{?enable_plpython3:BuildRequires:	python3-devel}
%{?enable_pltcl:BuildRequires:		tcl-devel}
%{?enable_sdt:BuildRequires:		systemtap-sdt-devel}
%{?enable_selinux:BuildRequires:	libselinux-devel >= 2.0.93 selinux-policy}
%{?enable_ssl:BuildRequires:		openssl-devel}
%{?enable_xml:BuildRequires:		libxml2-devel libxslt-devel}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system. These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection.

### main package

%package -n %pkg_main
Summary:	PostgreSQL client programs and libraries
Requires:	/sbin/ldconfig
%requires_libs

Requires(post):		%cmd_update_alt
Requires(postun):	%cmd_update_alt

Provides:	postgresql >= %{version}-%{release}

%description -n %pkg_main
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system. These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection. The PostgreSQL server can be found in the
%pkg_server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the %pkg_server package.

%files -n %pkg_main -f %pkg_main.list
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES COPYRIGHT

%post -n %pkg_main

# Create alternatives entries for common binaries and man files
for cmd in %pkg_main_cmd ; do
    %cmd_update_alt --install %{_bindir}/${cmd}        pgsql-${cmd}    %pg_bindir/${cmd}        %pg_alternative_prio
    %cmd_update_alt --install %{_mandir}/man1/${cmd}.1 pgsql-${cmd}man %pg_mandir/man1/${cmd}.1 %pg_alternative_prio
done

%postun -n %pkg_main
# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]; then
    for cmd in %pkg_main_cmd ; do
        %cmd_update_alt --remove pgsql-${cmd}    %pg_bindir/psql
        %cmd_update_alt --remove pgsql-${cmd}man %pg_mandir/man1/${cmd}.1
    done
fi

### libraries package

%package -n %pkg_libs
Summary:	The shared libraries required for any PostgreSQL clients
Provides:	postgresql-libs = %pg_version_major
%requires_libpq5

%description -n %pkg_libs
The %pkg_libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%post -n %pkg_libs
%cmd_update_alt --install /etc/ld.so.conf.d/postgresql-pgdg-libs.conf pgsql-ld-conf %pg_libs_conf %pg_alternative_prio
/sbin/ldconfig

%postun -n %pkg_libs
if [ "$1" -eq 0 ]; then
    %cmd_update_alt --remove pgsql-ld-conf %pg_libs_conf
    /sbin/ldconfig
fi

%files -n %pkg_libs
%defattr(-,root,root)
%pg_libdir/libecpg.so*
%pg_libdir/libpgfeutils.a
%pg_libdir/libpgtypes.so.*
%pg_libdir/libecpg_compat.so.*
%pg_libdir/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %pg_libs_conf

### server package

%package -n %pkg_server
Summary:	The programs needed to create and run a PostgreSQL server
%requires_main
%requires_libs
Requires(pre):		/usr/sbin/useradd /usr/sbin/groupadd
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig
Requires:		/usr/sbin/useradd, /sbin/chkconfig
Provides:		postgresql-server >= %{version}-%{release}

%description -n %pkg_server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The %pkg_server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%pre -n %pkg_server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post -n %pkg_server
/sbin/ldconfig

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=%pg_dbdir/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" > /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

# Create alternatives entries for common binaries and man files
for cmd in %pkg_server_cmd ; do
    %cmd_update_alt --install %{_bindir}/${cmd}        pgsql-${cmd}    %pg_bindir/${cmd}        %pg_alternative_prio
    %cmd_update_alt --install %{_mandir}/man1/${cmd}.1 pgsql-${cmd}man %pg_mandir/man1/${cmd}.1 %pg_alternative_prio
done

if [ $1 -eq 1 ] ; then
    if [ -x /bin/systemctl ]; then
        /bin/systemctl daemon-reload >/dev/null 2>&1 || :
        %systemd_post %pg_systemd_service
    else
        chkconfig --add %pg_sysvinit_service
    fi
fi

%preun -n %pkg_server
if [ $1 -eq 0 ] ; then
    if [ -x /bin/systemctl ]; then
        # Package removal, not upgrade
        /bin/systemctl --no-reload disable %pg_systemd_service >/dev/null 2>&1 || :
        /bin/systemctl stop %pg_systemd_service >/dev/null 2>&1 || :
    else
        /sbin/service %pg_sysvinit_service condstop >/dev/null 2>&1
        chkconfig --del %pg_sysvinit_service
    fi
fi

%postun -n %pkg_server

# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]; then
    for cmd in %pkg_server_cmd ; do
        %cmd_update_alt --remove pgsql-${cmd}    %pg_bindir/psql
        %cmd_update_alt --remove pgsql-${cmd}man %pg_mandir/man1/${cmd}.1
    done
fi

/sbin/ldconfig

if [ -x /bin/systemctl ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    if [ $1 -ge 1 ] ; then
        # Package upgrade, not uninstall
        /bin/systemctl try-restart %pg_systemd_service >/dev/null 2>&1 || :
    fi
else
    /sbin/service %pg_sysvinit_service condrestart >/dev/null 2>&1
fi

%files -n %pkg_server -f %pkg_server.list
%defattr(-,root,root)
%{_bindir}/pg_config-%pg_version_major
%pg_bindir/postgresql-setup
%pg_bindir/postgresql-check-db-dir
%{_unitdir}/%pg_systemd_service
%config(noreplace) %{_initrddir}/%pg_sysvinit_service
%if %enable_pam
%config(noreplace) /etc/pam.d/*
%endif
%attr (755,root,root) %dir %pg_etc_sysconfig
%pg_datadir/postgres.bki
%pg_datadir/postgres.description
%pg_datadir/postgres.shdescription
%pg_datadir/system_views.sql
%pg_datadir/*.sample
%pg_datadir/timezonesets/*
%pg_datadir/tsearch_data/*.affix
%pg_datadir/tsearch_data/*.dict
%pg_datadir/tsearch_data/*.ths
%pg_datadir/tsearch_data/*.rules
%pg_datadir/tsearch_data/*.stop
%pg_datadir/tsearch_data/*.syn
%pg_libdir/dict_int.so
%pg_libdir/dict_snowball.so
%pg_libdir/dict_xsyn.so
%pg_libdir/euc2004_sjis2004.so
%pg_libdir/pgoutput.so
%pg_libdir/plpgsql.so
%dir %pg_extdir
%pg_extdir/plpgsql*

%dir %pg_libdir
%dir %pg_datadir
%attr(700,postgres,postgres) %dir %pg_dbroot
%attr(700,postgres,postgres) %dir %pg_dbdir
%attr(700,postgres,postgres) %dir %pg_dbdir/data
%attr(700,postgres,postgres) %dir %pg_dbdir/backups
%attr(755,postgres,postgres) %dir %pg_rundir
%pg_libdir/*_and_*.so
%pg_datadir/information_schema.sql
%pg_datadir/snowball_create.sql
%pg_datadir/sql_features.txt
%pg_datadir/conversion_create.sql

%pg_libdir/chkpass.so
%pg_extdir/chkpass--1.0.sql
%pg_extdir/chkpass--unpackaged--1.0.sql
%pg_extdir/chkpass.control

### timetravel extension

%package -n %pkg_timetravel
Summary:	Timetravel extension for PostgreSQL
%requires_server

%description -n %pkg_timetravel
Provides the "time travel" extension for PostgreSQL,
which provides support for accessing historical data.

%files -n %pkg_timetravel
%defattr(-,root,root)
%pg_libdir/timetravel.so
%pg_extdir/timetravel--1.0.sql
%pg_extdir/timetravel--unpackaged--1.0.sql
%pg_extdir/timetravel.control

### xml extension

%if %enable_xml

%package -n %pkg_xml
Summary:	XML extension for PostgreSQL
%requires_server

%description -n %pkg_xml
Provides the XML extension for PostgreSQL.

%files -n %pkg_xml
%defattr(-,root,root)
%pg_libdir/pgxml.so
%pg_extdir/xml2*

%endif

### documentation package

%package -n %pkg_docs
Summary:	Extra documentation for PostgreSQL
Provides:	postgresql-docs >= %{version}-%{release}

%description -n %pkg_docs
The %pkg_docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation. This package also
includes HTML version of the documentation.

%files -n %pkg_docs
%defattr(-,root,root)
%pg_docdir/*
%exclude %pg_docdir/extension/*.example

### contrib package

%package -n %pkg_contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
%requires_main
%requires_libs
Provides:	postgresql-contrib >= %{version}-%{release}
%{?enable_selinux:Requires:	selinux-policy}

%description -n %pkg_contrib
The %pkg_contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%files -n %pkg_contrib
%defattr(-,root,root)
%pg_docdir/extension/*.example
%pg_libdir/_int.so
%pg_libdir/adminpack.so
%pg_libdir/amcheck.so
%pg_libdir/auth_delay.so
%pg_libdir/autoinc.so
%pg_libdir/auto_explain.so
%pg_libdir/bloom.so
%pg_libdir/btree_gin.so
%pg_libdir/btree_gist.so
%pg_libdir/citext.so
%pg_libdir/cube.so
%pg_libdir/dblink.so
%pg_libdir/earthdistance.so
%pg_libdir/file_fdw.so*
%pg_libdir/fuzzystrmatch.so
%pg_libdir/insert_username.so
%pg_libdir/isn.so
%pg_libdir/hstore.so
%if %enable_plperl
%pg_libdir/hstore_plperl.so
%endif
%pg_libdir/lo.so
%pg_libdir/ltree.so
%pg_libdir/moddatetime.so
%pg_libdir/pageinspect.so
%pg_libdir/passwordcheck.so
%pg_libdir/pgcrypto.so
%pg_libdir/pgrowlocks.so
%pg_libdir/pgstattuple.so
%pg_libdir/pg_buffercache.so
%pg_libdir/pg_freespacemap.so
%pg_libdir/pg_prewarm.so
%pg_libdir/pg_stat_statements.so
%pg_libdir/pg_trgm.so
%pg_libdir/pg_visibility.so
%pg_libdir/postgres_fdw.so
%pg_libdir/refint.so
%pg_libdir/seg.so
%if %enable_ssl
%pg_libdir/sslinfo.so
%endif
%if %enable_selinux
%pg_libdir/sepgsql.so
%pg_datadir/contrib/sepgsql.sql
%endif
%pg_libdir/tablefunc.so
%pg_libdir/tcn.so
%pg_libdir/test_decoding.so
%pg_libdir/tsm_system_rows.so
%pg_libdir/tsm_system_time.so
%pg_libdir/unaccent.so
%pg_libdir/uuid-ossp.so
%pg_extdir/uuid-ossp*
%pg_extdir/adminpack*
%pg_extdir/amcheck*
%pg_extdir/autoinc*
%pg_extdir/bloom*
%pg_extdir/btree_gin*
%pg_extdir/btree_gist*
%pg_extdir/citext*
%pg_extdir/cube*
%pg_extdir/dblink*
%pg_extdir/dict_int*
%pg_extdir/dict_xsyn*
%pg_extdir/earthdistance*
%pg_extdir/file_fdw*
%pg_extdir/fuzzystrmatch*
%pg_extdir/hstore.control
%pg_extdir/hstore--*.sql
%pg_extdir/hstore_plperl*
%pg_extdir/insert_username*
%pg_extdir/intagg*
%pg_extdir/intarray*
%pg_extdir/isn*
%pg_extdir/lo*
%pg_extdir/ltree.control
%pg_extdir/ltree--*.sql
%pg_extdir/moddatetime*
%pg_extdir/pageinspect*
%pg_extdir/pg_buffercache*
%pg_extdir/pg_freespacemap*
%pg_extdir/pg_prewarm*
%pg_extdir/pg_stat_statements*
%pg_extdir/pg_trgm*
%pg_extdir/pg_visibility*
%pg_extdir/pgcrypto*
%pg_extdir/pgrowlocks*
%pg_extdir/pgstattuple*
%pg_extdir/postgres_fdw*
%pg_extdir/refint*
%pg_extdir/seg*
%pg_extdir/hstore_plpython3u--1.0.sql
%pg_extdir/hstore_plpython3u.control
%pg_extdir/ltree_plpython3u--1.0.sql
%pg_extdir/ltree_plpython3u.control
%if %enable_ssl
%pg_extdir/sslinfo*
%endif
%pg_extdir/tablefunc*
%pg_extdir/tcn*
%pg_extdir/tsm_system_rows*
%pg_extdir/tsm_system_time*
%pg_extdir/unaccent*
%pg_bindir/oid2name
%pg_bindir/vacuumlo
%pg_bindir/pg_recvlogical
%pg_bindir/pg_standby
%pg_mandir/man1/oid2name.1
%pg_mandir/man1/pg_recvlogical.1
%pg_mandir/man1/pg_standby.1
%pg_mandir/man1/vacuumlo.1

### libpq -- postgresql client library

%package -n %pkg_libpq5
Summary:	PostgreSQL client library

%description -n %pkg_libpq5
Postgresql client library

%files -n %pkg_libpq5
%pg_libdir/libpq.so.*
%pg_localedir/*/LC_MESSAGES/libpq5*.mo

%post -n %pkg_libpq5
%cmd_update_alt --install %_libdir/libpq.so.5 pgsql-libpq5 %pg_libdir/libpq.so.5 %pg_alternative_prio

%postun -n %pkg_libpq5
%cmd_update_alt --remove pgsql-libpq5 %pg_libdir/libpq.so.5

### server devel package

%package -n %pkg_server_devel
Summary:	PostgreSQL development files for server extensions
%requires_server

%description -n %pkg_server_devel
PostgreSQL server development header files and libraries

%files -n %pkg_server_devel
%defattr(-,root,root)
%pg_libdir/pgxs/*

### generic devel package

%package -n %pkg_devel
Summary:	PostgreSQL development header files and libraries
%requires_main
%requires_libs
%requires_server_devel
Requires:	zlib-devel
BuildRequires:	readline-devel
%{?enable_pam:BuildRequires:		pam-devel}
%{?enable_ssl:BuildRequires:		openssl-devel}
%{?enable_xml:BuildRequires:		libxml2-devel libxslt-devel}
%{?enable_selinux:BuildRequires:	libselinux-devel >= 2.0.93}

%description -n %pkg_devel
The %pkg_devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a PostgreSQL server.

%files -n %pkg_devel -f %pkg_devel.list
%defattr(-,root,root)
%pg_includedir/*
%pg_bindir/ecpg
%pg_libdir/libpq.so
%pg_libdir/libecpg.so
%pg_libdir/libpq.a
%pg_libdir/libecpg.a
%pg_libdir/libecpg_compat.so
%pg_libdir/libecpg_compat.a
%pg_libdir/libpgcommon.a
%pg_libdir/libpgport.a
%pg_libdir/libpgtypes.so
%pg_libdir/libpgtypes.a
%pg_libdir/pkgconfig/*
%pg_mandir/man1/ecpg.*
%pg_mandir/man3/*
%pg_mandir/man7/*

### plperl package

%if %enable_plperl

%package -n %pkg_plperl
Summary:	The Perl procedural language for PostgreSQL
%requires_main
%requires_server
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:	postgresql-plperl >= %{version}-%{release}

%description -n %pkg_plperl
The %pkg_plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%files -n %pkg_plperl -f %pkg_plperl.list
%defattr(-,root,root)
%pg_libdir/plperl.so
%pg_extdir/plperl*

%endif

### plpython2 package

%if %enable_plpython2

%package -n %pkg_plpython2
Summary:	The Python procedural language for PostgreSQL
%requires_main
%requires_server
Provides:	postgresql-plpython >= %{version}-%{release}
Provides:	%{name}-plpython2%{?_isa} = %{version}-%{release}
Requires:	libpython2_7-1_0

%description -n %pkg_plpython2
The %pkg_plpython2 package contains the PL/Python procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python.

%files -n %pkg_plpython2 -f %pkg_plpython2.list
%defattr(-,root,root)
%pg_libdir/plpython2.so
%pg_extdir/plpython2u*
%pg_extdir/plpythonu*
%pg_libdir/hstore_plpython2.so
%pg_libdir/ltree_plpython2.so
%pg_extdir/*_plpythonu*
%pg_extdir/*_plpython2u*

%endif

### plpython3 package

%if %enable_plpython3

%package -n %pkg_plpython3
Summary:	The Python3 procedural language for PostgreSQL
%requires_main
%requires_server
Provides:	postgresql-plpython3 >= %{version}-%{release}
Requires:	python3-libs

%description -n %pkg_plpython3
The %pkg_plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.

%files -n %pkg_plpython3 -f %pkg_plpython3.list
%pg_extdir/plpython3*
%pg_libdir/plpython3.so
%pg_libdir/hstore_plpython3.so
%pg_libdir/jsonb_plpython3.so
%pg_libdir/ltree_plpython3.so
%pg_extdir/*_plpython3u*

%endif

### pltcl package

%if %enable_pltcl

%package -n %pkg_pltcl
Summary:	The Tcl procedural language for PostgreSQL
%requires_main
%requires_server
Requires:	tcl
Provides:	postgresql-pltcl >= %{version}-%{release}

%description -n %pkg_pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %pkg_pltcl package contains the PL/Tcl language
for the backend.

%files -n %pkg_pltcl -f %pkg_pltcl.list
%defattr(-,root,root)
%pg_libdir/pltcl.so
%pg_extdir/pltcl*

%endif

### MAIN package

%prep
%setup -q -n postgres-%{version}
./autogen.sh

%build

# plpython requires separate configure/build runs to build against python 2
# versus python 3. Our strategy is to do the python 3 run first, then make
# distclean and do it again for the "normal" build. Note that the installed
# Makefile.global will reflect the python 2 build, which seems appropriate
# since that's still considered the default plpython version.
%if %enable_plpython3

export PYTHON=/usr/bin/python3

%{configure_call}

# We need to build PL/Python and a few extensions:
# Build PL/Python
cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..
cd src/pl/plpython
%{__make} all
cd ..
# save built form in a directory that "make distclean" won't touch
%{__cp} -a plpython plpython3
cd ../..
# Build some of the extensions with PY3 support
for p3bl in %{python3_build_list} ; do
	p3blpy3dir="$p3bl"3
	pushd contrib/$p3bl
	MAKELEVEL=0 %{__make} %{?_smp_mflags} all
	cd ..
	# save built form in a directory that "make distclean" won't touch
	%{__cp} -a $p3bl $p3blpy3dir
	popd
done
# must also save this version of Makefile.global for later
%{__cp} src/Makefile.global src/Makefile.global.python3

%{__make} distclean

%endif

unset PYTHON
# Explicitly run Python2 here -- in future releases,
# Python3 will be the default.
export PYTHON=/usr/bin/python2

# Normal (not python3) build begins here
%{configure_call}

MAKELEVEL=0 %{__make} %{?_smp_mflags} all docs
%{__make} %{?_smp_mflags} -C contrib all

%install

%{__rm} -rf %buildroot

%{__make} DESTDIR=%buildroot install install-docs

%if %enable_plpython3
	%{__mv} src/Makefile.global src/Makefile.global.save
	%{__cp} src/Makefile.global.python3 src/Makefile.global
	touch -r src/Makefile.global.save src/Makefile.global
	# Install PL/Python3
	pushd src/pl/plpython3
	%{__make} DESTDIR=%buildroot install
	popd

	for p3bl in %{python3_build_list} ; do
		p3blpy3dir="$p3bl"3

		# Install jsonb_plpython3
		pushd contrib/$p3blpy3dir
		%{__make} DESTDIR=%buildroot install
		popd
	done

	%{__mv} -f src/Makefile.global.save src/Makefile.global
%endif

%{__make} -C contrib DESTDIR=%buildroot install

%{__mkdir} -p %buildroot/%pg_pamdir
cat postgresql.pam.in | %generate_file > %buildroot/%pg_pamdir/postgresql-%pg_version_major.pam

cat postgresql-setup.in | %generate_file > %buildroot/%pg_bindir/postgresql-setup
chmod 755 %buildroot/%pg_bindir/postgresql-setup

cat postgresql-check-db-dir.in | %generate_file > %buildroot/%pg_bindir/postgresql-check-db-dir
chmod 755 %buildroot/%pg_bindir/postgresql-check-db-dir

%{__mkdir} -p %buildroot/%{_unitdir}
cat postgresql.service.in | %generate_file > %buildroot/%{_unitdir}/%pg_systemd_service

%{__install} -d %buildroot/%{_initrddir}
cat postgresql.init.in | %generate_file > %buildroot/%{_initrddir}/%pg_sysvinit_service
chmod 755 %buildroot/%{_initrddir}/%pg_sysvinit_service

# Create the directory for sockets.
%{__install} -d -m 755 %buildroot/%pg_rundir

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
%{__install} -d -m 700 %buildroot/%pg_dbdir/data

# backups of data go here...
%{__install} -d -m 700 %buildroot/%pg_dbdir/backups

# Create the multiple postmaster startup directory
%{__install} -d -m 700 %buildroot/%pg_etc_sysconfig

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %buildroot/%pg_datadir/

cat postgresql-libs.conf.in | %generate_file > %buildroot/%pg_libs_conf
chmod u=rw,go=r %buildroot/%pg_libs_conf

mkdir -p %buildroot/%{_bindir}
ln -s %pg_bindir/pg_config %buildroot/%{_bindir}/pg_config-%pg_version_major

# create translations

for cmd in %pkg_main_cmd %pkg_server_cmd ecpg ecpglib6 pgscripts plpgsql; do
    %find_lang $cmd-%pg_version_major || touch $cmd-%pg_version_major.lang
done

# create file list for devel package

cat \
    ecpg-%pg_version_major.lang \
    ecpglib6-%pg_version_major.lang > %pkg_devel.list

# create file list for main package
(
    cat pgscripts-%pg_version_major.lang
    for cmd in %pkg_main_cmd ; do
        echo "%attr(755,root,root) %pg_bindir/$cmd"
        echo "%pg_mandir/man1/$cmd.*"
        cat $cmd-%pg_version_major.lang
    done
) > %pkg_main.list

# create package list for server package
(
    cat plpgsql-%pg_version_major.lang
    for cmd in %pkg_server_cmd ; do
        echo "%attr(755,root,root) %pg_bindir/$cmd"
        echo "%pg_mandir/man1/$cmd.*"
        cat $cmd-%pg_version_major.lang
    done
) > %pkg_server.list

# create file list for plperl package

%if %enable_plperl
%find_lang plperl-%pg_version_major
cat plperl-%pg_version_major.lang > %pkg_plperl.list
%endif

# create file list for plpython2 package

%if %enable_plpython2
%find_lang plpython-%pg_version_major
cat plpython-%pg_version_major.lang > %pkg_plpython2.list
%endif

# create file list for plpython3 package

%if %enable_plpython3
# plpython3 shares message files with plpython
%find_lang plpython-%pg_version_major
cat plpython-%pg_version_major.lang >> %pkg_plpython3.list
%endif

# create file list for pltcl package

%if %enable_pltcl
%find_lang pltcl-%pg_version_major
cat pltcl-%pg_version_major.lang > %pkg_pltcl.list
%endif

%clean
%{__rm} -rf %buildroot

%changelog
* Thu Jun 04 2020 Enrico Weigelt, metux IT consult <info@metux.net> - %pg_version_major.%pg_version_minor
- Refactored packaging for SLES12
