#!/bin/sh
# Make snapshot of nacl-binutils
# Author: Elan Ruusamäe <glen@pld-linux.org>
set -e

# Generated from git
# git clone http://git.chromium.org/native_client/nacl-binutils.git
# (Checkout ID taken from chromium-17.0.963.46/native_client/tools/REVISIONS)
# cd nacl-binutils
# git checkout 73acd6f5f2ec5daa6e9be737ade60f03e258602b
# cd ..
# For binutils version, grep "AM_INIT_AUTOMAKE(bfd, " bfd/configure.in
# mv nacl-binutils nacl-binutils-2.20.1-git73acd6f
# tar cfj nacl-binutils-2.20.1-git73acd6f.tar.bz2 nacl-binutils-2.20.1-git73acd6f

package=nacl-binutils
repo_url=https://chromium.googlesource.com/native_client/$package
nacl_trunk=http://src.chromium.org/native_client/trunk
omahaproxy_url=http://omahaproxy.appspot.com
specfile=crossnacl-binutils.spec

chrome_channel=${1:-stable}
chrome_version=$(curl -s "$omahaproxy_url/all?os=linux&channel=$chrome_channel" | awk -F, 'NR > 1{print $3}')
test -n "$chrome_version"
chrome_revision=$((echo 'data='; curl -s $omahaproxy_url/revision.json?version=$chrome_version; echo ',print(data.chromium_revision)') | js)
test -n "$chrome_revision"
chrome_branch=$(IFS=.; set -- $chrome_version; echo $3)
test -s DEPS.py || svn cat http://src.chromium.org/chrome/branches/$chrome_branch/src/DEPS@$chrome_revision > DEPS.py
nacl_revision=$(awk -F'"' '/nacl_revision.:/{print $4}' DEPS.py)
test -n "$nacl_revision"

export GIT_DIR=$package.git

if [ ! -d $GIT_DIR ]; then
	install -d $GIT_DIR
	git init --bare
	git remote add origin $repo_url
	git fetch --depth 1 origin refs/heads/master:refs/remotes/origin/master
else
	git fetch origin refs/heads/master:refs/remotes/origin/master
fi

# get src/native_client/tools/REVISIONS directly from svn
test -n "$nacl_revision"
test -s NACL_REVISIONS.sh || svn cat $nacl_trunk/src/native_client/tools/REVISIONS@$nacl_revision > NACL_REVISIONS.sh

if grep -Ev '^(#|(LINUX_HEADERS_FOR_NACL|NACL_(BINUTILS|GCC|GDB|GLIBC|NEWLIB))_COMMIT=[0-9a-f]+$|)' NACL_REVISIONS.sh >&2; then
	echo >&2 "I refuse to execute grabbed file for security concerns"
	exit 1
fi
. ./NACL_REVISIONS.sh

githash=$NACL_BINUTILS_COMMIT
git show $githash:bfd/configure.in > configure.in
version=$(awk '/AC_INIT/{v=$2; gsub(/[\[\])]*/, "",v);print v}' configure.in)
shorthash=$(git rev-parse --short $githash)
prefix=$package-$version-git$shorthash
archive=$prefix.tar.xz

if [ -f $archive ]; then
	echo "Tarball $archive already exists at $shorthash"
	rm -f NACL_REVISIONS.sh DEPS.py configure.in
	exit 0
fi

git -c tar.tar.xz.command="xz -9c" archive $githash --prefix $prefix/ -o $archive

../dropin $archive

rm -f NACL_REVISIONS.sh DEPS.py configure.in
