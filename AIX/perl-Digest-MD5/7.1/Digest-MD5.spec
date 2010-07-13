#
#   - Digest::MD5 -
#   This spec file was automatically generated by cpan2rpm [ver: 2.028]
#   The following arguments were used:
#       Digest-MD5-2.39.tar.gz -U --tempdir=/tmp/test
#   For more information on cpan2rpm please visit: http://perl.arix.com/
#

%define pkgname Digest-MD5
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1

name:      perl-Digest-MD5
summary:   Digest-MD5 - Perl interface to the MD5 Algorithm
version:   2.39
release:   2
vendor:    by Neil Winton <CN.Winton@axion.bt.co.uk>
packager:  Arix International <cpan2rpm@arix.com>
license:   Artistic
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: ppc
prefix:    %(echo %{_prefix})
source:    Digest-MD5-2.39.tar.gz

%description
The "Digest::MD5" module allows you to use the RSA Data Security
Inc. MD5 Message Digest algorithm from within Perl programs.  The
algorithm takes as input a message of arbitrary length and produces as
output a 128-bit "fingerprint" or "message digest" of the input.

Note that the MD5 algorithm is not as strong as it used to be.  It has
since 2005 been easy to generate different messages that produce the
same MD5 digest.  It still seems hard to generate messages that
produce a given digest, but it is probably wise to move to stronger
algorithms for applications that depend on the digest to uniquely identify
a message.

The "Digest::MD5" module provide a procedural interface for simple
use, as well as an object oriented interface that can handle messages
of arbitrary length and which can read files directly.

#
# This package was generated automatically with the cpan2rpm
# utility.  To get this software or for more information
# please visit: http://perl.arix.com/
#

%prep
%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
grep -rsl '^#!.*perl' . |
#   grep -v '.bak$' |xargs --no-run-if-empty \
grep -v '.bak$' |xargs \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
%{__make} 
%if %maketest
%{__make} test
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

# SuSE Linux
#        if [ -e /etc/SuSE-release -o -e /etc/UnitedLinux-release ]
#        then
#            %{__mkdir_p} %{buildroot}/var/adm/perl-modules
#            %{__cat} `find %{buildroot} -name "perllocal.pod"`  \
#                | %{__sed} -e s+%{buildroot}++g                 \
#                > %{buildroot}/var/adm/perl-modules/%{name}
#        fi

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
#        find %{buildroot}%{_prefix}             \
#            -type d -depth                      \
#            -exec rmdir {} \; 2>/dev/null

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    print "%doc  rfc1321.txt hints Changes README";
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
        }
    print join "\n", sort @ret;

    sub wanted {
        return if /auto$/;

        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;

        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;

        $dirs[@dirs] = $_;
        }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
        }
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %filelist
%defattr(-,root,root)

%changelog
* Mon Jun 21 2010 root@c114m4h1p04.ppd.pok.ibm.com
- Initial build.
