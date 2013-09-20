#!/bin/bash
##
## Mailman Hack: Rotate and compress archived mbox files
## Copyright (c) 2013 SATOH Fumiyasu @ OSS Technology Corp., Japan
##
## License: GNU General Public License version 2 or later
##
## Requiremetns: run.py (withlist module)
##

set -u
umask 0022
renice 1 "$$" >/dev/null 2>&1 || :
ionice -c 3 -p "$$" >/dev/null 2>&1 || :

perr()
{
  echo "$0: ERROR: $1" 1>&2
}

pdie()
{
  perr "$1"
  exit ${2-1}
}

mm_user="${MM_USER:-@MM_USER@}"

bin_dir="${MM_BINDIR-@MM_BINDIR@}"
var_dir="${MM_VARDIR-@MM_VARDIR@}"

cmd_usage="Usage: $0 [OPTIONS] [LIST-NAME]"

## ----------------------------------------------------------------------

if [[ $(id |sed -n 's/^[^=]*=[0-9]*(\([^)]*\)).*$/\1/p') != $mm_user ]]; then
  pdie "Run this command with Mailman user: $mm_user"
fi

## ----------------------------------------------------------------------

all=''
suffix=''

while [[ $# -gt 0 ]]; do
  opt="$1"; shift

  ## -ovalue → -o value
  if [[ -z "${opt##-[s]?*}" ]]; then
    set -- "${opt#??}" ${1+"$@"}
    opt="${opt%$1}"
  ## -abc → -a -bc
  elif [[ -z "${opt##-[!-]?*}" ]]; then
    set -- "-${opt#??}" ${1+"$@"}
    opt="${opt%${1#-}}"
  ## --option=value → --option value
  elif [[ -z "${opt##--*=*}" ]]; then
    set -- "${opt#--*=}" ${1+"$@"}
    opt="${opt%%=*}"
  fi

  case "$opt" in
  --help)
    echo "$cmd_usage"
    exit 0
    ;;
  -a|--all-lists)
    all="set"
    ;;
  -s|--suffix)
    if [[ -z ${1-} ]]; then
      pdie "Invalid option value: $opt ${1-UNSPECIFIED}"
    fi
    suffix="$1"
    shift
    ;;
  --)
    break
    ;;
  -*)
    pdie "Invalid option: $opt"
    ;;
  *)
    set -- "$opt" ${1+"$@"}
    break
    ;;
  esac
done

if [[ -z $all && $# -eq 0 || -n $all && $# -gt 0 ]]; then
  echo "$cmd_usage"
  exit 1
fi

if [[ -z $suffix ]]; then
  suffix=$(date '+%Y%m')
  let suffix--
  if [[ $suffix = @(*00) ]]; then
    suffix="${suffix%00}"
    let suffix--
    suffix="${suffix}12"
  fi
fi

{
  if [[ -n $all ]]; then
    "$bin_dir/list_lists" --bare
  else
    for ml_name in "$@"; do
      echo "$ml_name"
    done
  fi
} \
|while read ml_name; do
  mbox_src="$var_dir/archives/private/$ml_name.mbox/$ml_name.mbox"
  mbox_dst="$mbox_src.$suffix"

  [[ -s $mbox_src ]] || continue
  [[ -f $mbox_dst || -f $mbox_dst.gz ]] && continue

  "$bin_dir/withlist" --lock --quiet --run run "$ml_name" \
    mv "$mbox_src" "$mbox_dst" || exit 1

  gzip -1 "$mbox_dst" || exit 1
done

exit 0

