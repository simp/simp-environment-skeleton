#!/bin/sh

source `dirname $0`/gencerts_common.sh

check_cacerts

batch=1
if [ "$1" == "auto" ]; then
  batch=0
fi

create_ca

exit_code=0

for hosts in `cat togen`; do
  hosts=`echo $hosts | sed -e 's/[ \t]//g'`
  hname=`echo $hosts | cut -d',' -f1`
  if [ "$hname" != "$hosts" ];
  then
    alts=`echo $hosts | cut -d',' -f2-`
    altnames=''
    for i in `echo $alts | tr ',' '\n'`
    do
      ruby -r ipaddr -e "begin IPAddr.new('$i') rescue exit 1 end"
      if [ $? -eq 0 ]; then
        # This is required due to some applications not properly supporting the
        # IP version of subjectAltName.
        prefixes='IP DNS'
      else
        prefixes='DNS'
      fi

      for prefix in $prefixes; do
        if [ "$altnames" != ''  ]; then
          altnames+=",$prefix:$i"
        else
          altnames+="$prefix:$i"
        fi
      done
    done

    echo "processing $hname"
    sed -e "s/#HOSTNAME#/$hname/" -e "s/#ALTNAMES#/$altnames/" default_altnames.cnf > output/conf/$hname.cnf
  else
    echo "processing $hname"
    sed -e "s/#HOSTNAME#/$hname/" default.cnf > output/conf/$hname.cnf
  fi

  export OPENSSL_CONF=output/conf/$hname.cnf

  req_cert $hname "${keydist}/${hname}"

  exit_code=$?
done

if [[ $exit_code -eq 0 ]]; then
  distribute_ca
fi

exit $exit_code
