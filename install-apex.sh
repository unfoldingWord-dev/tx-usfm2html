#!/usr/bin/env bash

install_dir=$1  # first argument

version=$(curl -s https://api.github.com/repos/apex/apex/tags | grep -Eo '"name":.*?[^\\]",'  | head -n 1 | sed 's/[," ]//g' | cut -d ':' -f 2)
url="https://github.com/apex/apex/releases/download/${version}/apex_linux_amd64"

curl -sL ${url} -o ${install_dir}/apex
chmod +x ${install_dir}/apex
echo "INSTALL DIR = $install_dir"
ls ${install_dir}
