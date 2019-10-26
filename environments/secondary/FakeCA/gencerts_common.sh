#!/bin/sh

# Common functions for gencerts items.

if [ ! -z "${KEYDIST}" ]; then
  keydist="${KEYDIST}"
else
  keydist="`dirname $0`/../site_files/pki_files/files/keydist"
fi

export CATOP="`pwd`/demoCA"

check_cacerts () {
  if [ ! -f cacertkey ]; then
    dd if=/dev/urandom status=none bs=60 count=1 | openssl base64 -e -nopad | tr -d '\n' > cacertkey
    echo '' >> cacertkey
  fi
}

create_ca () {
  if [ ! -d demoCA ]; then
    export OPENSSL_CONF=ca.cnf;

    sed -i "s/^\([[:space:]]*commonName_default\).*/\1 \t\t= Fake Org Fake CA - `uuidgen | cut -f1 -d'-'`/" ca.cnf;

    CA='./CA'

    if [ $batch -eq 0 ]; then
      CA='./CA_batch'
    fi

    $CA -newca

    if [ $? -ne 0 ]; then
      echo "Error creating CA"
      exit 1
    fi
  fi

  if [ ! -d output/conf ]; then
    mkdir -p "output/conf"
  fi

  if [ ! -d working ]; then
    mkdir -p "working"
  fi

  if [ ! -d output/users ]; then
    mkdir -p "output/users"
  fi
}

distribute_ca () {
  cacert="demoCA/cacert.pem";
  hash=`openssl x509 -in $cacert -hash -noout`;
  cacerts="${keydist}/cacerts";

  if [ ! -d $cacerts ]; then
    mkdir -p $cacerts;
  fi

  suffix=0;

  if [ -f $cacerts/$hash.0 ] && [ "`md5sum $cacert | cut -f1 -d' '`" != "`md5sum $cacerts/$hash.0 | cut -f1 -d' '`" ]; then
    echo "Found existing CA cert, preserving....";
    pushd .;
    cd $cacerts;
    suffix=$(( 1 + `ls $hash.* | sort -n | tail -1 | cut -f2 -d'.'` ));
    mv -f cacert.pem $hash.$suffix;
    popd;
  elif [ -f $cacerts/$hash.0 ]; then
    echo "Existing CA cert does not need to be replaced....";
  else
    echo "Copying in new CA cert...."
    ca_id=`grep '^[[:space:]]*commonName_default' ca.cnf | rev | cut -f1 -d' ' | rev`

    cp $cacert $cacerts/cacert_${ca_id}.pem;

    cd $cacerts;
    ln -s cacert_${ca_id}.pem $hash.0;

    cd -;
  fi

  if [[ $UID -eq 0 ]]; then
    chmod -R u+rwX,g+rX,o-rwx $keydist;
    chown -R root.`/opt/puppetlabs/bin/puppet config print group 2>/dev/null` $keydist;
  fi
}

req_cert () {
  cert_id=$1
  dist_dir=$2

  if [ -z "${cert_id}" ]; then
    echo 'Error: You must pass a target name directory to req_cert()'
    return 1
  fi

  if [ -z "${dist_dir}" ]; then
    echo 'Error: You must pass a target output directory to req_cert()'
    return 1
  fi

  echo 'Creating certificate request'

  reqfile="working/${cert_id}.req.pem"
  staging="working/${cert_id}/staging"

  mkdir -p "${staging}"

  echo 'Running openssl req'

  openssl req -new -nodes -keyout "${staging}/${cert_id}.pem" -out "${reqfile}" -batch

  req_subj=`openssl req -in "${reqfile}" -noout -subject | sed -e 's/^subject=//' | sed -e 's/[[:space:]]=[[:space:]]/=/g' | sed -e 's_[[:space:]]*,[[:space:]]*_/_g'`

  if [ -z "${req_subj}" ]; then
    echo "Error: Could not determine the subject in '${reqfile}'"
    return 1
  fi

  # The fourth field of index.txt is the certificate hash
  existing_certs=`grep "^V[[:space:]].*${req_subj}" demoCA/index.txt | cut -f4`

  for cert in $existing_certs; do
    if [ ! -d demoCA/revoked ]; then
      mkdir demoCA/revoked
    fi

    certfile="demoCA/newcerts/${cert}.pem"

    echo "Found existing certificate for ${cert_id}, revoking!"
    OPENSSL_CONF=ca.cnf openssl ca -passin file:cacertkey -revoke ${certfile} -crl_reason superseded
    mv $certfile demoCA/revoked
  done

  echo "Running openssl ca"
  openssl ca -passin file:cacertkey -batch -out ${staging}/${cert_id}.pub -infiles ${reqfile}

  cat ${staging}/${cert_id}.pub >> ${staging}/${cert_id}.pem

  echo 'Validating newly created certs'

  pub_sig=`openssl x509 -noout -modulus -in ${staging}/${cert_id}.pub | openssl sha256`
  priv_sig=`openssl rsa -noout -modulus -in ${staging}/${cert_id}.pem | openssl sha256`

  if [ "${pub_sig}" != "${priv_sig}" ]; then
    echo "Error: Private key does not match public key for '${cert_id}'"
    return 2
  else
    if [ ! -d "${dist_dir}" ]; then
      echo "Creating directory '${dist_dir}'"
      mkdir -p "${dist_dir}/cacerts"
    fi

    cp -r "${staging}"/* "${dist_dir}"
    return 0
  fi
}
