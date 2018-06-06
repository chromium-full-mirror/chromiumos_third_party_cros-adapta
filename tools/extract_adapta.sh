#!/bin/bash

# Copyright 2018 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

PRIMARY_COLOR="#1a73e8"

usage() {
  echo "Usage: $0 [-i] [-c PRIMARY_COLOR]"
  echo "-i"
  echo -e "\tInstall build dependancies"
  echo "-c PRIMARY_COLOR"
  echo -e "\tOverride the color setting. Default: $PRIMARY_COLOR"
  echo "Extracts a copy of the Adapta assets from a frozen version of adapta."
  echo "Should be run from the root of the CrosAdapta repository."
  exit 1
}

install_deps () {
  DEPS=(
    autoconf
    automake
    inkscape
    libgdk-pixbuf2.0-dev # gdk-pixbuf2-devel
    glib2.0-dev # glib2-devel
    libsass-dev
    libxml2
    pkg-config
    sassc
    parallel
  )

  # Install dependencies.
  echo "Sudo requested for installing dependencies ${DEPS[*]}"
  sudo apt install -y ${DEPS[*]}
}

build () {
  BUILD_FLAGS=(
   "--enable-parallel"       # Turn on parallel building.
   "--disable-gnome"         # Disable gnome-shell support.
   "--disable-cinnamon"      # Disable cinnamon support.
   "--disable-flashback"     # Disable flashback support.
   "--disable-xfce"          # Disable xfce support.
   "--disable-mate"          # Disable mate support.
   "--disable-openbox"       # Disable openbox support.
   "--with-selection_color=$PRIMARY_COLOR"
   "--with-accent_color=$PRIMARY_COLOR"
   "--with-suggestion_color=$PRIMARY_COLOR"
   "--with-destruction_color=#FF5252"
  )

  cd $SOURCE_DIR
  ./autogen.sh ${BUILD_FLAGS[*]}
  make
}

# Parse the options.
while getopts ":ic:" o; do
    case "${o}" in
        i)
            install_deps
            ;;
        c)
            PRIMARY_COLOR=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

# Unzip Adapta into the current directory.
SOURCE_ZIP="adapta_source.tar.gz"
SOURCE_DIR="adapta_source_3.93.1.1"

tar -xf $SOURCE_ZIP

# Run the build in a sub shell so that cd doesn't change our dir.
(build)

# Copy assets into CrosAdapta.
GTK2_ASSETS_SRC="$SOURCE_DIR/gtk/asset/assets-gtk2/*"
GTK3_ASSETS_SRC="$SOURCE_DIR/gtk/asset/assets-gtk3/*"

GTK2_ASSETS_DST="gtk-2.0/assets/"
GTK3_ASSETS_DST="gtk-3.0/assets/"

# Ensure that the assets dir exists.
mkdir -p $GTK2_ASSETS_DST
mkdir -p $GTK3_ASSETS_DST

# Copy extracted assets into the repo.
cp -r $GTK2_ASSETS_SRC $GTK2_ASSETS_DST
cp -r $GTK3_ASSETS_SRC $GTK3_ASSETS_DST

# Add the updates files.
git add -u

# Remove the untracked assets (e.g. assets removed since adapta import).
git ls-files --others gtk*/assets | xargs rm
# Remove the source files.
rm -r adapta_source_*
