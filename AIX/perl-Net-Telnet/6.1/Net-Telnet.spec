#
#   - Net-Telnet -
#   This spec file was automatically generated by cpan2rpm [ver: 2.028]
#   The following arguments were used:
#       Net-Telnet-3.03.tar.gz -U --tempdir=/tmp/test
#   For more information on cpan2rpm please visit: http://perl.arix.com/
#

%define pkgname Net-Telnet
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1

name:      perl-Net-Telnet
summary:   Net-Telnet - Interact with TELNET port or other TCP ports
version:   3.03
release:   2 
vendor:    Jay Rogers <jay@rgrs.com>
packager:  Arix International <cpan2rpm@arix.com>
license:   Artistic
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: ppc
prefix:    %(echo %{_prefix})
source:    Net-Telnet-3.03.tar.gz

%description
Net::Telnet allows you to make client connections to a TCP port and do
network I/O, especially to a port using the TELNET protocol.  Simple
I/O methods such as print, get, and getline are provided.  More
sophisticated interactive features are provided because connecting to
a TELNET port ultimately means communicating with a program designed
for human interaction.  These interactive features include the ability
to specify a time-out and to wait for patterns to appear in the input
stream, such as the prompt from a shell.

Other reasons to use this module than strictly with a TELNET port are:

=over 2

=item *

You're not familiar with sockets and you want a simple way to make
client connections to TCP services.

=item *

You want to be able to specify your own time-out while connecting,
reading, or writing.

=item *

You're communicating with an interactive program at the other end of
some socket or pipe and you want to wait for certain patterns to
appear.

=back

Here's an example that prints who's logged-on to the remote host
sparky.  In addition to a username and password, you must also know
the user's shell prompt, which for this example is "bash$"

    use Net::Telnet ();
    $t = new Net::Telnet (Timeout => 10,
                          Prompt => '/bash\$ $/');
    $t->open("sparky");
    $t->login($username, $passwd);
    @lines = $t->cmd("who");
    print @lines;

More examples are in the EXAMPLES section below.

Usage questions should be directed to the Usenet newsgroup
comp.lang.perl.modules.

Contact me, Jay Rogers <jay@rgrs.com>, if you find any bugs or have
suggestions for improvement.

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
    print "%doc  README";
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
* Tue Jun 22 2010 root@c114m4h1p04.ppd.pok.ibm.com
- Initial build.
