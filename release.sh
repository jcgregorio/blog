# This bash file is intended to be used for building .deb release files.
# To use this file just create your own bash file in
# which you define the APPNAME and DESCRIPTION vars and the
# copy_release_files() function which copies all the files needed in the
# distribution in ${ROOT}. Then source this file after those definitions.
#
# Follow Debian conventions for file locations. For example:
#
# HTML Template files in    /usr/local/share/${APPNAME}/
# Binaries in               /usr/local/bin/${APPNAME}
# Small read/write files in /var/local/${APPNAME}/
# Config files in           /etc/${APPNAME}/
#
# The first command line argument to the calling script
# will be used as the 'note' for the release package.
#
# BYPASS_GENERATION
# -----------------
# If BYPASS_GENERATION is set then we know that the caller has created or
# copied in the debian file themselves, and we are to use it as-is. This is
# useful in cases where we are installing software that the author has already
# provided a debian package for, for example influxdb.
#
# DEPENDS
# -------
# If DEPENDS is specified it should be a list of dependencies that this package
# depends upon. Note that they will not be installed if missing. If you want
# packages installed beyond the base snapshot they that should be done in the
# startup script. See https://cloud.google.com/compute/docs/startupscript
#
# For more details see ../push/DESIGN.md.
#
# SYSTEMD
# -------
# If defined this should be a space separated list of *.service files that are
# to be enabled and started when the package is installed. The target system
# must support systemd. The service file(s) should be copied into
# /etc/systemd/system/*.service in your copy_release_files() function. A
# post-installation script will be run that enables and runs all such
# services.
#
# SYSTEMD_TIMER
# -------------
# If defined it is assumed to contain a systemd timer that will trigger a
# delayed setup and restart of the services. In this case the services
# identified in SYSTEMD are enabled, but not restarted.
# This is useful if a service needs to install a package via apt-get.
# With this delay a systemd unit is triggered after the package is installed.

set -x

ROOT=`mktemp -d`
OUT=`mktemp -d`

# Create all directories here, so their perms can be set correctly.
mkdir --parents ${ROOT}/DEBIAN

# Set directory perms.
sudo chmod 755 -R ${ROOT}

# Create the control files that describes this deb.
echo 2.0 > ${ROOT}/DEBIAN/debian-binary

cat <<-EOF > ${ROOT}/DEBIAN/control
	Package: ${APPNAME}
	Version: 1.0
	Depends: ${DEPENDS}
	Architecture: amd64
	Maintainer: ${USERNAME}@${HOST}
	Priority: optional
	Description: ${DESCRIPTION}
EOF

# Either restart SYSTEMD or SYSTEMD_TIMER.
RESTART_TARGET="$SYSTEMD"
if [ -v SYSTEMD_TIMER ]; then
  RESTART_TARGET=${SYSTEMD_TIMER}
fi

# Generate the post-install file that wires up the services.
cat <<-EOF > ${ROOT}/DEBIAN/postinst
#!/bin/bash
INIT_SCRIPT="${INIT_SCRIPT}"
set -e
if [ -e /bin/systemctl ]
then
  /bin/systemctl daemon-reload
EOF

# Only call enable if there is something to enable.
if [ ! -z "$SYSTEMD" ]; then
  cat <<-EOF >> ${ROOT}/DEBIAN/postinst
  /bin/systemctl enable ${SYSTEMD}
EOF
fi

# Only restart if there is a target defined.
if [ ! -z "$RESTART_TARGET" ]; then
  cat <<-EOF >> ${ROOT}/DEBIAN/postinst
  /bin/systemctl restart ${RESTART_TARGET}
EOF
fi

cat <<-EOF >> ${ROOT}/DEBIAN/postinst
elif [ ! -z "\$INIT_SCRIPT" ]
then
  update-rc.d \$INIT_SCRIPT enable
  service $INIT_SCRIPT start
fi
EOF
chmod 755 ${ROOT}/DEBIAN/postinst

copy_release_files

if [ ! -v BYPASS_GENERATION ]
then
  # Build the debian package.
  sudo dpkg-deb --build ${ROOT} ${OUT}/${APPNAME}.deb
else
  # Just use the debian package that copy_release_files
  # placed in ${ROOT}/{APPNAME}.deb.
  OUT=${ROOT}
fi

