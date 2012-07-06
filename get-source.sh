#!/bin/sh
# Make snapshot of nacl-binutils
# Author: Elan Ruusamäe <glen@pld-linux.org>
# $Id$
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
repo_url=http://git.chromium.org/native_client/$package.git
specfile=crossnacl-binutils.spec
git_update=1

chrome_version=20.0.1132.47

chrome_revision=$(curl -s https://omahaproxy.appspot.com/revision?version=$chrome_version)
chrome_branch=$(IFS=.; set -- $chrome_version; echo $3)
test -e DEPS.py || svn cat http://src.chromium.org/chrome/branches/$chrome_branch/src/DEPS@$chrome_revision > DEPS.py
nacl_revision=$(awk -F'"' '/nacl_revision.:/{print $4}' DEPS.py)

export GIT_DIR=$package/.git

if [ ! -d $package ]; then
	git clone --depth 10 $repo_url $package
else
	git fetch
	git pull origin master
fi

# get src/native_client/tools/REVISIONS directly from svn
test -e NACL_REVISIONS.sh || svn cat https://src.chromium.org/native_client/trunk/src/native_client/tools/REVISIONS@$nacl_revision > NACL_REVISIONS.sh

if grep -Ev '^(#|(LINUX_HEADERS_FOR_NACL|NACL_(BINUTILS|GCC|GDB|GLIBC|NEWLIB))_COMMIT=[0-9a-f]+$|)' NACL_REVISIONS.sh >&2; then
	echo >&2 "I refuse to execute grabbed file for security concerns"
	exit 1
fi
. ./NACL_REVISIONS.sh

version=$(awk '/AM_INIT_AUTOMAKE/{v=$NF; sub(/\)/, "",v);print v}' $package/bfd/configure.in)
githash=$NACL_BINUTILS_COMMIT
shorthash=git$(git rev-parse --short $githash)
prefix=$package-$version-$shorthash

if [ -f $prefix.tar.bz2 ]; then
	echo "Tarball $prefix.tar.bz2 already exists"
	exit 0
fi

git archive $githash --prefix $prefix/ > $prefix.tar
bzip2 -9 $prefix.tar

../dropin $prefix.tar.bz2

rm -f NACL_REVISIONS.sh DEPS.py
